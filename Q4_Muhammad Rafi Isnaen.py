# -*- coding: utf-8 -*-
"""tempatsampah_2.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1M8_Efo6jDdus1KGEcGrt5UUqW75dUFEA
"""

import numpy as np
import matplotlib.pyplot as plt
import math

# Data
x = np.arange(1, 145, 1)
y = np.array([1863, 1614, 2570, 1685, 2101, 1811, 2457, 2171, 2134, 2502, 2358, 2399,
              2048, 2523, 2086, 2391, 2150, 2340, 3129, 2277, 2964, 2997, 2747, 2862,
              3405, 2677, 2749, 2755, 2963, 3161, 3623, 2768, 3141, 3439, 3601, 3531,
              3477, 3376, 4027, 3175, 3274, 3334, 3964, 3649, 3502, 3688, 3657, 4422,
              4197, 4441, 4736, 4521, 4485, 4644, 5036, 4876, 4789, 4544, 4975, 5211,
              4880, 4933, 5079, 5339, 5232, 5520, 5714, 5260, 6110, 5334, 5988, 6235,
              6365, 6266, 6345, 6118, 6497, 6278, 6638, 6590, 6271, 7246, 6584, 6594,
              7092, 7326, 7409, 7976, 7959, 8012, 8195, 8008, 8313, 7791, 8368, 8933,
              8756, 8613, 8705, 9098, 8769, 9544, 9050, 9186, 10012, 9685, 9966, 10048,
              10244, 10740, 10318, 10393, 10986, 10635, 10731, 11749, 11849, 12123, 12274,
              11666, 11960, 12629, 12915, 13051, 13387, 13309, 13732, 13162, 13644, 13808,
              14101, 13992, 15191, 15018, 14917, 15046, 15556, 15893, 16388, 16782, 16716,
              17033, 16896, 17689])

# Transform y to Y = ln(y)
Y = np.log(y)

# Calculate the sums needed for the linear regression using for loop
n = len(x)
sum_x = 0
sum_Y = 0
sum_xY = 0
sum_x2 = 0

for i in range(n):
    sum_x += x[i]
    sum_Y += Y[i]
    sum_xY += x[i] * Y[i]
    sum_x2 += x[i] * x[i]

# Calculate coefficients a' and b' for the linear regression Y = a' + b'x
b_prime = (n * sum_xY - sum_x * sum_Y) / (n * sum_x2 - sum_x * sum_x)
a_prime = (sum_Y - b_prime * sum_x) / n

# Transform back to the coefficients a and b for the exponential regression y = a * e^(b * x)
a = np.exp(a_prime)
b = b_prime

# Print coefficients
print(f"a = {a:.3f}")
print(f"b = {b:.3f}")

# Print the exponential regression equation
print(f"The exponential regression equation is: y = {a:.3f} * e^({b:.3f} * x)")

# Define the exponential regression function
exponential_regression = lambda x: a * np.exp(b * x)

# Predict y values using the exponential regression model
y_pred = np.zeros(len(x))
for i in range(len(x)):
    y_pred[i] = exponential_regression(x[i])

# Function to calculate derivatives
def derivate(f, x, h, mode='first'):
    if mode == 'first':
        result = (-f(x) + f(x+h)) / h
    elif mode == 'second':
        result = (f(x) - 2*f(x+h) + f(x+(2*h))) / h**2
    elif mode == 'third':
        result = (-f(x) + (3*f(x+h)) - (3*f(x+(2*h))) + f(x+(3*h))) / h**3
    elif mode == 'fourth':
        result = (f(x) - (4*f(x+h)) + (6*f(x+(2*h))) - (4*f(x+(3*h))) + f(x+(4*h))) / h**4
    elif mode == 'fifth':
        result = (-f(x) + (5*f(x+h)) - (10*f(x+(2*h))) + (10*f(x+(3*h))) - (5*f(x+(4*h))) + f(x+(5*h))) / h**5
    return result

# Choose a point for Taylor series expansion (midpoint of x)
a_point = x[len(x) // 2]
h = 1

# Function for Taylor series
f = exponential_regression

# Calculate derivatives at the chosen point
f_prime = [f(a_point)]
f_prime.append(derivate(f, a_point, h, mode='first'))
f_prime.append(derivate(f, a_point, h, mode='second'))
f_prime.append(derivate(f, a_point, h, mode='third'))
f_prime.append(derivate(f, a_point, h, mode='fourth'))
f_prime.append(derivate(f, a_point, h, mode='fifth'))

# Taylor series approximation function
def taylor_series(x, a_point, f_prime):
    taylor_approx = np.zeros(len(x))
    for i in range(len(x)):
        taylor_approx[i] = f_prime[0]
        for n in range(1, len(f_prime)):
            taylor_approx[i] += f_prime[n] * (x[i] - a_point)**n / math.factorial(n)
    return taylor_approx

# Calculate Taylor series approximation
taylor_approx = taylor_series(x, a_point, f_prime)

# Calculate Taylor series approximation
taylor_approx = taylor_series(x, a_point, f_prime)

# Accuracy Calculation for Exponential Regression and Taylor Series
mae_exp = 0
mae_taylor = 0

# Mean Absolute Error for Exponential Regression
for i in range(len(y)):
    mae_exp += abs(y[i] - y_pred[i])
mae_exp /= len(y)

# Mean Absolute Error for Taylor Series
for i in range(len(y)):
    mae_taylor += abs(y[i] - taylor_approx[i])
mae_taylor /= len(y)

print(f"Mean Absolute Error for Exponential Regression: {mae_exp:.3f}")
print(f"Mean Absolute Error for Taylor Series: {mae_taylor:.3f}")

# Extend the range to ensure we capture the point
extended_x = np.arange(1, 300, 1)
taylor_approx_extended = taylor_series(extended_x, a_point, f_prime)

# Newton-Raphson Method for Root Finding
def newtonraphson_graph(f, df, x0, eps):
    x = [x0]
    y = [f(x0)]
    delta = abs(f(x0))
    while delta > eps:
        x0 -= f(x0) / df(x0)
        delta = abs(f(x0))
        x.append(x0)
        y.append(f(x0))
    return x0, x, y

# Function and its derivative for Newton-Raphson
f_root = lambda x: a * np.exp(b * x) - 25000
df_root = lambda x: a * b * np.exp(b * x)

# Initial guess
x0 = 120  # Initial guess
eps = 1e-6

# Apply Newton-Raphson method
root, x_iter, y_iter = newtonraphson_graph(f_root, df_root, x0, eps)

# Calculate the month when the warehouse will be full using loop
full_month = None
for i in range(145, len(extended_x)):  # Start from month 145
    taylor_value = f_prime[0]
    for n in range(1, len(f_prime)):
        taylor_value += f_prime[n] * (i - a_point)**n / math.factorial(n)
    taylor_approx_extended[i] = taylor_value
    if taylor_value > 25000:
        full_month = i
        break
taylor_approx_extended = taylor_approx_extended[:full_month+1]  # Stop the Taylor series plot at full_month

# Calculate the month to start building a new warehouse
build_month = full_month - 13

# Plot the original data, regression curve, and Taylor approximation
plt.figure(figsize=(12, 6))
plt.scatter(x, y, color='blue', label='Actual data')
plt.plot(x, y_pred, color='green', label='Trend line')
plt.plot(extended_x[:len(taylor_approx_extended)], taylor_approx_extended, color='orange', label='Taylor Series approximation')
plt.axhline(25000, color='red', linestyle='--', label='Max warehouse capacity')
plt.scatter(full_month, a * np.exp(b * full_month), color='red', label=f'Month {full_month}, {a * np.exp(b * full_month):.3f} bags produced')
plt.axvline(full_month, color='red', linestyle='--')
plt.scatter(build_month, a * np.exp(b * build_month), color='purple', label=f'Start building new warehouse in Month {build_month}')
plt.axvline(build_month, color='purple', linestyle='--')
plt.xlabel('Months')
plt.ylabel('Bags produced')
plt.title('Bags Produced Over Time')
plt.legend()
plt.grid(True)
plt.show()

# Output results
print(f"The exponential regression equation is: y = {a:.3f} * e^({b:.3f} * x)")
print(f"The warehouse will be full in month {full_month} with approximately {a * np.exp(b * full_month):.3f} bags produced.")
print(f"Start building a new warehouse in month {build_month}.")