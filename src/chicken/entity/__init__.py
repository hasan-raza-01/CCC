from dataclasses import dataclass
from pathlib import Path


@dataclass
class DataIngestionConfigEntity:
    dir_path: Path
    source_uri: str
    zip_file_path: Path
    raw_data_dir: Path
    training_data_dir: Path
    testing_data_dir: Path
    train_data_dir: Path
    val_data_dir: Path


@dataclass
class DataPreprocessingConfigEntity:
    dir_path: Path
    train_data_dir: Path
    val_data_dir: Path
    test_data_dir: Path


@dataclass
class ModelEvaluationConfigEntity:
    tensorboard_dir: Path

