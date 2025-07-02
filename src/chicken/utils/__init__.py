from chicken.exception import CustomException
from chicken.logger import logging
from box import ConfigBox
from pathlib import Path
import pickle
import yaml
import sys
import os
import base64



def read_yaml(file_path:str)-> ConfigBox:
    """Reads yaml file only

    Args:
        file_path (Path): path of .yaml file having content for extraction

    Returns:
        (Path)
        ConfigBox: Content of .yaml file, like key.value 
    """
    try:
        with open(Path(file_path), "rt") as file_obj:
            return ConfigBox(yaml.safe_load(file_obj))
    except Exception as e:
        logging.error(e)
        raise CustomException(e, sys)


def create_dirs(path:str)-> None:
    """create directories on given argument

    Args:
        path (str): path for directory creation
    """
    try:
        path = Path(path)
        os.makedirs(path, exist_ok=True)
        logging.info(f"path {path} created")
    except Exception as e:
        logging.error(e)
        raise CustomException(e, sys)


def save_object(path:str, object:object)-> None:
    """saves the object into .h5 file

    Args:
        path (str): path to save the object
        object (object): object to be saved
    """
    try:
        with open(Path(path), "wb") as file_obj:
            pickle.dump(object, file_obj)
            logging.info("object saved successfully")
    except Exception as e:
        logging.error(e)
        raise CustomException(e, sys)


def load_object(path:str)-> object:
    """load the object present at path with pickle and return

    Args:
        path (str): path for the object

    Returns:
        object: object at path will be returned
    """
    try:
        with open(Path(path), "rb") as file_obj:
            obj = pickle.load(file_obj)
            logging.info("object successfully loaded")
            return obj
    except Exception as e:
        logging.error(e)
        raise CustomException(e, sys)
    

def decodeImage(imgstring, fileName):
    imgdata = base64.b64decode(imgstring)
    with open(fileName, 'wb') as f:
        f.write(imgdata)
        f.close()
