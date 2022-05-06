import numpy as np
import random
import math
inputs=np.array([1,1,1,0,1,0])
bias= np.array([])
##first layer with 4 neurons
firstlayer=np.array([])
numberofneurons=10

#calculation function for each neuron
def neuron(inputs,weights,bias):
    z=0
    for x in range(len(inputs)):
        z= z+ inputs[x]* weights[x]
    z=z+bias
    z=1 / (1 + math.exp(-z))
    return z
#initializes the random weights
def createrandomweights(numberofneurons):
    weights=np.empty((numberofneurons,len(inputs)))
    for x in range(numberofneurons):
        for p in range(len(inputs)):
            weights[x][p]=random.random()
    return weights

weights=createrandomweights(numberofneurons)

#intiialzes the biases
def createrandombias(numberofneurons):
    bias=np.empty(numberofneurons)
    for p in range(numberofneurons):
        bias[p]=random.random()
    return bias

bias=createrandombias(numberofneurons)

#calculates neurons for each layer
def layer(weights,bias, inputs, layer):
    for p in range(numberofneurons):
        neuron1=neuron(inputs,weights[p],bias[p])
        layer=np.append(layer,neuron1)
    return layer

#calls function and calculates MSE
def backpropogate(inputs,weights, bias, trainingrate):
    layer1=layer(weights,bias,inputs, firstlayer)
    MSE=0
    dMSEdlayer=0
    for x in range(numberofneurons):
        tempz = layer1[x]
        for p in range(len(inputs)):
            neuronerror = layer1[x] - inputs[p]
            MSE = MSE + (neuronerror) ** 2
            dMSEdlayer=dMSEdlayer+ 2*(neuronerror)
            dlayerdz= tempz*(1-tempz)
            dzdw=inputs[p]
            dMSEdw=dMSEdlayer*dlayerdz*dzdw
            weights[x][p]=weights[x][p]-trainingrate*dMSEdw

        dMSEdb=dMSEdlayer*dlayerdz
        bias[x]=bias[x]-trainingrate*dMSEdb
    return layer1
def train(inputs,weights,bias,trainingrate, epochs):
    for x in range(epochs):
        print("Epoch " + str(x+1) + " :")
        print(backpropogate(inputs,weights,bias,trainingrate))

layer1 = train(inputs,weights,bias,0.01, 2000)










