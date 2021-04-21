##############################################################################################
# Filename: RBM_learn.py
#
# Purpose: A small library for defining and training Restricted Boltzmann Machine objects
#
# Author(s): Bobby (Robert) Lumpkin
#
# Library Dependencies: numpy, SciPy
##############################################################################################

## Load modules
import numpy as np
from scipy.special import expit

class rbm_network:
    ## Initialize the RBM object by creating n_v & n_h properties for the number of visible and hidden units
    def __init__(self, n_v, n_h):
        self.n_v = n_v
        self.n_h = n_h

    ## A function to initialize the weights of the RBM
    def initialize_weights(self, seed):
        # Set a seed for reproducibility
        np.random.seed(seed)

        # randomly initialize the weights and biases
        self.W = np.random.normal(loc = 0, scale = (1 / (self.n_v + self.n_h)), size = (self.n_v, self.n_h))

    ## Define a function to generate a layer of neurons using conditional probabilities 
    def generate_layer(self, W, current_layer):
        other_layer = np.sign(expit(np.matmul(np.transpose(W), current_layer)) - np.random.uniform(low = 0, high = 1, size = W.shape[1]))
   
        return other_layer
 
    ## Define a function to generate a layer for an entire array of neurons
    def generate_layer_array(self, W, layer_array):
        n = layer_array.shape[0]
        n_other_layer = W.shape[1]
   
        other_layer_array = np.transpose(np.sign(expit(np.matmul(np.transpose(W), np.transpose(layer_array))) - np.random.uniform(low = 0, high = 1, size = (W.shape[1], n))))
   
        return other_layer_array
   
    ## Define a function to implement a single step of weight updates
    def update_weights(self, W, v_0, learning_rate):# Input the current weights matrix and the array of visible neurons 
        # Get the number of patterns, visible layer size and hidden layer size
        n = v_0.shape[0]
        n_v = v_0.shape[1]
        n_h = W.shape[1]
   
        # Generate the h_0, v_1, and h_1 layers
        h_0 = self.generate_layer_array(W, v_0)
        v_1 = self.generate_layer_array(np.transpose(W), h_0)
        h_1 = self.generate_layer_array(W, v_1)
   
        # Initialize matrices to store the "bracket" operator values
        brackets_0 = np.zeros((n_v, n_h))
        brackets_1 = np.zeros((n_v, n_h))
   
        # Compute the "correlations" (bracket operator)
        for i in range(n_v):
            for j in range(n_h):
                # compute <v^0_ih^0_j>
                v_i = v_0[:, i]
                h_j = h_0[:, j]
                brackets_0[i, j] = np.mean(np.multiply(v_i, h_j))
           
                # compute <v^1_ih^1_j>
                v_i = v_1[:, i]
                h_j = h_0[:, j]
                brackets_1[i, j] = np.mean(np.multiply(v_i, h_j))
   
        W_new = W + learning_rate * (brackets_0 - brackets_1)
   
        return W_new
   
    ## Define a function to compute the mean absolute error over the training set
    def MAE(self, v_0):
        W = self.W
        h_0 = self.generate_layer_array(W, v_0)
        v_1 = self.generate_layer_array(np.transpose(W), h_0)
        MAE = np.mean(np.absolute(v_0 - v_1))
    
        return MAE
   
    ## Define a function to implement RBM learning
    def RBM_learn(self, v_0, learning_rate, num_epochs, verbose = 1):
        # Initialize array for storing MAE values
        MAE_array = np.zeros((1, num_epochs))
   
        for i in range(num_epochs):
            self.W = self.update_weights(self.W, v_0, learning_rate)
            MAE_afterUpdate = self.MAE(v_0)
            MAE_array[0, i] = MAE_afterUpdate
            if verbose == True:
                print("MAE after epoch ", i + 1, " : ", MAE_afterUpdate)
       
        return self.W, MAE_array
   
    ## Define a function to implement RBM learning with an adaptive learning rate
    def RBM_learn_adaptive(self, v_0, learning_rate, num_epochs, tau, verbose = 1):
        # Initialize array for storing MAE values
        MAE_array = np.zeros((1, num_epochs))
   
        for i in range(num_epochs):
            adaptive_lr = (learning_rate / (1 + (i / tau)))
            self.W = self.update_weights(self.W, v_0, adaptive_lr)
            MAE_afterUpdate = self.MAE(v_0)
            MAE_array[0, i] = MAE_afterUpdate
            if verbose == True:
                print("MAE after epoch ", i + 1, " : ", MAE_afterUpdate)
       
        return self.W, MAE_array
