import os
import pandas as pd
from sklearn.model_selection import train_test_split
from SentiPers.Router import ROOT_DIR

data_size = 7415


def ingest():
    CONFIG_PATH = os.path.join(ROOT_DIR, 'data.csv')
    data = pd.read_csv(CONFIG_PATH, sep='\t')
    data.drop(['Negative-Keywords', 'Neutral-Keywords', 'Positive-Keywords', 'Targets'], axis=1, inplace=True)
    data = data[data.Value.isnull() == False]
    # map applies a function on each cell of Value then if it null, it will set it with 0s
    data['Value'] = data['Value'].map(int)
    data = data[data['Text'].isnull() == False]
    data.reset_index(inplace=True)
    data.drop('index', axis=1, inplace=True)
    print('Dataset Loaded with shape', data.shape)
    return data


ingest = ingest()   # Get all text
x_train, x_test, y_train, y_test = train_test_split(ingest.head(data_size).Text, ingest.head(data_size).Value)


def get_data():
    return x_train, x_test, y_train, y_test
