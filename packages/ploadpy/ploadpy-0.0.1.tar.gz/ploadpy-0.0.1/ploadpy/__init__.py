def p1():
    return """import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

dataset = pd.read_csv('iris.csv')
X = dataset.iloc[:, :4].values
y = dataset['species'].values
dataset.head(5)

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

from sklearn.naive_bayes import GaussianNB
classifier = GaussianNB()
classifier.fit(X_train, y_train)
y_pred = classifier.predict(X_test)
y_pred

from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)

from sklearn.metrics import accuracy_score
print("Accuracy : ", accuracy_score(y_test, y_pred))

cm

df = pd.DataFrame({'Real Values': y_test, 'Predicted Values': y_pred})
df
"""

def p2():
    return """import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sklearn

dataset = pd.read_csv('iris.csv')
X = dataset.iloc[:, [1, 2, 3]].values
y = dataset.iloc[:, -1].values

from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
X[:, 0] = le.fit_transform(X[:, 0])

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=0)

from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

from sklearn.neighbors import KNeighborsClassifier
classifier = KNeighborsClassifier(n_neighbors=5, metric='minkowski', p=2)
classifier.fit(X_train, y_train)

y_pred = classifier.predict(X_test)

y_test
y_pred

from sklearn.metrics import confusion_matrix, accuracy_score
cm = confusion_matrix(y_test, y_pred)
ac = accuracy_score(y_test, y_pred)

cm
ac
"""

def p3():
    return """import numpy as np
from sklearn.datasets import load_iris

iris = load_iris()
iris.target_names

targets = (iris.target == 0).astype(np.int8)
print(targets)

from sklearn.model_selection import train_test_split

datasets = train_test_split(iris.data, targets, test_size=0.2)
train_data, test_data, train_labels, test_labels = datasets

# Now, we create a Perceptron instance and fit the training data:
from sklearn.linear_model import Perceptron

p = Perceptron(random_state=42, max_iter=10, tol=0.001)
p.fit(train_data, train_labels)

import random

sample = random.sample(range(len(train_data)), 10)
for i in sample:
    print(i, p.predict([train_data[i]]))

from sklearn.metrics import classification_report

print(classification_report(p.predict(train_data), train_labels))
print(classification_report(p.predict(test_data), test_labels))
"""

def p4():
    return """import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

# Load dataset
data = load_iris()

# Get features and target
X = data.data
y = data.target

# Get dummy variable
y = pd.get_dummies(y).values
y[:3]

# Split data into train and test data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=20, random_state=4)

# Initialize variables
learning_rate = 0.1
iterations = 5000
N = y_train.size

# number of input features
input_size = 4

# number of hidden layers neurons
hidden_size = 2

# number of neurons at the output layer
output_size = 3

results = pd.DataFrame(columns=["mse", "accuracy"])

# Initialize weights
np.random.seed(10)

# initializing weight for the hidden layer
W1 = np.random.normal(scale=0.5, size=(input_size, hidden_size))

# initializing weight for the output layer
W2 = np.random.normal(scale=0.5, size=(hidden_size, output_size))


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def mean_squared_error(y_pred, y_true):
    return ((y_pred - y_true) ** 2).sum() / (2 * y_pred.size)


def accuracy(y_pred, y_true):
    acc = y_pred.argmax(axis=1) == y_true.argmax(axis=1)
    return acc.mean()


for itr in range(iterations):
    # feedforward propagation
    # on hidden layer
    Z1 = np.dot(X_train, W1)
    A1 = sigmoid(Z1)

    # on output layer
    Z2 = np.dot(A1, W2)
    A2 = sigmoid(Z2)

    # Calculating error
    mse = mean_squared_error(A2, y_train)
    acc = accuracy(A2, y_train)
    results = results.append({"mse": mse, "accuracy": acc}, ignore_index=True)

    # backpropagation
    E1 = A2 - y_train
    dW1 = E1 * A2 * (1 - A2)
    E2 = np.dot(dW1, W2.T)
    dW2 = E2 * A1 * (1 - A1)

    # weight updates
    W2_update = np.dot(A1.T, dW1) / N
    W1_update = np.dot(X_train.T, dW2) / N

    W2 = W2 - learning_rate * W2_update
    W1 = W1 - learning_rate * W1_update

results.mse.plot(title="Mean Squared Error")
results.accuracy.plot(title="Accuracy")

# feedforward
Z1 = np.dot(X_test, W1)
A1 = sigmoid(Z1)
Z2 = np.dot(A1, W2)
A2 = sigmoid(Z2)
acc = accuracy(A2, y_test)

print("Accuracy: {}".format(acc))
"""

def p5():
    return """from sklearn.datasets import load_iris
from sklearn.cluster import KMeans
from sklearn.mixture import GaussianMixture
from sklearn.metrics import completeness_score
import matplotlib.pyplot as plt
import numpy as np

data = load_iris()
x = data.data
y = data.target

wcss = []
for i in range(2, 11):
    model = KMeans(n_clusters=i)
    model.fit(x)
    wcss.append(model.inertia_)
plt.figure()
plt.plot(range(2, 11), wcss)

model = KMeans(n_clusters=3)
model.fit(x)
print("The completeness score of KMeans is:", completeness_score(y, model.labels_))

gmm = GaussianMixture(n_components=3, random_state=1)
gmm.fit(x)
y_pred = gmm.predict(x)
print("The completeness score of Gaussian Mixture is:", completeness_score(y, y_pred))

plt.figure(figsize=(21, 7))
colorMap = np.array(["lime", "red", "black"])

plt.subplot(1, 3, 1)
plt.scatter(x[:, 2], x[:, 3], c=colorMap[y])
plt.title("Real Classification")
plt.xlabel("Petal Length")
plt.ylabel("Petal Width")

plt.subplot(1, 3, 2)
plt.scatter(x[:, 2], x[:, 3], c=colorMap[model.labels_])
plt.title("KMeans Classification")
plt.xlabel("Petal Length")
plt.ylabel("Petal Width")

plt.subplot(1, 3, 3)
plt.scatter(x[:, 2], x[:, 3], c=colorMap[gmm.predict(x)], s=40)
plt.title("Gaussian Mixture Classification")
plt.xlabel("Petal Length")
plt.ylabel("Petal Width")
"""