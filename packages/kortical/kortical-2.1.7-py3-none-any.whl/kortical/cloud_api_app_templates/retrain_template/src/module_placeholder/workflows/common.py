from kortical.app import get_app_config

app_config = get_app_config(format='yaml')

target = app_config['target']
model_code = r"""- ml_solution:
  - data_set:
    - target_column: close_price_above_open
    - problem_type: classification
    - evaluation_metric: accuracy
    - fraction_of_data_set_to_use: 1
    - cross_validation_folds: 3
    - time_series:
      - date_time_index: date
      - test_start_date_time: '2015-08-10 00:00:00'
      - test_end_date_time: '2015-12-31 00:00:00'
  - features:
    - numeric:
      - 'high_price'
      - 'low_price'
      - 'close_price'
    - categorical
    - text:
      - tweet_contents
    - date:
      - date
  - models:
    - one_of:
      - xgboost
      - linear
      - random_forest
      - extra_trees
      - decision_tree
      - deep_neural_network
      - lightgbm"""


def preprocessing(df):
    # Do custom logic here
    pass


def postprocessing(df):
    return df