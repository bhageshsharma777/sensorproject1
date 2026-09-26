import sys
from dataclasses import dataclass
import os
from typing import Dict, Any

import numpy as np
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.svm import SVC
from xgboost import XGBClassifier

from src.constant import *
from src.exception import CustomException
from src.logger import logging
from src.utils.main_util import MainUtils


@dataclass
class ModelTrainerConfig:
    artifact_dir = os.path.join(artifact_folder)
    trained_model_path = os.path.join(artifact_folder, "model.pkl")
    model_config_file_path = os.path.join(artifact_folder, "model.yaml")
    expected_accuracy: float = 0.45


class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()
        self.util = MainUtils()

        self.models = {
            "RandomForest": RandomForestClassifier(),
            "XGBClassifier": XGBClassifier(),
            "GradientBoosting": GradientBoostingClassifier(),
            "SVC": SVC(),
        }

    def evaluate_models(self, X: np.ndarray, y: np.ndarray, models: Dict[str, Any]):
        try:
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            report: dict = {}

            for model_name, model in models.items():
                model.fit(X_train, y_train)

                y_train_pred = model.predict(X_train)
                y_test_pred = model.predict(X_test)

                train_model_score = accuracy_score(y_train, y_train_pred)
                test_model_score = accuracy_score(y_test, y_test_pred)

                report[model_name] = test_model_score

            return report
        except Exception as e:
            raise CustomException(e, sys) from e

    def get_best_model(self, X: np.ndarray, y: np.ndarray):
        try:
            model_report = self.evaluate_models(X, y, self.models)
            print(model_report)
            best_model_score = max(model_report.values())
            best_model_name = max(model_report, key=model_report.get)
            best_model_object = self.models[best_model_name]

            return best_model_name, best_model_object, best_model_score
        except Exception as e:
            raise CustomException(e, sys) from e

    def finetune_best_model(self, best_model_object, best_model_name, X_train, y_train):
        try:
            model_param_grid = self.util.read_yaml_file(self.model_trainer_config.model_config_file_path)

            if best_model_name == "RandomForest":
                param_grid = model_param_grid.get("RandomForest", {})
            elif best_model_name == "XGBClassifier":
                param_grid = model_param_grid.get("XGBClassifier", {})
            elif best_model_name == "GradientBoosting":
                param_grid = model_param_grid.get("GradientBoosting", {})
            elif best_model_name == "SVC":
                param_grid = model_param_grid.get("SVC", {})
            else:
                param_grid = {}

            if not param_grid:
                return best_model_object

            grid_search = GridSearchCV(
                best_model_object,
                param_grid=param_grid,
                cv=5,
                n_jobs=1,
                verbose=1,
            )

            grid_search.fit(X_train, y_train)
            best_params = grid_search.best_params_
            print("best params are", best_params)
            return grid_search.best_estimator_
        except Exception as e:
            raise CustomException(e, sys) from e

    def initiate_model_trainer(self, train_array, test_array):
        try:
            logging.info("splitting training and testing input and target feature")

            x_train, y_train, x_test, y_test = (
                train_array[:, :-1],
                train_array[:, -1],
                test_array[:, :-1],
                test_array[:, -1],
            )
            best_model_name, best_model_object, best_model_score = self.get_best_model(
                x_train, y_train
            )
            if best_model_score < self.model_trainer_config.expected_accuracy:
                raise Exception("No model met the expected accuracy threshold")

            finetuned_model = self.finetune_best_model(
                best_model_object, best_model_name, x_train, y_train
            )
            test_model_score = accuracy_score(y_test, finetuned_model.predict(x_test))
            logging.info("Best model: %s, test accuracy: %s", best_model_name, test_model_score)
            return finetuned_model
        except Exception as e:
            raise CustomException(e, sys) from e

                

