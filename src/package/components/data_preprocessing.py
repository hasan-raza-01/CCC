from package.exception import CustomException
from package.logger import logging
from package.utils import create_dirs
from keras.applications.vgg16 import preprocess_input # type: ignore
from tensorflow.image import resize # type: ignore
from tensorflow.data import Dataset # type: ignore
from package.entity import DataIngestionConfigEntity, DataPreprocessingConfigEntity
from dataclasses import dataclass
import numpy as np
import os
import sys



@dataclass
class DataPreprocessing:
    __data_ingestion_config: DataIngestionConfigEntity
    __data_preprocessing_config: DataPreprocessingConfigEntity

    def resize_and_scale(self, X):
        """Description: resize image(X) in 224X224 for VGG16

        Args:
            X (image_data): input image for model
        """
        try:
            X = resize(X, (224, 224))/255 # resizing and scaling
            return X
        except Exception as e:
            logging.error(e)
            raise CustomException(e, sys)
    

    def preprocess(self)-> None:
        try:
            inputs = {
                self.__data_ingestion_config.train_data_dir:self.__data_preprocessing_config.train_data_dir, 
                self.__data_ingestion_config.val_data_dir:self.__data_preprocessing_config.val_data_dir, 
                self.__data_ingestion_config.testing_data_dir:self.__data_preprocessing_config.test_data_dir 
            }
            logging.info("Data Preprocessing initiated")
            create_dirs(self.__data_preprocessing_config.dir_path) # creating main directory
            
            for read_path, save_path in inputs.items():

                read_path = os.path.join(read_path)
                save_path = os.path.join(save_path)
                create_dirs(save_path) # creating saving directory where transformed data will be stored

                data = Dataset.load(read_path) # loading data

                data = data.map(lambda X, y: (self.resize_and_scale(X), y)) # resizing and scaling

                data = data.batch(20, drop_remainder=True) # droping incomplete batch

                data = data.map(lambda X, y: (preprocess_input(X), y)) # converting into input format of VGG16

                # extracting image, label
                X = []
                y = []
                for image_data, label_data in data:
                    X.append(image_data.numpy())
                    y.append(label_data.numpy())

                # creating proper numpy array
                X = np.concatenate(X, axis=0) 
                y = np.concatenate(y, axis=0)

                # saving data
                np.save(os.path.join(save_path, "input_data.npy"), X)
                np.save(os.path.join(save_path, "labels.npy"), y)
            
            logging.info("Data Preprocessing completed")
        except Exception as e:
            logging.error(e)
            raise CustomException(e, sys)

