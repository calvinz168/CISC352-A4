import nn
import numpy as np

class PerceptronModel(object):
    def __init__(self, dim):
        """
        Initialize a new Perceptron instance.

        A perceptron classifies data points as either belonging to a particular
        class (+1) or not (-1). `dim` is the dimensionality of the data.
        For example, dim=2 would mean that the perceptron must classify
        2D points.
        """
        self.w = nn.Parameter(1, dim)

    def get_weights(self):
        """
        Return a Parameter instance with the current weights of the perceptron.
        """
        return self.w

    def run(self, x_point):
        """
        Calculates the score assigned by the perceptron to a data point x.

        Inputs:
            x_point: a node with shape (1 x dimensions)
        Returns: a node containing a single number (the score)
        """
        "*** YOUR CODE HERE ***"
        return nn.DotProduct(self.w, x_point)

    def get_prediction(self, x_point):
        """
        Calculates the predicted class for a single data point `x_point`.

        Returns: -1 or 1
        """
        "*** YOUR CODE HERE ***"
        score = nn.as_scalar(self.run(x_point))
        return 1 if score >= 0 else -1

    def train_model(self, dataset):
        """
        Train the perceptron until convergence.
        """
        "*** YOUR CODE HERE ***"
        converged = False
        while not converged:
            converged = True
            for x_point, y_label in dataset.iterate_once(1):
                prediction = self.get_prediction(x_point)
                actual_label = nn.as_scalar(y_label)

                if prediction != actual_label: # updates the weights
                    converged = False
                    nn.Parameter.update(self.w, actual_label, x_point)

class RegressionModel(object):
    def __init__(self):

        self.W1 = nn.Parameter(1, 50)
        self.b1 = nn.Parameter(1, 50)
        self.W2 = nn.Parameter(50, 1)
        self.b2 = nn.Parameter(1, 1)
        self.learning_rate = 0.001

    def run(self, x):
        """
        Runs the model for a batch of examples.
        """
        h1 = nn.ReLU(nn.AddBias(nn.Linear(x, self.W1), self.b1))  # Hidden layer with ReLU activation
        output = nn.AddBias(nn.Linear(h1, self.W2), self.b2)      # Output layer
        return output

    def get_loss(self, x, y):
        """
        Computes the loss for a batch of examples.
        """

        predictions = self.run(x)
        loss = nn.SquareLoss(predictions, y)
        return loss

    def train_model(self, dataset):
        """
        Trains the model.
        """
        
        while True:
            total_loss = 0
            num_batches = 0
            for x_batch, y_batch in dataset.iterate_once(batch_size=10):
                loss = self.get_loss(x_batch, y_batch)

                gradients = nn.gradients([self.W1, self.b1, self.W2, self.b2], loss)

                self.W1.update(-self.learning_rate, gradients[0])
                self.b1.update(-self.learning_rate, gradients[1])
                self.W2.update(-self.learning_rate, gradients[2])
                self.b2.update(-self.learning_rate, gradients[3])
                
                total_loss += nn.as_scalar(loss)
                num_batches += 1
            
            avg_loss = total_loss / num_batches
            print(f"Avg loss: {avg_loss}")

            if avg_loss < 0.02:
                break


class DigitClassificationModel(object):
    """
    A model for handwritten digit classification using the MNIST dataset.

    Each handwritten digit is a 28x28 pixel grayscale image, which is flattened
    into a 784-dimensional vector for the purposes of this model. Each entry in
    the vector is a floating point number between 0 and 1.

    The goal is to sort each digit into one of 10 classes (number 0 through 9).

    (See RegressionModel for more information about the APIs of different
    methods here. We recommend that you implement the RegressionModel before
    working on this part of the project.)
    """
    def __init__(self):
        # Initialize your model parameters here
        "*** YOUR CODE HERE ***"
        self.learning_rate = 0.1
        self.batch_size = 100
        self.hidden_size = 200
        
        # Initialize weights and biases
        self.W1 = nn.Parameter(784, self.hidden_size)
        self.b1 = nn.Parameter(1, self.hidden_size)
        self.W2 = nn.Parameter(self.hidden_size, 10)
        self.b2 = nn.Parameter(1, 10)

    def run(self, x):
        """
        Runs the model for a batch of examples.

        Your model should predict a node with shape (batch_size x 10),
        containing scores. Higher scores correspond to greater probability of
        the image belonging to a particular class.

        Inputs:
            x: a node with shape (batch_size x 784)
        Output:
            A node with shape (batch_size x 10) containing predicted scores
                (also called logits)
        """
        "*** YOUR CODE HERE ***"
        layer1 = nn.ReLU(nn.AddBias(nn.Linear(x, self.W1), self.b1))
        logits = nn.AddBias(nn.Linear(layer1, self.W2), self.b2)
        return logits

    def get_loss(self, x, y):
        """
        Computes the loss for a batch of examples.

        The correct labels `y` are represented as a node with shape
        (batch_size x 10). Each row is a one-hot vector encoding the correct
        digit class (0-9).

        Inputs:
            x: a node with shape (batch_size x 784)
            y: a node with shape (batch_size x 10)
        Returns: a loss node
        """
        "*** YOUR CODE HERE ***"
        logits = self.run(x)
        return nn.SoftmaxLoss(logits, y)

    def train_model(self, dataset):
        """
        Trains the model.
        """
        "*** YOUR CODE HERE ***"
        while True:
            for x, y in dataset.iterate_once(self.batch_size):
                loss = self.get_loss(x, y)
                gradients = nn.gradients([self.W1, self.b1, self.W2, self.b2], loss)
                
                # Update parameters
                self.W1.update(-self.learning_rate, gradients[0])
                self.b1.update(-self.learning_rate, gradients[1])
                self.W2.update(-self.learning_rate, gradients[2])
                self.b2.update(-self.learning_rate, gradients[3])
                
            # Check validation accuracy for termination
            if dataset.get_validation_accuracy() >= 0.975:
                break
