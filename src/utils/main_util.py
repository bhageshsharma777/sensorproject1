import sys
from typing import Dict , Tuple
import os
import pandas as pd
import pickle
import yaml
import boto3

from src.constant import *
from src.exception import CustomException
from src.logger import logging

class MainUtil:
    def __init__(self) -> None:
        pass

    @staticmethod
    def read_yaml_file(file_path: str) -> Dict:
        try:
            with open(file_path, 'rb') as yaml_file:
                return yaml.safe_load(yaml_file)
        except Exception as e:
            raise CustomException(e, sys) from e

    @staticmethod
    def read_schema_config_file() -> Dict:
        try:
            schema_config = MainUtil.read_yaml_file(os.path.join("config", "schema.yaml"))
            return schema_config
        except Exception as e:
            raise CustomException(e, sys) from e
@staticmethod
def save_object(file_path: str, obj: object) -> None:
        logging.info(f"Entered the save_object method of MainUtil class")

        try:
            with open(file_path, "wb") as file_obj:
                pickle.dump(obj, file_obj)
                logging.info(f"Entered the save_object method of MainUtil class")
        except Exception as e:
            raise CustomException(e, sys) from e
@staticmethod
def load_object(file_path: str) -> object:
    logging.info(f"Entered the load_object method of MainUtil class")
   
    try:
        with open(file_path, "rb") as file_obj:
            return pickle.load(file_obj)
        logging.info(f"Entered the load_object method of MainUtil class")
        return obj
    except Exception as e:
        raise CustomException(e, sys) from e