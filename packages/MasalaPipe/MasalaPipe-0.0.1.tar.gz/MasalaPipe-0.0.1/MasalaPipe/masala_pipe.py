import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.model_selection import StratifiedKFold
from sklearn import metrics
from .LGBM_otm import LGBMOptimizator
from .rank_count import RankCountVectorizer
from scipy.stats import ks_2samp
from feature_engine.selection import DropConstantFeatures, SmartCorrelatedSelection
from lightgbm import LGBMClassifier
import mrmr
from BorutaShap import BorutaShap
import shap
from numpy import mean
from numpy import std
from rich.console import Console
from rich.progress import track

console = Console()
plt.rcParams["figure.dpi"] = 300
plt.rcParams["font.size"] = 12
# pd.options.mode.chained_assignment = None


class MasalaPipe:
    """

    """

    def __init__(
        self,
        data,
        id_label,
        features,
        target,
        categorical_features=[],
        col_safra=None,
        test_size=0.3,
        niter=10,
        metric_eval="AUC",
        metric_method="default",
        thr_train_test=0.5,
        correlation_tol=0.85,
        constant_tol=0.95,
        early_stopping_rounds=3,
        eval_features=False,
        filename_storage="LGBM_search",
        save_in_txt=False,
        rank_count=True,
        params_test=None,
    ):

        self.validate_inputs(data, id_label, col_safra, target, features)
        self.data = data
        self.id_label = id_label
        self.target = target
        self.features = features
        self.categorical_features = categorical_features
        self.col_safra = col_safra
        self.test_size = test_size
        self.niter = niter
        self.metric_eval = metric_eval
        self.metric_method = metric_eval
        self.thr_train_test = thr_train_test
        self.correlation_tol = correlation_tol
        self.constant_tol = constant_tol
        self.early_stopping_rounds = early_stopping_rounds
        self.eval_features = eval_features
        self.rank_count = rank_count
        self.params_test = params_test
        self.filename_storage = filename_storage
        self.save_in_txt = save_in_txt

    def validate_inputs(self, data, id_label, col_safra, target, features):
        if col_safra != None:
            assert (set([target, id_label, col_safra]).union(set(features))).issubset(
                (set(data.columns))
            ), f"{target, id_label, col_safra} and {features} most be columns in raw_data"
            assert set(data[target].unique()) == {0, 1}, "target must be only 0 " "or 1"
        else:
            assert (set([target, id_label]).union(set(features))).issubset(
                (set(data.columns))
            ), f"{target, id_label} and {features} most be columns in raw_data"
            assert set(data[target].unique()) == {0, 1}, "target must be only 0 " "or 1"

    def split_train_test(self):
        X = self.data
        y = self.data[[self.target]]
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, random_state=42, test_size=self.test_size
        )
        self.X_test = self.X_test[
            ~self.X_test[self.id_label].isin(self.X_train[self.id_label].unique())
        ]
        self.y_test = self.X_test[[self.target]]

    def preprocess(self):
        self.split_train_test()
        self.find_irrelevant_features()
        self.find_correlated_features()

    def run_pipe(self):
        self.params_select()
        self.fit_model(
            self.params,
            self.X_train.copy(),
            self.X_test.copy(),
            self.y_train,
            self.y_test,
        )
        self.performance_resume()

    def params_select(self):
        console.log("--> Parameters select")
        if self.params_test == None:
            model_opt = LGBMOptimizator(
                self.X_train,
                self.y_train,
                self.target,
                self.features,
                self.categorical_features,
                self.niter,
                self.metric_eval,
                self.metric_method,
                self.thr_train_test,
                self.col_safra,
                self.early_stopping_rounds,
                self.eval_features,
                self.filename_storage,
                self.save_in_txt,
            )
            best_trial, self.study = model_opt.get_optimal_params()
            self.params = best_trial.params
            if self.eval_features:
                del self.params["n_features"]
                self.features = [
                    x
                    for x in self.features
                    if x in best_trial.user_attrs["selected_features"]
                ]
                self.categorical_features = [
                    x
                    for x in self.categorical_features
                    if x in best_trial.user_attrs["selected_features"]
                ]
        else:
            self.params = self.params_test
        console.print(f"selected parameters: {self.params}")

    def fit_model(self, params, X_train, X_test, y_train, y_test):
        console.log("--> Fit model")
        clf = LGBMClassifier(**self.params)
        if len(self.categorical_features) > 0:
            rc = RankCountVectorizer()
            X_train[self.categorical_features] = X_train[
                self.categorical_features
            ].astype(str)
            X_test[self.categorical_features] = X_test[
                self.categorical_features
            ].astype(str)
            X_train = rc.fit_transform(X_train, cols=self.categorical_features)
            X_test = rc.transform(X_test, cols=self.categorical_features)
            clf.fit(X_train[self.features], y_train[self.target])
            self.rc = rc
            self.rc_vec = rc.vec
        else:
            clf.fit(X_train[self.features], y_train[self.target])
        self.clf = clf

    def performance_resume(self):
        console.log("--> Performance")
        prob_train = self.get_preds(self.X_train.copy())
        prob_test = self.get_preds(self.X_test.copy())
        console.print(
            f"AUC train: {metrics.roc_auc_score(self.y_train[self.target], prob_train):.4f}"
        )
        console.print(
            f"AUC test: {metrics.roc_auc_score(self.y_test[self.target], prob_test):.4f}"
        )
        console.print(
            f"KS train: {self.ks(self.y_train[self.target], prob_train)*100:.2f}"
        )
        console.print(
            f"KS test: {self.ks(self.y_test[self.target], prob_test)*100:.2f}"
        )

        self.plot_roc_curve(self.y_test[self.target], prob_test)

        console.log("--> Feature Importance")
        imp = pd.DataFrame(self.clf.feature_importances_, self.features).reset_index()
        imp.columns = ["var", "imp"]
        imp = imp.sort_values("imp", ascending=False)
        self.imp = imp
        sns.barplot(x="imp", y="var", color="#006e9cff", data=imp.iloc[:15])
        plt.title(f"Feature Importance")
        plt.show()

        console.log("--> Shap Explainer")
        X_shap = self.X_train[self.features]
        if len(self.categorical_features) > 0:
            X_shap[self.categorical_features] = X_shap[
                self.categorical_features
            ].astype(str)
            X_shap = self.rc.transform(X_shap, cols=self.categorical_features)
        explainer = shap.TreeExplainer(self.clf)
        shap_values = explainer.shap_values(X_shap)
        shap.summary_plot(shap_values[1], X_shap)
        shap_df = pd.DataFrame(np.abs(shap_values[1]), columns=[self.features])
        shap_df = (
            pd.DataFrame(shap_df.mean(), columns=["impact"])
            .reset_index()
            .rename(columns={"level_0": "var"})
            .sort_values(by=["impact"], ascending=False)
        )
        self.shap_df = shap_df
        sns.barplot(x="impact", y="var", color="red", data=shap_df.iloc[:15])
        plt.title(f"SHAP Impact")
        plt.show()

    def assert_can_predict(self, data):
        assert set(self.features).issubset(
            data.columns
        ), "Need variables used for training"

    def get_preds(self, data):
        self.assert_can_predict(data)
        if (len(self.categorical_features)) > 0:
            data[self.categorical_features] = data[self.categorical_features].astype(
                str
            )
            data = self.rc.transform(data, cols=self.categorical_features)
        preds = self.clf.predict_proba(data[self.features])[:, 1]
        return preds

    def mrmr_features_select(self, k):
        console.log("|Features select| MRMR")
        X = self.X_train.copy()
        rc = RankCountVectorizer()
        X[self.categorical_features] = X[self.categorical_features].astype(str)
        X = rc.fit_transform(X, cols=self.categorical_features)
        self.selected_features_mrmr = mrmr.mrmr_classif(
            X=X[self.features], y=X[[self.target]], K=k
        )
        self.features = [x for x in self.features if x in self.selected_features_mrmr]
        self.categorical_features = [
            x for x in self.categorical_features if x in self.selected_features_mrmr
        ]

    def borutashap_features_select(self):
        console.log("|Features select| BorutaShap")
        model = LGBMClassifier()
        X = self.X_train.copy()
        rc = RankCountVectorizer()
        X[self.categorical_features] = X[self.categorical_features].astype(str)
        X = rc.fit_transform(X, cols=self.categorical_features)
        Feature_Selector = BorutaShap(
            model=model, importance_measure="shap", classification=True
        )
        Feature_Selector.fit(
            X=X[self.features],
            y=X[self.target],
            n_trials=100,
            sample=False,
            train_or_test="test",
            normalize=True,
            verbose=True,
        )
        subset = Feature_Selector.Subset()
        self.selected_features_boruta = list(subset.columns)
        self.features = [x for x in self.features if x in self.selected_features_boruta]
        self.categorical_features = [
            x for x in self.categorical_features if x in self.selected_features_boruta
        ]
        console.print(
            f"Total selected features in BorutaShap {len(self.selected_features_boruta)}"
        )

    def forward_features_select(
        self,
        X_train,
        params,
        imp_df,
        target,
        categorical_features=[],
        k_folds=5,
        rank_count=True,
    ):
        console.log("|Features select| forward features select")

        y_train = X_train[[target]]

        skf = StratifiedKFold(n_splits=k_folds, random_state=42, shuffle=True)

        features_temp = list(imp_df["var"])
        features = []
        features_cat = []
        features.append(imp_df.iloc[0][0])
        if features[0] in categorical_features:
            features_cat.append(features[0])
        features_temp.remove(imp_df.iloc[0][0])
        model = LGBMClassifier(**params)
        score_train = []
        score_val = []
        for train_index, val_index in skf.split(X_train, y_train):
            X_train_k_fold = X_train.iloc[train_index, :]
            y_train_k_fold = y_train.iloc[train_index, :]
            X_val_k_fold = X_train.iloc[val_index, :]
            y_val_k_fold = y_train.iloc[val_index, :]

            if len(categorical_features) > 0:
                if rank_count:
                    rc = RankCountVectorizer()
                    X_train_k_fold[features_cat] = X_train_k_fold[features_cat].astype(
                        str
                    )
                    X_val_k_fold[features_cat] = X_val_k_fold[features_cat].astype(str)
                    X_train_k_fold = rc.fit_transform(X_train_k_fold, cols=features_cat)
                    X_val_k_fold = rc.transform(X_val_k_fold, cols=features_cat)
                    model.fit(X_train_k_fold[features], y_train_k_fold[target])
                else:
                    model.fit(
                        X_train_k_fold[features],
                        y_train_k_fold[target],
                        cat_features=features_cat,
                    )
            else:
                model.fit(X_train_k_fold[features], y_train_k_fold[target])

            p_train = model.predict_proba(X_train_k_fold[features])[:, 1]
            p_val = model.predict_proba(X_val_k_fold[features])[:, 1]
            score_train.append(metrics.roc_auc_score(y_train_k_fold[target], p_train))
            score_val.append(metrics.roc_auc_score(y_val_k_fold[target], p_val))
        score_temp = np.mean(score_val)
        std_temp = np.std(score_val)
        console.print(
            "Best Feature:", features[0], "AUC = ", score_temp, "+/- ", std_temp
        )
        n = 2
        len_features = len(features_temp) + 1
        for variavel in track(features_temp, description="Selecting features..."):
            model = LGBMClassifier(**params)
            score_train = []
            score_val = []
            features_cat = [
                var for var in features + [variavel] if var in categorical_features
            ]

            for train_index, val_index in skf.split(X_train, y_train):
                X_train_k_fold = X_train.iloc[train_index, :]
                y_train_k_fold = y_train.iloc[train_index, :]
                X_val_k_fold = X_train.iloc[val_index, :]
                y_val_k_fold = y_train.iloc[val_index, :]

                if len(categorical_features) > 0:
                    if rank_count:
                        rc = RankCountVectorizer()
                        X_train_k_fold[features_cat] = X_train_k_fold[
                            features_cat
                        ].astype(str)
                        X_val_k_fold[features_cat] = X_val_k_fold[features_cat].astype(
                            str
                        )
                        X_train_k_fold = rc.fit_transform(
                            X_train_k_fold, cols=features_cat
                        )
                        X_val_k_fold = rc.transform(X_val_k_fold, cols=features_cat)
                        model.fit(
                            X_train_k_fold[features + [variavel]],
                            y_train_k_fold[target],
                        )
                    else:
                        model.fit(
                            X_train_k_fold[features + [variavel]],
                            y_train_k_fold[target],
                            cat_features=features_cat,
                        )
                else:
                    model.fit(
                        X_train_k_fold[features + [variavel]], y_train_k_fold[target]
                    )

                p_train = model.predict_proba(X_train_k_fold[features + [variavel]])[
                    :, 1
                ]
                p_val = model.predict_proba(X_val_k_fold[features + [variavel]])[:, 1]
                score_train.append(
                    metrics.roc_auc_score(y_train_k_fold[target], p_train)
                )
                score_val.append(metrics.roc_auc_score(y_val_k_fold[target], p_val))
            score = np.mean(score_val)
            std = np.std(score_val)
            if score > score_temp:
                score_temp = score
                features.append(variavel)
                console.print(
                    f"[{n}/{len_features}] Feature add:",
                    variavel,
                    "AUC = ",
                    score,
                    "+/- ",
                    std,
                )
            else:
                console.print(
                    f"[{n}/{len_features}] Feature no add:",
                    variavel,
                    "AUC = ",
                    score,
                    "+/- ",
                    std,
                )
            n += 1
        console.log(f"Total selected features: {len(features)}")
        return features

    def ks(self, y, y_pred):
        return ks_2samp(y_pred[y == 1], y_pred[y != 1]).statistic

    def plot_roc_curve(self, y_test, prob_test):
        fpr, tpr, thresholds = metrics.roc_curve(y_test, prob_test)
        auc = metrics.roc_auc_score(y_test, prob_test)

        plt.figure(dpi=300.0)
        plt.plot(
            fpr,
            tpr,
            color="darkorange",
            label="AUC = %0.2f" % auc,
        )
        plt.plot([0, 1], [0, 1], color="navy", linestyle="--")
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel("False Positive Rate")
        plt.ylabel("True Positive Rate")
        plt.title("ROC Curve")
        plt.legend(loc="lower right")
        plt.rcParams["figure.dpi"] = 300
        plt.rcParams["font.size"] = 12
        plt.show()

    def find_irrelevant_features(self):
        raw_data = self.X_train[self.features]
        const_dropper = DropConstantFeatures(
            tol=self.constant_tol, missing_values="include"
        )
        const_dropped = const_dropper.fit_transform(raw_data)
        self.constant_features = const_dropper.features_to_drop_
        self.features = [x for x in self.features if x not in self.constant_features]
        self.categorical_features = [
            x for x in self.categorical_features if x not in self.constant_features
        ]
        console.log(
            f"|Preprocess| total constant features dropped: {len(self.constant_features)}"
        )

    def find_correlated_features(self):
        corr_droper = SmartCorrelatedSelection(
            method="spearman",
            threshold=self.correlation_tol,
            selection_method="model_performance",
            scoring="roc_auc",
            estimator=LGBMClassifier(),
        )
        corr_droper.fit(X=self.X_train[self.features], y=self.X_train[[self.target]])
        self.correlated_features = corr_droper.features_to_drop_
        self.features = [x for x in self.features if x not in self.correlated_features]
        self.categorical_features = [
            x for x in self.categorical_features if x not in self.correlated_features
        ]
        console.log(
            f"|Preprocess| total correlated features dropped: {len(self.correlated_features)}"
        )
