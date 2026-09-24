import sys
import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import RobustScaler , FuncTransformer
from sklearn.pipeline import Pipeline

from src.constant import *
from src.exception import CustomException # type: ignore
from src.logger import logging # type: ignore
from src.utils.main_util import MainUtil
from dataclasses import dataclass

@dataclass
class DataTransformationConfig:
    artifact_dir = os.path.join(artifact_folder) # type: ignore
    data_transformation_dir = os.path.join(artifact_dir, "data_transformation")
    transformed_train_file_path = os.path.join(artifact_dir, "train.npy")
    transformed_test_file_path = os.path.join(artifact_dir, "test.npy")
    preprocessor_object_file_path = os.path.join(artifact_dir, "preprocessor.pkl")

    class DataTransformation:
        def __init__(self, feature_store_file_path) -> None:
            self.feature_store_file_path = feature_store_file_path
            self.data_transformation_config = DataTransformationConfig()
            self.util = MainUtil()


            @staticmethod
            def get_data(feature_store_file_path:str)-> pd.DataFrame:
                try:
                    data = pd.read_csv(feature_store_file_path)
                    data.rename(columns={"good/bad": TARGET_COLUMN}, inplace=True)

                    return data
                except Exception as e:
                    raise CustomException(e, sys) 

                try:
                    imputer_step = SimpleImputer(strategy="constant", fill_value=0)

                    scaler_step = ('scaler',RobustScaler())

                    preprocessor = Pipeline(steps=[('imputer', imputer_step), scaler_step])

                    return preprocessor
                except Exception as e:
                    raise CustomException(e, sys)

                def initiate_data_transformation(self):
                    logging.info(f"Entered the initiate_data_transformation method of DataTransformation class")

                    try:
                        dataframe = self.get_data(feature_store_file_path=self.feature_store_file_path)
                        


                        X = dataframe.drop(columns=[TARGET_COLUMN], axis=1)
                        y = data[TARGET_COLUMN]

                        preprocessor = self.get_data_transformer_object()

                        X_train_scaled = preprocessor.fit_transform(X_train)
                        X_test_scaled = preprocessor.transform(X_test)
                        os.makedirs(os.path.dirname(preprocessor.path), exist_ok=True)
                        self.utils.save_object(file_path=preprocessor.path, obj=preprocessor)

                        train_arr = np.c_[X_train_scaled, np.array(y_train)]
                        test_arr = np.c_[X_test_scaled, np.array(y_test)]
                        return (train_arr, test_arr, preprocessor_path)
                    except Exception as e:
                        raise CustomException(e, sys)
                     