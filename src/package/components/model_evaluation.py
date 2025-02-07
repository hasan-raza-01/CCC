from package.entity import DataPreprocessingConfigEntity
from package.entity import ModelEvaluationConfigEntity
from package.components.model_trainer import ModelTrainer
from package.exception import CustomException
from keras.callbacks import EarlyStopping, TensorBoard # type: ignore
from package.utils import create_dirs
from urllib.request import urlparse
from dataclasses import dataclass
from package.logger import logging
from retrying import retry
from pathlib import Path
import mlflow, bentoml
import numpy as np
import keras_tuner
import dagshub
import sys
import os



@dataclass
class ModelEvaluation:
    __data_preprocessing_config: DataPreprocessingConfigEntity
    __model_evaluation_config: ModelEvaluationConfigEntity

    @retry(stop_max_attempt_number=2, wait_fixed=10000)
    def start(self):
        try:
            mt = ModelTrainer()
            build_model = mt.build_model
            logging.info("Model Evaluation Initiated")
            tuner = keras_tuner.RandomSearch(
            build_model,
            objective='val_loss',
            max_trials=1 # 20 default
            )

            # getting path for train, val and test data
            X_train_path = os.path.join(self.__data_preprocessing_config.train_data_dir, "input_data.npy")
            y_train_path = os.path.join(self.__data_preprocessing_config.train_data_dir, "labels.npy")
            X_val_path = os.path.join(self.__data_preprocessing_config.val_data_dir, "input_data.npy")
            y_val_path = os.path.join(self.__data_preprocessing_config.val_data_dir, "labels.npy")
            X_test_path = os.path.join(self.__data_preprocessing_config.test_data_dir, "input_data.npy")
            y_test_path = os.path.join(self.__data_preprocessing_config.test_data_dir, "labels.npy")

            # loading data from specified path
            X_train = np.load(Path(X_train_path))
            y_train = np.load(Path(y_train_path))
            X_val = np.load(Path(X_val_path))
            y_val = np.load(Path(y_val_path))
            X_test = np.load(Path(X_test_path))
            y_test = np.load(Path(y_test_path))

            create_dirs(self.__model_evaluation_config.tensorboard_dir) # creating tensorboard_dir
            
            early_stoping = EarlyStopping(patience=10, restore_best_weights=True)
            tensorboard = TensorBoard(self.__model_evaluation_config.tensorboard_dir, histogram_freq=1)

            tuner.search(X_train, y_train, 
                        epochs=1, # 50 default
                        validation_data=(X_val, y_val),
                        callbacks = [early_stoping, tensorboard]
                        )

            # connecting with dagshub repository
            dagshub.init(repo_owner='hasan-raza-01', repo_name='CCC', mlflow=True)
            
            with mlflow.start_run():
                best_model = tuner.get_best_models()[0]
                test_loss, test_accuracy = best_model.evaluate(X_test, y_test)
                best_hps = tuner.get_best_hyperparameters(num_trials=1)[0]
                
                if test_accuracy < 0.6:
                    model = tuner.hypermodel.build(best_hps)
                    history = model.fit(X_train, y_train, epochs=1, # 2 default
                                        validation_split=0.2)
                    
                    val_acc_per_epoch = history.history['val_accuracy']
                    best_epoch = val_acc_per_epoch.index(max(val_acc_per_epoch)) + 1

                    best_model.fit(
                        X_train, y_train,
                        epochs=1, # best_epoch defalut
                        validation_split=0.2,
                        callbacks = [early_stoping, tensorboard]
                    )

                    test_loss, test_accuracy = best_model.evaluate(X_test, y_test)
                
                mlflow.log_metric("loss", test_loss)
                mlflow.log_metric("accuracy", test_accuracy)
                mlflow.log_params(best_hps.values)

                infer_signature = mlflow.models.infer_signature(X_train, best_model.predict(X_train))
                
                uri = "https://dagshub.com/hasan-raza-01/CCC.mlflow/"
                mlflow.set_tracking_uri(uri)
                
                tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme

                if tracking_url_type_store != "file":
                    mlflow.keras.log_model(best_model, "VGG16",
                                           registered_model_name="VGG16", 
                                           signature=infer_signature
                                    )
                else:
                    mlflow.keras.log_model(best_model, "VGG16", 
                                           signature=infer_signature
                                    )

                # saving model locally
                bentoml.keras.save_model("VGG16", best_model)

                # saving model locally
                best_model.save("artifacts/model/model.h5")

            logging.info("Model Evaluation completed")
        except Exception as e:
            logging.error(e)
            raise CustomException(e, sys)

