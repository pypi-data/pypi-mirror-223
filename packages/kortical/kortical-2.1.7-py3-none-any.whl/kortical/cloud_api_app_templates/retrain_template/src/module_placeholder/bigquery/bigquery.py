import json
import logging
from datetime import datetime, timedelta
from kortical.app import get_app_config
from kortical.secret import secret

from google.oauth2 import service_account
from google.cloud import bigquery
from google.cloud import bigquery_storage

logger = logging.getLogger(__name__)

service_account_key = json.loads(secret.get("bigquery_service_account_key"))
credentials = service_account.Credentials.from_service_account_info(
    info=service_account_key, scopes=["https://www.googleapis.com/auth/cloud-platform"],
)

app_config = get_app_config(format='yaml')
BIGQUERY_TABLE = app_config['bigquery_table']

# Make clients.
bqclient = bigquery.Client(credentials=credentials, project=credentials.project_id,)
bqstorageclient = bigquery_storage.BigQueryReadClient(credentials=credentials)


def get_cutoff_dates(table):
    # Get the maximum timestamp in the table
    max_timestamp_query = f"SELECT MAX({app_config['date_column']}) as max_timestamp FROM `{table}`"
    max_timestamp = bqclient.query(max_timestamp_query).to_dataframe().iloc[0]['max_timestamp']

    # Calculate cutoff timestamps
    test_cutoff_timestamp = max_timestamp - timedelta(days=app_config['test_set_cutoff_days'])
    train_cutoff_timestamp = test_cutoff_timestamp - timedelta(days=app_config['train_set_cutoff_days'])
    logger.info(f"Will query rows between [{train_cutoff_timestamp}] and [{max_timestamp}], rows past [{test_cutoff_timestamp}] to be used for testing.")
    return train_cutoff_timestamp, test_cutoff_timestamp


# Function to calculate the percentage of rows needed
def calculate_percentage_needed(total_rows, desired_rows):
    return min(100, (desired_rows / total_rows) * 100)


def get_sampling_percentage(table, min_timestamp):
    """Calculate the sampling percentage necessary to fit within the maximum amount of rows."""
    total_rows_query = f"SELECT count(date) as total_rows FROM `{table}` where TIMESTAMP(date) >= TIMESTAMP(DATETIME('{min_timestamp}'))"
    total_rows = bqclient.query(total_rows_query).to_dataframe().iloc[0]['total_rows']
    max_rows = app_config['bigquery_max_rows']
    required_percentage = calculate_percentage_needed(total_rows, max_rows)
    logger.info(f"Setting sampling percentage to [{required_percentage}%] of [{total_rows}] total selectable rows.")
    return required_percentage


def get_selected_rows(table, required_percentage, min_timestamp):
    """Get [required_percentage]% of rows from bigquery dated after [min_timestamp]"""
    selected_rows_query = f"""SELECT
        `int64_field_0`,
        `date`,
        `high_price`,
        `low_price`,
        `close_price`, 
        `volume`,
        `tweet_contents`,
        `total_user_tweets_today`,
        `unique_users_tweets_today`,
        `close_price_above_open`
    FROM `{table}` TABLESAMPLE SYSTEM ({required_percentage} PERCENT) WHERE TIMESTAMP(date) >= TIMESTAMP(DATETIME('{min_timestamp}'))"""
    selected_rows = bqclient.query(selected_rows_query).to_dataframe()
    return selected_rows


def create_dataframes_from_bigquery():
    # Creating dataframe from bigquery data
    logger.info('Creating dataframe from bigquery')

    # Set a table.
    table = BIGQUERY_TABLE

    # Get the dates we will work with. train_cutoff_timestamp will be how far back
    # we get training data from, test_cutoff_timestamp defines where we split that data
    # to keep the most recent for the testing dataset.
    train_cutoff_timestamp, test_cutoff_timestamp = get_cutoff_dates(table)
    required_percentage = get_sampling_percentage(table, train_cutoff_timestamp)

    selected_rows = get_selected_rows(table, required_percentage, train_cutoff_timestamp)

    # Split into training and testing datasets based on the date cutoff.
    mask = selected_rows['date'] >= test_cutoff_timestamp
    df_test = selected_rows[mask]
    df_train = selected_rows[~mask]

    return df_train, df_test
