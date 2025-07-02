from chicken.configuration import ModelEvaluationConfig, DataPreprocessingConfig
from chicken.components.model_evaluation import ModelEvaluation
from chicken.logger import logging
from chicken.exception import CustomException
import sys




STAGE_NAME = "Train and Evaluation stage"


class EvaluationPipeline:
    def __init__(self):
        pass

    def main(self):
        data_preprocessing_config = DataPreprocessingConfig
        model_evaluation_config = ModelEvaluationConfig
        evaluation = ModelEvaluation(data_preprocessing_config, model_evaluation_config)
        evaluation.start()



if __name__ == '__main__':
    try:
        logging.info(f"*******************")
        logging.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        obj = EvaluationPipeline()
        obj.main()
        logging.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logging.exception(e)
        raise CustomException(e, sys)
            