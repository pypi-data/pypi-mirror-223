from celery.result import AsyncResult
import logging

from kortical import api
from kortical.app import get_app_config

from module_placeholder.celery import celery
from module_placeholder.authentication import safe_api_call
from module_placeholder.bigquery.bigquery import create_dataframes_from_bigquery
from module_placeholder.workflows import train

logger = logging.getLogger(__name__)

app_config = get_app_config(format='yaml')
model_name = app_config['model_name']
api.init()

NO_ONGOING_TRAINING = "NO ONGOING TRAINING"
COLLECTING_DATA = "COLLECTING DATA"
TRAINING_MODEL = "TRAINING MODEL"
PUBLISHED = "PUBLISHED"
NON_PUBLISHED = "NON PUBLISHED"


# run task in celery worker
@celery.task(bind=True, ignore_result=True)
def train_workflow(self):
    self.update_state(state=COLLECTING_DATA)
    df_train, df_test = create_dataframes_from_bigquery()

    self.update_state(state=TRAINING_MODEL)
    model_published = train.train(df_train, df_test, self)

    self.update_state(state=PUBLISHED if model_published else NON_PUBLISHED)


def register_routes(app):
    @app.route('/train', methods=['post'])
    @safe_api_call
    def post_train():
        model = api.model.Model.create_or_select(model_name)
        if model.train_status()['is_training'] is True:
            return {'error': 'Model is already training.'}

        # Create background process for training
        task = train_workflow.apply_async()

        return {'train_id': task.task_id}

    @app.route('/train/<train_id>', methods=['get'])
    @safe_api_call
    def get_train_status(train_id):
        # Get celery task by id
        result = AsyncResult(train_id)
        return {'status': result.state}

    @app.route('/health', methods=['get'])
    def health():
        return {"result": "success"}
