# CCC: AI‑Powered Chicken Coccidiosis Detection Chatbot

An end-to-end, AI-driven pipeline for automated detection and classification of chicken coccidiosis from images. By leveraging a modular training workflow, semantic image processing, and a real‑time Flask web interface, this system empowers poultry farmers and veterinarians with rapid, reliable diagnostic insights—anytime, anywhere.

---

## Here’s a preview of the app’s user interface:
![UI Screenshot](./screenshots/ui-preview.png)

---

## 📂 Repository Structure 
``` 
.
├── .dvc/                      # DVC configuration & cache for data version control
├── .github/
│   └── workflows/             # CI/CD pipeline workflows for automated deployment
├── config/
│   └── config.yaml            # Project configuration: artifact paths, model settings, training parameters
├── notebook/
│   └── trail.ipynb            # Experimental trials and prototyping
├── screenshots/               # Project screenshots and demo images
├── src/
│   └── chicken/               # Main package source code
│       ├── __init__.py
│       ├── cloud/
│       │   └── __init__.py    # Cloud storage operations (S3, GCS)
│       ├── components/        # Core ML pipeline components
│       │   ├── __init__.py
│       │   ├── data_ingestion.py       # Downloads and extracts chicken disease dataset
│       │   ├── data_preprocessing.py   # Prepares images: resizing, normalization, augmentation
│       │   ├── model_trainer.py        # Trains CNN model for disease classification
│       │   └── model_evaluation.py     # Evaluates model: accuracy, loss, confusion matrix
│       ├── configuration/
│       │   └── __init__.py    # Configuration manager: reads config.yaml, creates entity objects
│       ├── constants/
│       │   └── __init__.py    # Project constants: file paths, class names, environment variables
│       ├── entity/
│       │   └── __init__.py    # Dataclass entities: artifact and configuration objects
│       ├── exception/
│       │   └── __init__.py    # Custom exception handling with detailed error messages
│       ├── logger/
│       │   └── __init__.py    # Structured logging setup with timestamps
│       ├── pipeline/          # Orchestration layer for training and prediction pipelines
│       │   ├── __init__.py
│       │   ├── stage_01_data_ingestion.py      # Orchestrates data ingestion component
│       │   ├── stage_02_data_preprocessing.py  # Orchestrates data preprocessing component
│       │   ├── stage_03_train_and_eval.py      # Orchestrates training and evaluation components
│       │   └── prediction_pipeline/
│       │       └── __init__.py    # Prediction pipeline: loads model and classifies chicken images
│       └── utils/
│           └── __init__.py    # Utility functions: YAML I/O, image operations, common helpers
├── templates/
│   └── index.html             # Web interface for image upload and disease classification
├── .dockerignore              # Excludes unnecessary files from Docker image build
├── .dvcignore                 # Files ignored by DVC version control
├── .gitignore                 # Git exclusions: virtual environments, artifacts, model weights
├── Dockerfile                 # Container image for production deployment
├── README.md                  # Project documentation and setup instructions
├── app.py                     # Flask application: /predict endpoint for disease classification
├── dvc.lock                   # DVC lock file: ensures reproducibility with artifact hashes
├── dvc.yaml                   # DVC pipeline definition: stages, dependencies, and outputs
├── inputImage.jpg             # Sample input image for testing
├── main.py                    # Training pipeline orchestrator: runs all 3 stages via DVC
├── requirements.txt           # Python dependencies: TensorFlow/PyTorch, Flask, DVC
└── setup.py                   # Package installer: configures package for pip installation
```

## 🔧 Core Workflow

1. **Data Ingestion**  
   Managed via DVC, raw image datasets (microscopic slides, fecal smears) are downloaded, extracted, and split into training, validation, and test sets using `stage_01_data_ingestion.py`.

2. **Data Preprocessing**  
   Normalizes, augments, and transforms raw images into model-ready tensors within `stage_02_data_preprocessing.py`, ensuring robust performance under varied lighting and sample conditions.

3. **Model Training & Evaluation**  
   Trains a convolutional neural network using `stage_03_train_and_eval.py`, logs metrics (accuracy, precision, recall), and produces evaluation reports and saved model artifacts.

4. **Prediction Pipeline**  
   Loads the trained model in `chicken.pipeline.prediction_pipeline.PredictionPipeline`, decodes base64‑encoded uploads, and outputs classification results (e.g., “Infected” vs. “Healthy”).

5. **Real‑Time Flask API & UI**  
   - **Flask Backend** (`app.py`, `main.py`): Exposes `/predict`, `/train`, and `/` (UI) endpoints.  
   - **Templates** (`templates/index.html`): User-friendly upload interface.  
   - CORS‑enabled for integration with third‑party frontends or mobile apps.

---

## ✅ Key Capabilities

- **Image‑Grounded Diagnosis**  
  Delivers classification grounded in real microscopic images, pinpointing coccidial infections with high accuracy.  
- **Modular, Scalable Architecture**  
  Decoupled ingestion, preprocessing, training, and inference layers make extension and maintenance straightforward.  
- **Production‑Ready Best Practices**  
  - **DVC** for data and model versioning  
  - **Structured Logging** for pipeline transparency (`chicken.logger`)  
  - **Custom Exceptions** (`chicken.exception`) for robust error handling  
- **Containerized Deployment**  
  Dockerfile and `.dockerignore` ensure consistent environments and rapid scaling.  
- **Extensible ML Stack**  
  Swap in alternative model architectures or augment preprocessing steps with minimal code changes.

---

## 🐔 Disease Information

Chicken coccidiosis is a disease caused by a microscopic parasite that damages the intestines of chickens. It can lead to malnutrition, dehydration, and blood loss, and can be fatal.

### Symptoms  
- Diarrhea  
- Blood or mucus in feces  
- Depression, ruffled feathers  
- Pale skin, weight loss  

### Transmission  
- Oral–fecal route via infective oocysts in droppings  
- Contaminated litter, equipment, clothing, dust, or insects  

### Control & Prevention  
- Vaccination & preventative medication  
- Good management practices: litter hygiene, biosecurity  
- Disinfectants: steam cleaning, boiling water, 10% ammonia solution  
- Healthy birds develop immunity over time  

---

## 🚀 Deployment & CI/CD

- **GitHub Actions**  
  Automated DVC pulls, linting, testing, and Docker builds in `.github/workflows/`.
- **DVC**  
  Tracks and version‑controls datasets and model artifacts (`.dvc`, `dvc.yaml`, `dvc.lock`).
- **Docker**  
  Dockerfile Builds a slim‑based Python 3.11 image, installs dependencies, and sets `uv run app.py` as the entrypoint.
- **Azure Container Registry (ACR)**  
  Securely stores and manages your Docker images in Azure.
- **Azure Web App for Containers**  
  Deploys container images directly from ACR, offering auto‑scaling, built‑in load balancing, and fully managed hosting.

---

## Required Environment Variables
 ```bash
 DAGSHUB_USER_TOKEN=""
 ```

---

## 🏃 Running Locally

1. **Clone the repo**  
    ```bash
    git clone https://github.com/hasan-raza-01/CCC.git
    cd CCC
    ```
2. **Install dependencies**
   ```bash
   pip install --upgrade pip uv
   uv venv 
   .venv\scripts\activate
   uv pip install -e .
   ```
3. **Train the model**
    - ***Option A: Run full pipeline***
    ```
    uv run main.py
    ```
    - ***Option B: Trigger via Flask endpoint or navigate to the endpoint***
    #### only run when app is up or it will throws error
    ```bash 
    curl http://localhost:8080/train
    ```
4. **Start the API & UI**
    - ***Run Locally***
    ```bash 
    uv run app.py
    ```
    - ***Run Using Docker***
    ```bash 
    docker build -t ccc-detector:latest .
    docker run -p 8080:8080 ccc-detector:latest
    ```
5. **Interact via browser** 
    - Navigate to http://localhost:8080/ to upload images and view predictions.
