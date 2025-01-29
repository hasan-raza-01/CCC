from package.configuration import DataIngestionConfig, DataPreprocessingConfig
from package.components.data_preprocessing import DataPreprocessing
from package.logger import logging
from package.exception import CustomException
import sys


STAGE_NAME = "Data Preprocessing stage"

class DataPreprocessingTrainingPipeline:
    def __init__(self):
        pass

    def main(self):
        data_ingestion_config = DataIngestionConfig()
        data_preprocessing_config = DataPreprocessingConfig()
        data_preprocessing = DataPreprocessing(data_ingestion_config, data_preprocessing_config)
        data_preprocessing.preprocess()





if __name__ == '__main__':
    try:
        logging.info(f"*******************")
        logging.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        obj = DataPreprocessingTrainingPipeline()
        obj.main()
        logging.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logging.exception(e)
        raise CustomException(e, sys)


