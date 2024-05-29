import streamlit as st
import math
import re

# Function to estimate mean and SD from median, min, and max
def estimate_mean_sd_from_median_min_max(vals):
    try:
        median, min_val, max_val = re.findall(r'\d+[\.\d+]*', vals)
        median, min_val, max_val = map(float, [median, min_val, max_val])
        mean = (2 * median + min_val + max_val) / 4
        sd = (max_val - min_val) / 4
        return median, min_val, max_val, mean, sd
    except ValueError:
        return 'Invalid input. Please enter values in the format "median, min, max"', None, None, None, None

# Function to estimate mean and SD from quartiles
def estimate_mean_and_sd_from_quartiles(vals):
    try:
        median, q1, q3 = re.findall(r'\d+[\.\d+]*', vals)
        median, q1, q3 = map(float, [median, q1, q3])
        estimated_mean = (q1 + 2 * median + q3) / 4
        term1 = ((q1 - 2 * median + q3) ** 2) / 4
        term2 = (q3 - q1) ** 2
        variance = (1 / 12) * (term1 + term2)
        estimated_sd = math.sqrt(variance)
        return median, q1, q3, estimated_mean, estimated_sd
    except ValueError:
        return 'Invalid input. Please enter values in the format "median, Q1, Q3"', None, None, None, None
    
# Function to estimate mean and SD from median and confidence interval
def estimate_mean_sd_from_median_ci(vals):
    try:     
        median, lower_ci, upper_ci = re.findall(r'\d+[\.\d+]*', vals)
        median, lower_ci, upper_ci = map(float, [median, lower_ci, upper_ci])
        mean = (lower_ci + upper_ci + 2 * median) / 4
        sd = (upper_ci - lower_ci) / (2 * 1.96)
        return median, lower_ci, upper_ci, mean, sd
    except ValueError:
        return 'Invalid input. Please enter values in the format "median, lower CI, upper CI"', None, None, None, None

# Function to combine means and SDs
def combine_means_and_sds(vals):
    try:
        mean1, sd1, n1, mean2, sd2, n2 = re.findall(r'\d+[\.\d+]*', vals)
        mean1, sd1, n1, mean2, sd2, n2 = map(float, [mean1, sd1, n1, mean2, sd2, n2])
        combined_mean = (n1 * mean1 + n2 * mean2) / (n1 + n2)
        numerator = ((n1 - 1) * (sd1 ** 2) + (n2 - 1) * (sd2 ** 2) +
                    n1 * (mean1 - combined_mean) ** 2 + n2 * (mean2 - combined_mean) ** 2)
        combined_sd = math.sqrt(numerator / (n1 + n2 - 1))
        return mean1, sd1, n1, mean2, sd2, n2, combined_mean, combined_sd
    except ValueError:
        return 'Invalid input. Please enter values in the format "mean1, sd1, n1, mean2, sd2, n2"', None, None, None, None, None, None, None

# Streamlit app
st.title('Statistical Estimator Tool')

st.header('Estimate Mean and SD from Median, Min, and Max')
vals1 = st.text_input('Enter values as "median, min, max"', '')
if vals1:
    result = estimate_mean_sd_from_median_min_max(vals1)
    if isinstance(result, str):
        st.write(result)
    else:
        median, min_val, max_val, mean, sd = result
        st.write(f'Input values: Median = {median}, Min = {min_val}, Max = {max_val}')
        st.write(f'Estimated Mean: {mean}')
        st.write(f'Estimated Standard Deviation: {sd}')

st.header('Estimate Mean and SD from Quartiles')
vals2 = st.text_input('Enter values as "median, Q1, Q3"', '')
if vals2:
    result = estimate_mean_and_sd_from_quartiles(vals2)
    if isinstance(result, str):
        st.write(result)
    else:
        median, q1, q3, mean, sd = result
        st.write(f'Input values: Median = {median}, Q1 = {q1}, Q3 = {q3}')
        st.write(f'Estimated Mean: {mean}')
        st.write(f'Estimated Standard Deviation: {sd}')

st.header('Estimate Mean and SD from Median and Confidence Interval')
vals3 = st.text_input('Enter values as "median, lower CI, upper CI"', '')
if vals3:
    result = estimate_mean_sd_from_median_ci(vals3)
    if isinstance(result, str):
        st.write(result)
    else:
        median, lower_ci, upper_ci, mean, sd = result
        st.write(f'Input values: Median = {median}, Lower CI = {lower_ci}, Upper CI = {upper_ci}')
        st.write(f'Estimated Mean: {mean}')
        st.write(f'Estimated Standard Deviation: {sd}')

st.header('Combine Means and Standard Deviations')
vals4 = st.text_input('Enter values as "mean1, sd1, n1, mean2, sd2, n2"', '')
if vals4:
    result = combine_means_and_sds(vals4)
    if isinstance(result, str):
        st.write(result)
    else:
        mean1, sd1, n1, mean2, sd2, n2, combined_mean, combined_sd = result
        st.write(f'Input values: Mean 1 = {mean1}, SD 1 = {sd1}, n1 = {n1}')
        st.write(f'Mean 2 = {mean2}, SD 2 = {sd2}, n2 = {n2}')
        st.write(f'Combined Mean: {combined_mean}')
        st.write(f'Combined Standard Deviation: {combined_sd}')
