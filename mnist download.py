import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.datasets import mnist


#loading the dataset
(train_X, train_y), (test_X, test_y) = mnist.load_data()

