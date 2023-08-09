import copy
import json
import logging
from sklearn.metrics import f1_score

from kortical import api
from kortical.api.data import Data
from kortical.api.model import Model
from kortical.api.project import Project
from kortical.api.environment import Environment
from kortical.app import get_app_config

from module_placeholder.workflows import common, business_case


app_config = get_app_config(format='yaml')
model_name = app_config['model_name']
target = app_config['target']
logger = logging.getLogger(__name__)


# Status messages
UPLOADING_DATA = "Uploading train data to Kortical"
TRAINING_MODEL = "Training models"
MODEL_COMPARISON = "Comparing challenger vs champion model"
PUBLISHED = "Workflow complete, model was published."
NOT_PUBLISHED = "Workflow complete, model was not published."


# Celery task status
WORKFLOW_PROGRESS = {
    "status": None,
    "challenger_score": None,
    "champion_score": None
}


def train(df_train, df_test, celery_task):
    api.init()
    workflow_progress = copy.deepcopy(WORKFLOW_PROGRESS)

    # Do custom processing
    common.preprocessing(df_train)

    # Select model
    model = Model.select(model_name, delete_unpublished_versions=False, stop_train=True)

    # Upload train data
    workflow_progress["status"] = UPLOADING_DATA
    celery_task.update_state(state=json.dumps(workflow_progress))
    train_data = Data.upload_df(df_train, name=model_name)
    train_data.set_targets(target)

    # Train + return best version
    workflow_progress["status"] = TRAINING_MODEL
    celery_task.update_state(state=json.dumps(workflow_progress))
    challenger_model_version = model.train_model(
        train_data=train_data,
        model_code=common.model_code,
        number_of_train_workers=app_config.get('number_of_train_workers', 3),
        # Remove this minutes limitation to run in production and produce better models
        max_minutes_to_train=2,
        max_models_with_no_score_change=app_config.get('max_models_with_no_score_change', 50)
    )

    workflow_progress["status"] = MODEL_COMPARISON
    celery_task.update_state(state=json.dumps(workflow_progress))

    # Create a challenger model instance
    model_development = model.get_environment()
    challenger_model_instance = model_development.create_component_instance(challenger_model_version.id, wait_for_ready=True)

    # Get the champion model instance
    project = Project.get_selected_project()
    environment = Environment.get_selected_environment(project)
    champion_model_instance = environment.get_component_instance(model.name)
    if champion_model_instance is None:
        logger.info(f"Model instance does not exist in project [{project.name}] environment [{environment.name}]. Saving and deploying newly trained model version...")
        model.set_default_version(challenger_model_version, wait_for_ready=False)
        environment.create_component_instance(challenger_model_version.id)
        workflow_progress["status"] = PUBLISHED
        celery_task.update_state(state=json.dumps(workflow_progress))
        return True

    # Compare the performance of the challenger vs. champion model (i.e new vs. existing)
    challenger_predictions = challenger_model_instance.predict(df_test)
    challenger_score = f1_score(challenger_predictions[target], challenger_predictions[f"predicted_{target}"], average='weighted')
    workflow_progress["challenger_score"] = challenger_score
    celery_task.update_state(state=json.dumps(workflow_progress))

    champion_predictions = champion_model_instance.predict(df_test)
    champion_score = f1_score(champion_predictions[target], champion_predictions[f"predicted_{target}"], average='weighted')
    workflow_progress["champion_score"] = champion_score
    celery_task.update_state(state=json.dumps(workflow_progress))

    logger.info(f"New model score: [{challenger_score}], existing model score: [{champion_score}]")

    # Deploy the new model
    if business_case.should_publish(challenger_score=challenger_score, champion_score=champion_score):
        logger.info(f"Setting default version [{challenger_model_version}] for model [{model}]...")
        model.set_default_version(challenger_model_version, wait_for_ready=False)
        logger.info(f"Deploying version [{challenger_model_version}] to environment [{environment}]...")
        environment.create_component_instance(challenger_model_version.id)
        workflow_progress["status"] = PUBLISHED
        celery_task.update_state(state=json.dumps(workflow_progress))
        return True
    else:
        logger.info(f"Not publishing, retrained version [{model.default_version.id}] has an inferior score to the existing version.")
        workflow_progress["status"] = NOT_PUBLISHED
        celery_task.update_state(state=json.dumps(workflow_progress))
        return False
