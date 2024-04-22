At the beginning, the model was trained with a single convolutional layer (32 filters each of 3X3 kernel size), a (2X2) maxpool layer, dropout layer with 0.5 fraction, a flattening layer, a hidden dense layer with 128 units and an output layer with 43 units for each output. The convolutional and hidden dense layer had relu activation functions whereas the output layer had softmax function. But this model was unable to deliver optimal results with only 7% accuracy.

So, two more convolutional layers with 64 and 128 kernels each were added after the first one with one maxpool layer following each. This drastically increased the performance to around 85% accuracy.

For better results, the number of units in the hidden layer was also increaed to 256. This then, increased the accuracy to 90%.

Finally one more convolutional layer with 256 kernels was introduced with padding and the model was able to maintain an accuracy of 97%.

