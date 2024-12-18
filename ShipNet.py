import numpy as np
import math
import random 
import copy

def sigmoid(inputs):
    for input in inputs:
        input = (1 + (math.e ** (-input))) ** (-1)
    return inputs

def ReLU(inputs):
    for input in inputs:
        input = max(0, input)
    return inputs

def softMax(inputs):
    denomenator = sum([math.e**input for input in inputs])
    for input in inputs:
        input = (math.e**input)/denomenator
    return  inputs

class ShipNet:
    def __init__(self):
        self.weight1 = np.random.rand(2, 5)
        self.bias1 = np.random.rand(5, 1)

        self.weight2 = np.random.rand(5, 4)
        self.bias2 = np.random.rand(4, 1)

        #Neural Net of Architecture [2,5,4]
        #Inputs = [Angle to Nearest Asteroid, Distance to Nearest Asteroid]
        #Outputs = [Left, Right, Shoot, Move]

    def forward(self, inputs):
        inputs = np.dot(self.weight1, inputs) + self.bias1
        inputs = sigmoid(inputs)
        inputs = np.dot(self.weight2, inputs) + self.bias2
        inputs = softMax(inputs)
    
    #Returns a random action based on weighted probabilities
    def action(self, inputs):
        #Return Values {0: Left, 1: Right, 2: Shoot, 3: Move}

        inputs = self.forward(inputs)
        rand = random.randint(1,100)
        cumulative_sum = 0

        for index, prob in enumerate(inputs):
            cumulative_sum += prob
            if rand > cumulative_sum * 100:
                return index
        return 3
    
    def reproduce(self, entropy):
        child = copy.deepcopy(self)

        for parameter in [child.weight1, child.weight2, child.bias1, child.bias2]:
            perturbation = np.random.randint(-5 * entropy, 5 * entropy, size=parameter.shape) / 100
            parameter += perturbation

        return child


        

        
