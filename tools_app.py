import streamlit as st
import numpy as np
import math
import re

# Function to estimate mean and SD from median, min, and max
def estimate_mean_sd_from_median_min_max(median, min_val=None, max_val=None):
    if isinstance(median, str):
        median, min_val, max_val = re.findall(r'\d+[\.\d+]*', median)
        median, min_val, max_val = map(float, [median, min_val, max_val])

    mean = (2 * median + min_val + max_val) / 4
    sd = (max_val - min_val) / 4
    return mean, sd

# Function to estimate mean and SD from quartiles
def estimate_mean_and_sd_from_quartiles(median, q1=None, q3=None):
    if isinstance(median, str):
        median, q1, q3 = re.findall(r'\d+[\.\d+]*', median)
        median, q1, q3 = map(float, [median, q1, q3])

    estimated_mean = (q1 + 2 * median + q3) / 4
    term1 = ((q1 - 2 * median + q3) ** 2) / 4
    term2 = (q3 - q1) ** 2
    variance = (1 / 12) * (term1 + term2)
    estimated_sd = math.sqrt(variance)
    return estimated_mean, estimated_sd

# Function to estimate mean and SD from median and confidence interval
def estimate_mean_sd_from_median_ci(median, lower_ci, upper_ci):
    mean = (lower_ci + upper_ci + 2 * median) / 4
    sd = (upper_ci - lower_ci) / (2 * 1.96)
    return mean, sd

# Function to combine means and SDs
def combine_means_and_sds(mean1, sd1, n1, mean2, sd2, n2):
    combined_mean = (n1 * mean1 + n2 * mean2) / (n1 + n2)
    numerator = ((n1 - 1) * (sd1 ** 2) + (n2 - 1) * (sd2 ** 2) +
                 n1 * (mean1 - combined_mean) ** 2 + n2 * (mean2 - combined_mean) ** 2)
    combined_sd = math.sqrt(numerator / (n1 + n2 - 1))
    return combined_mean, combined_sd

# Streamlit app
st.title('Statistical Estimator Tool')

st.header('Estimate Mean and SD from Median, Min, and Max')
median = st.number_input('Median', value=0.0)
min_val = st.number_input('Minimum Value', value=0.0)
max_val = st.number_input('Maximum Value', value=0.0)
if st.button('Estimate from Median, Min, Max'):
    mean, sd = estimate_mean_sd_from_median_min_max(median, min_val, max_val)
    st.write(f'Estimated Mean: {mean}')
    st.write(f'Estimated Standard Deviation: {sd}')

st.header('Estimate Mean and SD from Quartiles')
q1 = st.number_input('First Quartile (Q1)', value=0.0)
q3 = st.number_input('Third Quartile (Q3)', value=0.0)
if st.button('Estimate from Quartiles'):
    mean, sd = estimate_mean_and_sd_from_quartiles(median, q1, q3)
    st.write(f'Estimated Mean: {mean}')
    st.write(f'Estimated Standard Deviation: {sd}')

st.header('Estimate Mean and SD from Median and Confidence Interval')
lower_ci = st.number_input('Lower Confidence Interval', value=0.0)
upper_ci = st.number_input('Upper Confidence Interval', value=0.0)
if st.button('Estimate from Median and CI'):
    mean, sd = estimate_mean_sd_from_median_ci(median, lower_ci, upper_ci)
    st.write(f'Estimated Mean: {mean}')
    st.write(f'Estimated Standard Deviation: {sd}')

st.header('Combine Means and Standard Deviations')
mean1 = st.number_input('Mean 1', value=0.0)
sd1 = st.number_input('Standard Deviation 1', value=0.0)
n1 = st.number_input('Sample Size 1', value=0)
mean2 = st.number_input('Mean 2', value=0.0)
sd2 = st.number_input('Standard Deviation 2', value=0.0)
n2 = st.number_input('Sample Size 2', value=0)
if st.button('Combine Means and SDs'):
    combined_mean, combined_sd = combine_means_and_sds(mean1, sd1, n1, mean2, sd2, n2)
    st.write(f'Combined Mean: {combined_mean}')
    st.write(f'Combined Standard Deviation: {combined_sd}')
