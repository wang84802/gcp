import os 
import sys
import jsonlines
from google.cloud import aiplatform, storage
from google.protobuf import json_format
from datetime import datetime

# 環境設置
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="./chris-project-364416-2cbb3d0fd013.json"

REGION = 'us-central1'
PROJECT_ID = 'chris-project-364416'
bucket_name = "chris_bucket_5"

def create_bucket(bucket_name):
    os.system("gsutil mb -l us-central1 gs://" + bucket_name)

def upload_csv(file_path, bucket_name):
    os.system("gsutil cp " + file_path + " gs://" + bucket_name)

def create_dataset(project, location, file_name):
    # initiate project
    aiplatform.init(project=PROJECT_ID, location=REGION)

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    src_uri = "gs://chris_bucket_4/1.csv"
    display_name = f"dataset_iAWE_1_{timestamp}"

    dataset = aiplatform.TabularDataset.create(
        display_name=display_name,
        gcs_source=src_uri
    )

def get_model_sample(project: str, location: str, model_name: str):
    # initiate project
    aiplatform.init(project=project, location=location)

    model = aiplatform.Model(model_name=model_name)

    print(model.display_name)
    print(model.resource_name)
    print(model)

def create_training_model(
    project: str,
    dataset_id: str,
    location: str = "us-central1",
    # model_display_name: str = None,
    target_column: str = None,
    training_fraction_split: float = 0.8,
    validation_fraction_split: float = 0.1,
    test_fraction_split: float = 0.1,
    # budget_milli_node_hours: int = 8000,
    # disable_early_stopping: bool = False,
    sync: bool = True,
):
    aiplatform.init(project=project, location=location)

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    training_job_display_name = f"tabular-training-job-{timestamp}"

    tabular_classification_job = aiplatform.AutoMLTabularTrainingJob(
        display_name=training_job_display_name, optimization_prediction_type="regression"
    )

    my_tabular_dataset = aiplatform.TabularDataset(dataset_name=dataset_id)

    model = tabular_classification_job.run(
        dataset=my_tabular_dataset,
        target_column=target_column,
        training_fraction_split=training_fraction_split,
        validation_fraction_split=validation_fraction_split,
        test_fraction_split=test_fraction_split,
        # budget_milli_node_hours=budget_milli_node_hours,
        # model_display_name=model_display_name,
        # disable_early_stopping=disable_early_stopping,
        sync=sync,
    )

    model.wait()

    print(model.display_name)
    print(model.resource_name)
    print(model.uri)
    return model

def get_model_version_info_sample(
    model_id: str, version_id: str, project: str, location: str
):
    """
    Get model version info.
    Args:
        model_id: The ID of the model.
        version_id: The version ID of the model version.
        project: The project ID.
        location: The region name.
    Returns:
        VersionInfo resource.
    """

    # Initialize the client.
    aiplatform.init(project=project, location=location)

    # Initialize the Model Registry resource with the ID 'model_id'.The parent_name of Model resource can be also
    # 'projects/<your-project-id>/locations/<your-region>/models/<your-model-id>'
    model_registry = aiplatform.models.ModelRegistry(model=model_id)

    # Get model version info with the version 'version_id'.
    model_version_info = model_registry.get_version_info(version=version_id)

    print(model_version_info)
    return model_version_info


create_bucket("chris_bucket_5")

upload_csv("data/1.csv", "chris_bucket_5")

create_dataset(PROJECT_ID, REGION, '1.csv')

create_training_model(project=PROJECT_ID, dataset_id='4025182326915858432', target_column='W')

get_model_sample(PROJECT_ID, REGION, 'tabular-training-job-20221028143443')

get_model_version_info_sample(model_id="tabular-training-job-20221028143443", version_id="1", project=PROJECT_ID, location=REGION)