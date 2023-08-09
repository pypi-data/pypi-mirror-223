import os
import pandas as pd
from sklearn.model_selection import train_test_split
from tests.helpers.root_dir import from_root_dir

from module_placeholder.workflows.train import train


class CeleryTaskMock:
    @staticmethod
    def update_state(state):
        print(state)


TRAIN_DATA_PATH = from_root_dir(os.path.join('data', 'apple_stock_tweets.csv'))


if __name__ == '__main__':
    df_train, df_test = train_test_split(pd.read_csv(TRAIN_DATA_PATH))
    train(df_train=df_train, df_test=df_test, celery_task=CeleryTaskMock)
