import numpy as np
from tensorflow.keras.preprocessing import image # type: ignore
from tensorflow.keras.models import load_model # type: ignore
import bentoml, mlflow



class PredictionPipeline:
    def __init__(self,filename):
        self.filename =filename


    
    def predict(self):

        imagename = self.filename
        test_image = image.load_img(imagename, target_size = (224,224))
        test_image = image.img_to_array(test_image)
        test_image = np.expand_dims(test_image, axis = 0)

        # load model
        try:
            model_uri = mlflow.get_artifact_uri("models/VGG16")
            print(f"mlflow model uri: {model_uri}")
            model = mlflow.tensorflow.load_model(model_uri)
            result = np.argmax(model.predict.run(test_image), axis=1)
        
        except Exception as e:
            try:
                print(f"""

    facing error when loading model from mlflow 1st try, mssg: {e}

    """) 
                model_uri = f"models:/VGG16@latest"
                print(f"mlflow model uri: {model_uri}")
                model = mlflow.tensorflow.load_model(model_uri)
                result = np.argmax(model.predict.run(test_image), axis=1)

            except Exception as e:
                print(f"""

    facing error when loading model from mlflow 2nd try, mssg: {e}

    """) 
                try:
                    model = bentoml.keras.load_model("VGG16:latest")
                    result = np.argmax(model.predict(test_image), axis=1)

                except Exception as e:
                    print(f"""

    facing error when loading model from bentoml, mssg: {e}

    """)            
                    try:
                        model = load_model("artifacts/model/model.h5")
                        result = np.argmax(model.predict(test_image), axis=1)

                    except Exception as e:
                        print(f"""

    facing error when loading model from bentoml, mssg: {e}

    """)

        print(result)

        if result[0] == 1:
            prediction = 'Healthy'
            return [{ "image" : prediction}]
        else:
            prediction = 'Coccidiosis'
            return [{ "image" : prediction}]
        
