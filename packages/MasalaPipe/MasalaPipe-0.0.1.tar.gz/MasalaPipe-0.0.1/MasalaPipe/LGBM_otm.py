import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedKFold
from sklearn import metrics
from scipy.stats import ks_2samp
from lightgbm import LGBMClassifier
from .rank_count import RankCountVectorizer
from sklearn import metrics
from numpy import mean
from numpy import std
import optuna
import shap
from optuna.storages import JournalStorage, JournalFileStorage
from rich.console import Console

console = Console()

class LGBMOptimizator:
    def __init__(
        self,
        x,
        y,
        target,
        features,
        categorical_features=[],
        niter=10,
        metric_eval="AUC",
        metric_method="default",
        thr=0.5,
        col_safra=None,
        early_stopping_rounds=3,
        eval_n_features=False,
        filename_storage="LGBM_search",
        save_in_txt=True,
        verbose=True,
    ):
        """
        metric_eval: 'AUC' or 'KS'
        metric_method: 'default', 'min', 'range'
        """
        self.x = x
        self.y = y
        self.features = features
        self.categorical_features = categorical_features
        self.target = target
        self.col_safra = col_safra
        self.niter = niter
        self.metric_eval = metric_eval
        self.metric_method = metric_method
        self.thr = thr
        self.early_stopping_rounds = early_stopping_rounds
        self.eval_n_features = eval_n_features
        self.verbose = verbose
        self.best_auc = 0.0
        self.score = 0.0
        self.iterations_not_improving = 0
        self.iterations = 0
        self.filename_storage = filename_storage
        self.save_in_txt = save_in_txt

    def get_optimal_params(self):
        if self.save_in_txt:
            self.create_log()
        optuna.logging.set_verbosity(optuna.logging.WARNING)
        if self.eval_n_features:
            self.get_baseline_model(
                self.x.copy(),
                self.y,
                self.target,
                self.features,
                self.categorical_features,
            )
        objective = self.generate_objective_function(
            self.x,
            self.y,
            self.target,
            self.features,
            self.categorical_features,
        )
        storage = JournalStorage(JournalFileStorage(f"{self.filename_storage}.log"))
        study = optuna.create_study(
            direction="maximize",
            study_name="Hyperparameter search",
            storage=storage,
            load_if_exists=True,
        )
        study.optimize(
            objective,
            n_trials=self.niter,
            callbacks=[self.early_stopping_fn],
            n_jobs=1,
        )
        best_trial = study.best_trial
        return best_trial, study

    def early_stopping_fn(
        self, study: optuna.study.Study, trial: optuna.trial.FrozenTrial
    ):
        if self.iterations_not_improving >= self.early_stopping_rounds:
            study.stop()

    def update_best_params(self, score, test_metrics):
        self.iterations += 1
        if score > self.best_auc:
            self.iterations_not_improving = 0
            self.best_auc = score
            if self.verbose:
                console.print(
                    f"|Iteration {self.iterations}| New parameters found - {self.metric_eval} of {np.mean(test_metrics):.4f} ({self.best_auc:.4f})"
                )
        else:
            self.iterations_not_improving += 1
            # print(self.iterations_not_improving)

    def ks(self, y, y_pred):
        return ks_2samp(y_pred[y == 1], y_pred[y != 1]).statistic

    def train_model(self, parameters, x, y):
        model = LGBMClassifier(**parameters)
        model.fit(x, y)
        return model

    def predict(self, model, x):
        return model.predict_proba(x)[:, 1]

    def get_metric_min(self, df, target, metric_eval, col_safra):
        if metric_eval == "KS":
            score_min = (
                df.groupby(col_safra)
                .apply(lambda x: self.ks(x[target], x["prob"]) * 100)
                .min()
            )
        else:
            score_min = (
                df.groupby(col_safra)
                .apply(lambda x: metrics.roc_auc_score(x[target], x["prob"]))
                .min()
            )
        return score_min

    def get_metric_range(self, df, target, metric_eval, col_safra):
        if metric_eval == "KS":
            score_min = (
                df.groupby(col_safra)
                .apply(lambda x: self.ks(x[target], x["prob"]) * 100)
                .min()
            )
            score_max = (
                df.groupby(col_safra)
                .apply(lambda x: self.ks(x[target], x["prob"]) * 100)
                .max()
            )
        else:
            score_min = (
                df.groupby(col_safra)
                .apply(lambda x: metrics.roc_auc_score(x[target], x["prob"]))
                .min()
            )
            score_max = (
                df.groupby(col_safra)
                .apply(lambda x: metrics.roc_auc_score(x[target], x["prob"]))
                .max()
            )
        range_ = score_max - score_min
        return range_

    def get_metric(self, df, target, metric_eval):
        if metric_eval == "KS":
            score = self.ks(df[target], df["prob"]) * 100
        else:
            score = metrics.roc_auc_score(df[target], df["prob"])
        return score

    def decision(self, metric_train, metric_test, metric_otm, thr=5):
        # print(np.abs(metric_train - metric_test))
        return 0 if np.abs(metric_train - metric_test) > thr else metric_otm

    def generate_objective_function(self, x, y, target, features, categorical_features):
        def objective(
            trial,
            x=x,
            y=y,
            target=target,
            features=features,
            categorical_features=categorical_features,
        ):
            parameters = {
                "learning_rate": trial.suggest_loguniform("learning_rate", 0.01, 0.2),
                "n_estimators": trial.suggest_int("n_estimators", 100, 1000, 100),
                "num_leaves": trial.suggest_int("num_leaves", 6, 150, 1, log=True),
                "max_depth": trial.suggest_int("max_depth", 5, 10),
                "min_child_samples": trial.suggest_int("min_child_samples", 50, 500, 5),
                "min_child_weight": trial.suggest_loguniform(
                    "min_child_weight", 0.0001, 1000
                ),
                "boosting_type": trial.suggest_categorical("boosting_type", ["gbdt"]),
                "objective": trial.suggest_categorical("objective", ["binary"]),
                "colsample_bytree": trial.suggest_uniform("colsample_bytree", 0.4, 1.0),
                "subsample": trial.suggest_uniform("subsample", 0.5, 1.0),
                "min_split_gain": trial.suggest_loguniform("min_split_gain", 0.01, 0.1),
            }
            if self.eval_n_features:
                n_features = trial.suggest_int("n_features", 1, len(self.shap_imp_base))
                selected_features = self.shap_imp_base["var"][:n_features].to_list()
                trial.set_user_attr("selected_features", selected_features)
                features = [x for x in selected_features]
                categorical_features = [
                    x for x in self.categorical_features if x in selected_features
                ]

            train_metrics = np.zeros(5)
            test_metrics = np.zeros(5)

            kf = StratifiedKFold(shuffle=True, random_state=42)

            for i, (idx_train, idx_test) in enumerate(kf.split(x, y)):
                x_train, y_train = x.iloc[idx_train], y.iloc[idx_train]
                x_test, y_test = x.iloc[idx_test], y.iloc[idx_test]
                if len(categorical_features) > 0:
                    rc = RankCountVectorizer()
                    x_train[categorical_features] = x_train[
                        categorical_features
                    ].astype(str)
                    x_test[categorical_features] = x_test[categorical_features].astype(
                        str
                    )
                    x_train = rc.fit_transform(x_train, cols=categorical_features)
                    x_test = rc.transform(x_test, cols=categorical_features)

                model = self.train_model(parameters, x_train[features], y_train[target])

                y_pred_train = self.predict(model, x_train[features])
                y_pred_test = self.predict(model, x_test[features])
                x_train["prob"] = y_pred_train
                x_test["prob"] = y_pred_test

                if self.metric_method == "min":
                    train_metrics[i] = self.get_metric_min(
                        x_train, target, self.metric_eval, self.col_safra
                    )
                    test_metrics[i] = self.get_metric_min(
                        x_test, target, self.metric_eval, self.col_safra
                    )
                elif self.metric_method == "range":
                    train_metrics[i] = self.get_metric_range(
                        x_train, target, self.metric_eval, self.col_safra
                    )
                    test_metrics[i] = self.get_metric_range(
                        x_test, target, self.metric_eval, self.col_safra
                    )
                else:
                    train_metrics[i] = self.get_metric(
                        x_train, target, self.metric_eval
                    )
                    test_metrics[i] = self.get_metric(x_test, target, self.metric_eval)

            metrics = {
                "train_metrics": list(train_metrics),
                "test_metrics": list(test_metrics),
                "train_metric": np.mean(train_metrics),
                "test_metric": np.mean(test_metrics),
            }

            for key in metrics:
                trial.set_user_attr(key, metrics[key])

            metric_otm = np.mean(test_metrics) - np.std(test_metrics)
            value = self.decision(
                np.mean(train_metrics), np.mean(test_metrics), metric_otm, thr=self.thr
            )
            self.update_best_params(value, test_metrics)
            if self.save_in_txt:
                f = open(f"{self.log_file}.txt", "a")
                f.write(
                    f"{self.iterations};{parameters};{list(metrics['train_metrics'])};{list(metrics['test_metrics'])}\n"
                )
                f.close()
            return value

        return objective

    def create_log(self):
        time_ref = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
        self.log_file = f"resume_opt_{time_ref}"
        f = open(f"{self.log_file}.txt", "w")
        f = open(f"{self.log_file}.txt", "a")
        f.write(f"iter;parameters;train_metrics;test_metrics\n")
        f.close()

    def get_baseline_model(self, x, y, target, features, categorical_features):
        if len(categorical_features) > 0:
            rc = RankCountVectorizer()
            x[categorical_features] = x[categorical_features].astype(str)
            x = rc.fit_transform(x, cols=categorical_features)
        model = LGBMClassifier()
        model.fit(x[features], y)
        explainer = shap.TreeExplainer(model)
        shap_values = explainer.shap_values(x[features])
        shap_df = pd.DataFrame(np.abs(shap_values[1]), columns=features)
        shap_df = (
            pd.DataFrame(shap_df.mean(), columns=["impact"])
            .reset_index()
            .rename(columns={"index": "var"})
            .sort_values(by=["impact"], ascending=False)
        )
        self.shap_imp_base = shap_df
