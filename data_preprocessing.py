
import pandas as pd

iris_data = pd.read_csv('iris.csv')

iris_data = iris_data.dropna()

iris_data.to_csv('preprocessed_iris.csv', index=False)
