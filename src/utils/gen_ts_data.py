# This code has been taken from "Learning Comprehensible Descriptions of Multivariate Time Series"
# from Dr. Tirthajyoti Sarkar
# As of May 2020 it is available at: https://nbviewer.jupyter.org/github/tirthajyoti/Machine-Learning-with-Python/blob/master/Synthetic_data_generation/Synth_Time_series.ipynb

import numpy as np
from numpy.random import default_rng
import pandas as pd
import random
import math
import matplotlib.pyplot as plt

# cylinder bell funnel based on "Learning comprehensible descriptions of multivariate time series"
def generate_bell(length, amplitude, default_variance):
    bell = np.random.normal(0, default_variance, length) + amplitude * np.arange(length)/length
    return bell

def generate_funnel(length, amplitude, default_variance):
    funnel = np.random.normal(0, default_variance, length) + amplitude * np.arange(length)[::-1]/length
    return funnel

def generate_cylinder(length, amplitude, default_variance):
    cylinder = np.random.normal(0, default_variance, length) + amplitude
    return cylinder

std_generators = [generate_bell, generate_funnel, generate_cylinder]



def generate_pattern_data_as_array(length=100, avg_pattern_length=5, avg_amplitude=1,
                          default_variance=1, variance_pattern_length=10, variance_amplitude=2,
                          generators=std_generators, include_negatives = True):
    data = np.random.normal(0, default_variance, length)
    current_start = random.randint(0, avg_pattern_length)
    current_length = current_length = max(1, math.ceil(random.gauss(avg_pattern_length, variance_pattern_length)))

    while current_start + current_length < length:
        generator = random.choice(generators)
        current_amplitude = random.gauss(avg_amplitude, variance_amplitude)

        while current_length <= 0:
            current_length = -(current_length-1)
        pattern = generator(current_length, current_amplitude, default_variance)

        if include_negatives and random.random() > 0.5:
            pattern = -1 * pattern

        data[current_start : current_start + current_length] = pattern

        current_start = current_start + current_length + random.randint(0, avg_pattern_length)
        current_length = max(1, math.ceil(random.gauss(avg_pattern_length, variance_pattern_length)))

    return np.array(data)

def generate_pattern_data_as_dataframe(length=100, numSamples=10, numClasses=3):
    id = np.zeros(length*numSamples)
    time = np.zeros(length*numSamples)
    data = np.zeros(length*numSamples)
    labels = np.zeros(numSamples)
    start = 0;
    amplitude = np.random.randint(1, 8, size=(numClasses))
    pattern_length = np.random.randint(8, 32, size=(numClasses))
    var_pattern_length = np.random.randint(16, 64, size=(numClasses))
    var_amplitude = np.random.randint(1, 4, size=(numClasses))
    for i in range(numSamples):
        label = random.randint(0, numClasses-1);
        labels[i] = label
        for j in range(length):
            id = i
            time = j
        data[start:start+length] = generate_pattern_data_as_array(
            length=length,
            avg_pattern_length=pattern_length[label],
            avg_amplitude=amplitude[label],
            variance_pattern_length=var_pattern_length[label],
            variance_amplitude=var_amplitude[label])
        start += length

    samples = {'id':id, 'time':time, 'x':data}
    df = pd.DataFrame(samples, columns=['id', 'time', 'x'])
    print("I mande a dataframe:\n", df)
    return df, labels
