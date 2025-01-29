from package.exception import CustomException
from package.logger import logging
from package.configuration import DataIngestionConfig
from package.components.data_ingestion import DataIngestion
import sys



STAGE_NAME = "Data Ingestion stage"

class DataIngestionTrainingPipeline:
    def __init__(self):
        pass

    def main(self):
        CONFIG = DataIngestionConfig()
        data_ingestion_config = CONFIG
        data_ingestion = DataIngestion(data_ingestion_config)
        logging.info("Data ingestion initiated")
        data_ingestion.download(CONFIG.source_uri, CONFIG.zip_file_path)
        data_ingestion.extract(CONFIG.zip_file_path,CONFIG.raw_data_dir)
        data_ingestion.get_training_testing_splits(CONFIG.raw_data_dir)
        data_ingestion.get_train_val_splits(CONFIG.training_data_dir)
        logging.info("Data ingestion completed")




if __name__ == '__main__':
    try:
        logging.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        obj = DataIngestionTrainingPipeline()
        obj.main()
        logging.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logging.exception(e)
        raise CustomException(e, sys)

