# ***NumSpark(v-1.0.1) - A Python Library for Mathematical Operations***

### NumSpark is a Python library that provides various mathematical operations and functionalities. It includes classes for handling arrays, vectors, complex numbers, and matrices, as well as a Statistics module for statistical calculations. The library also includes common mathematical functions like square root, exponent, logarithm, and trigonometric functions.

# ***Features***

### NumSpark library offers the following features:

- <p><b><h3>NumSparkArray: </h3></b>A class for handling arrays, supporting addition, subtraction, multiplication, and division operations. It also provides methods for calculating the length of the array.</p>
- <p><b><h3>Vector: </h3></b>A class for representing 3-dimensional vectors, allowing addition, subtraction, scalar multiplication, dot product, and cross product operations.</p>
- <p><b><h3>ComplexNumber: </h3></b>A class for handling complex numbers, supporting addition, subtraction, multiplication, division, and modulus calculations.</p>
- <p><b><h3>Matrix: </h3></b>A class for performing matrix operations, including addition, subtraction, scalar multiplication, matrix multiplication, transpose, adjoint, inverse, trace, and determinant.</p>
- <p><b><h3>Statistics: </h3></b>A module that provides statistical calculations such as mean, median, mode, variance, and standard deviation for a given dataset.</p>
- <p><b><h3>Mathematical Functions: </h3></b> NumSpark includes various mathematical functions such as square root, exponentiation, absolute value, logarithm (both natural and base-n), trigonometric functions (sine, cosine, tangent, cotangent, secant, and cosecant), and conversions between degrees and radians.</p>

# ***Installation***

### To use NumSpark

1. Make sure you have Python 3.x installed on your system.
2. Install NumSpark using pip:

    ```bash
    pip install numspark
    ```

# Usage
### <p>Below are some examples of how to use NumSpark library:</p>

```python
# Import the NumSpark classes and functions
from numspark import NumSparkArray, Vector, ComplexNumber, Matrix, Statistics, sqrt, log

# Create a NumSparkArray and perform operations
data = [1, 2, 3, 4, 5]
array = NumSparkArray(data)
array2 = array + 2
array3 = array * array2

# Create a Vector and perform operations
v1 = Vector(1, 2, 3)
v2 = Vector(4, 5, 6)
v3 = v1 + v2
dot_product = v1.dot(v2)

# Create a ComplexNumber and perform operations
z1 = ComplexNumber(2, 3)
z2 = ComplexNumber(1, 4)
z3 = z1 * z2
z4 = z1 / z2

# Create a Matrix and perform operations
matrix1 = Matrix([[1, 2], [3, 4]])
matrix2 = Matrix([[5, 6], [7, 8]])
matrix3 = matrix1 + matrix2
matrix4 = matrix1 * 2
matrix5 = matrix1 @ matrix2

# Use Statistics module to calculate mean, median, mode, variance, and standard deviation
data = [10, 20, 30, 40, 50]
mean_value = Statistics.mean(data)
median_value = Statistics.median(data)
mode_values = Statistics.mode(data)
variance = Statistics.variance(data)
std_deviation = Statistics.standard_deviation(data)

# Use mathematical functions
sqrt_result = sqrt(25)
log_result = log(100)

# Output the results
print(array)  # NumSparkArray([1, 2, 3, 4, 5])
print(array3) # NumSparkArray([3, 8, 15, 24, 35])

print(v3)  # Vector(5i 7j 9k)
print(dot_product)  # 32

print(z3)  # Re(-10), Img(11)
print(z4)  # Re(0.84), Img(-0.32)

print(matrix3)  # [[6, 8], [10, 12]]
print(matrix5)  # [[19, 22], [43, 50]]

print(mean_value)  # 30.0
print(median_value)  # 30
print(mode_values)  # [10, 20, 30, 40, 50]
print(variance)  # 250.0
print(std_deviation)  # 15.811388300841896

print(sqrt_result)  # 5.0
print(log_result)  # 2.0

```

# Contribution
### Contributions to the NumSpark library are welcome! If you find any issues or want to add new features, feel free to open a pull request or an issue on the GitHub repository.


# License
### This project is licensed under the MIT License - see the [LICENSE](https://github.com/Sahil-Rajwar-2004/NumSpark/blob/master/LICENSE) file for details.


# Acknowledgments
### NumSpark library is inspired by various mathematical concepts and aims to provide a simple and convenient way to perform mathematical operations in Python.
