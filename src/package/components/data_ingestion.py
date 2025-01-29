from package.utils import create_dirs
from package.exception import CustomException
from package.logger import logging
from dataclasses import dataclass
from urllib.request import urlretrieve
from  zipfile import ZipFile
from tensorflow.data import Dataset # type: ignore
from package.entity import DataIngestionConfigEntity
import keras
import sys
import os



@dataclass
class DataIngestion:
    __config: DataIngestionConfigEntity

    def download(self, source_uri:str, zip_file_path:str)-> None:
        """Description: downloads the data zip file and saves locally

        Args:
            source_uri (str): uri for downloading
            zip_file_path (str): path to save file locally
        """
        try:
            create_dirs(self.__config.dir_path)
            logging.info("Downloading........")
            urlretrieve(source_uri, zip_file_path)
            logging.info("Download complete.")            
        except Exception as e:
            logging.error(e)
            CustomException(e, sys)
    
    def extract(self, zip_file_path:str, raw_data_dir:str)-> None:
        """Description: extracts the zip file into given path

        Args:
            zip_file_path (str): path of zip file needed to be extracted
            raw_data_dir (str): path of directory for extraction
        """
        try:
            create_dirs(raw_data_dir) # creating directory

            with ZipFile(zip_file_path, "r") as zip_ref:
                zip_ref.extractall(raw_data_dir)
                logging.info("zip extraction comleted.")
        except Exception as e:
            logging.error(e)
            raise CustomException(e, sys)
    

    def get_training_testing_splits(self, raw_data_dir:str)-> None:
        """Description: splits and save the data into training and testing.
            Condition: only for binary problem statement,
            path of data should be
            
            folder1-->folder_class_1,folder_class_2

        Args:
            raw_data_dir (str): Parent folder path of folder containing data
        """
        try:
            data_dir_name = os.listdir(raw_data_dir)[0] # data directory name
            data_dir = os.path.join(raw_data_dir, data_dir_name) # full path the data directory
            training_dataset, testing_dataset = keras.preprocessing.image_dataset_from_directory(
                data_dir,
                label_mode="binary",
                class_names=["Coccidiosis", "Healthy"],
                batch_size=None,
                image_size=(224, 224),
                seed=123,
                validation_split=0.3,
                subset="both",
            )

            training_dataset_dir_path = self.__config.training_data_dir
            testing_dataset_dir_path = self.__config.testing_data_dir

            create_dirs(training_dataset_dir_path) # creating directory
            create_dirs(testing_dataset_dir_path) # creating directory

            training_dataset.save(training_dataset_dir_path) # saving training_dataset
            testing_dataset.save(testing_dataset_dir_path) # saving testing_dataset

            logging.info("training_dataset and testing_dataset saved successfully")
        except Exception as e:
            logging.error(e)
            raise CustomException(e, sys)
        

    def get_train_val_splits(self, training_data_dir:str)-> None:
        """Description: splits and save the data into train and validation.

        Args:
            training_data_dir (str): path of training dataset for further split on train and validation 
        """
        try:
            training_dataset = Dataset.load(training_data_dir)

            train_dataset_size = int(0.8 * len(training_dataset))

            # 80% of training data will be used for training
            train_dataset = training_dataset.take(train_dataset_size)
            
            # 20% of training data will be used for validation
            val_dataset = training_dataset.skip(train_dataset_size)
            
            train_dataset_dir_path = self.__config.train_data_dir
            val_dataset_dir_path = self.__config.val_data_dir

            create_dirs(train_dataset_dir_path) # creating directory
            create_dirs(val_dataset_dir_path) # creating directory

            train_dataset.save(train_dataset_dir_path) # saving train_dataset
            val_dataset.save(val_dataset_dir_path) # saving val_dataset

            logging.info("train_dataset and val_dataset saved successfully")
        except Exception as e:
            logging.error(e)
            raise CustomException(e, sys)

