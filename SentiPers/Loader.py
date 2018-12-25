import os
import pandas as pd
from sklearn.model_selection import train_test_split
from hazm import *
from SentiPers.Router import ROOT_DIR

n = 7415


def ingest():
    CONFIG_PATH = os.path.join(ROOT_DIR, 'data.csv')
    data = pd.read_csv(CONFIG_PATH, sep='\t')
    data.drop(['Negative-Keywords', 'Neutral-Keywords', 'Positive-Keywords', 'Targets'], axis=1, inplace=True)
    data = data[data.Value.isnull() == False]
    # map applies a function on each cell of Value then if it null, it will set it with 0s
    data['Value'] = data['Value'].map(int)
    data = data[data['Text'].isnull() == False]
    normalizer = Normalizer()   # Normalizing text using Hazm library (Remove half space)
    for i in range(0, n):
        string = normalizer.normalize(data.iloc[i].Text)    # Normalizer
        # Add some other instances
        string = string.replace('سیستم عامل', 'سیستم\u200cعامل')
        string = string.replace('نرم افزار', 'نرم\u200cافزار')
        string = string.replace('سخت افزار', 'سخت\u200cافزار')
        data.set_value(i, 'Text', string)
    data.reset_index(inplace=True)
    data.drop('index', axis=1, inplace=True)
    print('Dataset Loaded with shape', data.shape)
    return data


ingest = ingest()   # Get all text
x_train, x_test, y_train, y_test = train_test_split(ingest.head(n).Text,
                                                    ingest.head(n).Value)


def get_data():
    return x_train, x_test, y_train, y_test
