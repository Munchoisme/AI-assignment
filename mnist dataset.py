import tensorflow as tf
from tensorflow.keras.datasets import mnist
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense,Flatten
from tensorflow.keras.utils import to_categorical

#Downloads the MNIST dataset and splits it into training and testing sets
(train_X,train_y),(test_X,test_y) = mnist.load_data()

#Normalize pixel values to the range[0, 1]
train_X = train_X/255.0
test_X = test_X/255.0


train_y = to_categorical(train_y,10)
test_y = to_categorical(test_y,10)

#Builds a simple feedforward neural network for classifying the MNIST digits by converting the 28x28 pixel images into a flat vector of 784 inputs, followed by two hidden layers with ReLU activation and an output layer with softmax activation for the 10 digit classes. 
model = Sequential([
    Flatten(input_shape=(28,28)),     
    Dense(128,activation='relu'),
    Dense(64,activation='relu'),
    Dense(10,activation='softmax')   
])

#Compiles the model using the Adam optimizer, categorical cross-entropy loss function, and accuracy as a metric to evaluate the model's performance during training and testing.
model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

#Trains the model on the training data for 5 epochs with a batch size of 32, using 10% of the training data as a validation set to monitor the model's performance on unseen data during training.
model.fit(train_X,train_y,epochs=5,batch_size=32,validation_split=0.1)

#Evaluates the model's performance on the test set and prints the test accuracy.
loss,accuracy= model.evaluate(test_X,test_y)
print(f"Test accuracy:{accuracy:.4f}")