
import pandas as pd
import matplotlib.pyplot as plt

iris_data = pd.read_csv('preprocessed_iris.csv')

plt.scatter(iris_data['petal_length'], iris_data['petal_width'])
plt.xlabel('Petal Length')
plt.ylabel('Petal Width')
plt.title('Iris Petal Length vs Width')
plt.savefig('iris_visualization.png')  
