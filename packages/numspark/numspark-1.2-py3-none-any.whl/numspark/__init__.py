PI = 3.1415926535897932384626433832795
E = 2.7182818284590452353602874713527
INFINITY= INF = inf = float("inf")
NAN = NaN = nan = float("nan")
TRUE = true = True
FALSE = false = False
NONE = NULL = none = null = None

from collections import Counter
import numpy as np
import sympy

class List:
    @staticmethod
    def element_wise_operation(*lists, operation):
        list_lengths = set(len(arg) for arg in lists)
        if not all(isinstance(arg, list) for arg in lists) or len(list_lengths) != 1:
            raise ValueError("All arguments must be lists with the same length for element-wise operations.")
        result = [lists[0][i] for i in range(len(lists[0]))]
        for i in range(len(result)):
            for arg in lists[1:]:
                result[i] = operation(result[i],arg[i])
        return result
    
    @staticmethod
    def product(*lists):
        return List.element_wise_operation(*lists,operation=lambda x,y: x*y)
    
    @staticmethod
    def scalarProduct(lst,scalar=1):
        if not isinstance(lst, list):
            raise ValueError("The first argument must be a list.")
        return [val*scalar for val in lst]

    @staticmethod
    def add(*lists):
        return List.element_wise_operation(*lists,operation=lambda x,y: x+y)
    
    @staticmethod
    def scalarAdd(lst,scalar=0):
        if not isinstance(lst,list):
            raise ValueError("The first argument must be a list.")
        return [val+scalar for val in lst]

    @staticmethod
    def sub(*lists):
        return List.element_wise_operation(*lists,operation=lambda x,y: x-y)
    
    @staticmethod
    def scalarSub(lst,scalar=0):
        if not isinstance(lst,list):
            raise ValueError("The first argument must be a list.")
        return [val-scalar for val in lst]

    @staticmethod
    def div(*lists):
        return List.element_wise_operation(*lists,operation=lambda x,y: x/y)
    
    @staticmethod
    def scalarDiv(lst,scalar=1):
        if not isinstance(lst,list):
            raise ValueError("The first argument must be a list.")
        return [val/scalar for val in lst]

    @staticmethod
    def floorDiv(*lists):
        return List.element_wise_operation(*lists,operation=lambda x,y: x//y)
    
    @staticmethod
    def scalarFloorDiv(lst,scalar=1):
        if not isinstance(lst,list):
            raise ValueError("The first argument must be a list.")
        return [val//scalar for val in lst]

    @staticmethod
    def modulo(*lists):
        return List.element_wise_operation(*lists,operation=lambda x,y: x%y)
    
    @staticmethod
    def scalarModulo(lst,scalar=1):
        if not isinstance(lst, list):
            raise ValueError("The first argument must be a list.")
        return [val%scalar for val in lst]
    
    @staticmethod
    def pow(lst,scalar=1):
        if not isinstance(lst, list):
            raise ValueError("The first argument must be a list.")
        return [val**scalar for val in lst]
    
    @staticmethod
    def flatten(lst):
        flattened_list = []
        for item in lst:
            if isinstance(item,list):
                flattened_list.extend(List.flatten(item))
            else:
                flattened_list.append(item)
        return flattened_list

class Vector:
    @staticmethod
    def add(*args):
        if any(len(vec) != 3 for vec in args):
            raise ValueError("All vectors should have 3 directions")
        result = [0,0,0]
        for vec in args:
            result[0] += vec[0]
            result[1] += vec[1]
            result[2] += vec[2]
        return result
    
    @staticmethod
    def sub(*args):
        if any(len(vec) != 3 for vec in args):
            raise ValueError("All vectors should have 3 directions")
        result = list(args[0])
        for vec in args[1:]:
            result[0] -= vec[0]
            result[1] -= vec[1]
            result[2] -= vec[2]
        return result

    @staticmethod
    def crossProduct(*args):
        if any(len(vec) != 3 for vec in args):
            raise ValueError("All vectors should have 3 directions")
        result = [0,0,0]
        for i in range(len(args)):
            for j in range(len(args)):
                if i == j:
                    continue
                result[0] += args[i][1] * args[j][2] - args[j][1] * args[i][2]
                result[1] += -1 * (args[i][0] * args[j][2] - args[j][0] * args[i][2])
                result[2] += args[i][0] * args[j][1] - args[j][0] * args[i][1]
        return result

    @staticmethod
    def dotProduct(*args):
        if any(len(vec) != 3 for vec in args):
            raise ValueError("All vectors should have 3 directions")
        result = [0,0,0]
        for vec in args:
            result[0] += vec[0]
            result[1] += vec[1]
            result[2] += vec[2]
        return result

    @staticmethod
    def magnitude(vector):
        if len(vector) != 3:
            raise ValueError("vector should have 3 directions")
        return sqrt(vector[0]**2+vector[1]**2+vector[2]**2)

    @staticmethod
    def projection(*args):
        if len(args) < 2:
            raise ValueError("At least two vectors are required for projection.")
        if any(len(vec) != 3 for vec in args):
            raise ValueError("All vectors should have 3 directions")
        dot_result = Vector.dotProduct(*args)
        mag_vector2 = Vector.magnitude(args[1])
        return dot_result/mag_vector2

    @staticmethod
    def angleOfProjection(*args):
        if len(args) < 2:
            raise ValueError("At least two vectors are required to calculate the angle of projection.")
        if any(len(vec) != 3 for vec in args):
            raise ValueError("All vectors should have 3 directions")
        dot_result = Vector.dotProduct(*args)
        mag_vector1 = Vector.magnitude(args[0])
        mag_vector2 = Vector.magnitude(args[1])
        cos_angle = dot_result/(mag_vector1*mag_vector2)
        angle_rad = np.arccos(cos_angle)
        angle_deg = np.degrees(angle_rad)
        return angle_deg

class Matrix:
    @staticmethod
    def isMatrix(matrix):
        if not isinstance(matrix, list):
            return false
        num_columns = len(matrix[0]) if matrix else NULL
        for row in matrix:
            if not isinstance(row, list) or len(row) != num_columns:
                return false
        return true
    
    @staticmethod
    def isSquare(matrix):
        if not Matrix.isMatrix(matrix):
            raise ValueError("Error: given nested list isn't in the form of matrix")
        if len(matrix) != len(matrix[0]):
            return false
        return true

    @staticmethod
    def add(*matrices):
        for matrix in matrices:
            if not Matrix.isMatrix(matrix):
                raise ValueError("Error: given nested list isn't in the form of matrix")
        if len(set(len(matrix) for matrix in matrices)) != 1 or len(set(len(row) for matrix in matrices for row in matrix)) != 1:
            raise ValueError("All matrices must have the same dimensions for addition.")
        result = [[sum(matrix[i][j] for matrix in matrices) for j in range(len(matrices[0][i]))] for i in range(len(matrices[0]))]
        return result
    
    @staticmethod
    def scalarAdd(matrix,scalar=0):
        if not Matrix.isMatrix(matrix):
            raise ValueError("Error: given nested list isn't in the form of matrix")
        result = [[matrix[i][j]+scalar for j in range(len(matrix[i]))] for i in range(len(matrix))]
        return result
    
    @staticmethod
    def sub(*matrices):
        for matrix in matrices:
            if not Matrix.isMatrix(matrix):
                raise ValueError("Error: given nested list isn't in the form of matrix")
        if len(set(len(matrix) for matrix in matrices)) != 1 or len(set(len(row) for matrix in matrices for row in matrix)) != 1:
            raise ValueError("All matrices must have the same dimensions for subtraction.")
        result = [[matrices[0][i][j]-sum(matrix[i][j] for matrix in matrices[1:]) for j in range(len(matrices[0][i]))] for i in range(len(matrices[0]))]
        return result
    
    @staticmethod
    def scalarSub(matrix,scalar=0):
        if not Matrix.isMatrix(matrix):
            raise ValueError("Error: given nested list isn't in the form of matrix")
        result = [[matrix[i][j]-scalar for j in range(len(matrix[i]))] for i in range(len(matrix))]
        return result
    
    @staticmethod
    def product(*matrices):
        for matrix in matrices:
            if not Matrix.isMatrix(matrix):
                raise ValueError("Error: given nested list isn't in the form of matrix")
        if len(set(len(matrix[0]) for matrix in matrices)) != 1:
            raise ValueError("Number of columns in all matrices must be equal for multiplication.")
        result = matrices[0]
        for matrix in matrices[1:]:
            if len(matrix) != len(result[0]):
                raise ValueError("Number of rows in the second matrix must be equal to the number of columns in the first matrix for multiplication.")
            result = [[sum(result[i][k] * matrix[k][j] for k in range(len(result[0]))) for j in range(len(matrix[0]))] for i in range(len(result))]
        return result
    
    @staticmethod
    def scalarProduct(matrix,scalar=1):
        if not Matrix.isMatrix(matrix):
            raise ValueError("Error: given nested list isn't in the form of matrix")
        result = [[matrix[i][j] * scalar for j in range(len(matrix[i]))] for i in range(len(matrix))]
        return result
    
    @staticmethod
    def T(matrix):
        if not Matrix.isMatrix(matrix):
            raise ValueError("Error: given nested list isn't in the form of matrix")
        result = [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]
        return result
    
    @staticmethod
    def subMatrix(matrix,row,col):
        if not Matrix.isMatrix(matrix):
            raise ValueError("Error: given nested list isn't in the form of matrix")
        return [matrix[i][:col] + matrix[i][col+1:] for i in range(len(matrix)) if i != row]
    
    @staticmethod
    def det(matrix):
        if not Matrix.isMatrix(matrix):
            raise ValueError("Error: given nested list isn't in the form of matrix")
        if not Matrix.isSquare(matrix):
            raise ValueError("Error: given matrix isn't a square matrix")
        if len(matrix) != len(matrix[0]):
            raise ValueError("The matrix must be square for determinant calculation.")
        if len(matrix) == 1:
            return matrix[0][0]
        if len(matrix) == 2:
            return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
        det = 0
        for j in range(len(matrix[0])):
            sign = (-1) ** j
            minor = Matrix.subMatrix(matrix, 0, j)
            det += sign*matrix[0][j]*Matrix.det(minor)
        return det

    @staticmethod
    def cofactor(matrix):
        if not Matrix.isMatrix(matrix):
            raise ValueError("Error: given nested list isn't in the form of matrix")
        if not Matrix.isSquare(matrix):
            raise ValueError("Error: given matrix isn't a square matrix")
        cofactors = [[(-1) ** (i + j) * Matrix.det(Matrix.subMatrix(matrix, i, j)) for j in range(len(matrix[0]))] for i in range(len(matrix))]
        return cofactors

    @staticmethod
    def adjoint(matrix):
        if not Matrix.isMatrix(matrix):
            raise ValueError("Error: given nested list isn't in the form of matrix")
        if not Matrix.isSquare(matrix):
            raise ValueError("Error: given matrix isn't a square matrix")
        cofactors = Matrix.cofactor(matrix)
        return Matrix.T(cofactors)

    @staticmethod
    def inv(matrix):
        if not Matrix.isMatrix(matrix):
            raise ValueError("Error: given nested list isn't in the form of matrix")
        if not Matrix.isSquare(matrix):
            raise ValueError("Error: given matrix isn't a square matrix")
        det = Matrix.det(matrix)
        if det == 0:
            raise ValueError("Matrix is not invertible (non-singular).")
        adj = Matrix.adjoint(matrix)
        inv = Matrix.scalarProduct(adj,1/det)
        return inv
    
    @staticmethod
    def traces(matrix):
        if not Matrix.isMatrix(matrix):
            raise ValueError("input should be a matrix")
        if not Matrix.isSquare(matrix):
            raise ValueError("matrix should have same number of rows and cols")
        trace = 0
        for x in range(len(matrix)):
            trace += matrix[x][x]
        return trace
    
    @staticmethod
    def diagonalSum(matrix):
        if not Matrix.isMatrix(matrix):
            raise ValueError("input should be a matrix")
        if not Matrix.isSquare(matrix):
            raise ValueError("matrix should have same number of rows and cols")
        total = 0
        for x in range(len(matrix)):
            total += matrix[x][x]
            total += matrix[len(matrix)-x-1][x]
        if len(matrix)%2 != 0:
            total -= matrix[int(len(matrix)/2)][int(len(matrix)/2)]
        return total
    
    def removeCol(matrix,column):
        if not Matrix.isMatrix(matrix):
            raise ValueError("input should be a matrix")
        for rows in matrix:
            rows.remove(rows[column])
        return matrix
    
    def removeRow(matrix,row):
        if not Matrix.isMatrix(matrix):
            raise ValueError("input should be a matrix")
        matrix.remove(matrix[row])
        return matrix
    
    def reciprocal(matrix):
        if not Matrix.isMatrix(matrix):
            raise ValueError("input should be a matrix")
        for rows in matrix:
            for x in range(len(rows)):
                rows[x] = 1/rows[x]
        return matrix
    
class Set:
    @staticmethod
    def toSet(lst):
        return list(dict.fromkeys(lst))

    @staticmethod
    def intersect(*lists):
        if not lists:
            return []
        smallest_list = min(lists, key=len)
        result = list(smallest_list)
        for lst in lists:
            result = [element for element in result if element in list(set(lst))]
        return set(Set.toSet(result))
    
    @staticmethod
    def union(*lists):
        if not lists:
            return []
        result = []
        for lst in lists:
            for element in lst:
                if element not in result:
                    result.append(element)
        return set(Set.toSet(result))
    
    @staticmethod
    def belongsTo(element,lst):
        return element in lst

    @staticmethod
    def subSet(set1,set2):
        return all(element in set2 for element in set1)


def max(array):
    val = -INFINITY
    for x in array:
        if val < x:
            val = x
    return val

def min(array):
    val = INFINITY
    for x in array:
        if val > x:
            val = x
    return val

def sin(angle,unit="rad"):
    if unit == "deg":
        angle = deg2rad(angle)
    elif unit == "rad":
        if angle > PI:
            angle -= 2*PI
    else:
        raise ValueError(f"Invalid argument: expected rad or deg but got {unit}")
    sinx = 0
    term = angle
    i = 1
    while abs(term) > 1e-3:
        sinx += term
        term *= -1*angle**2/((2*i)*(2*i+1))
        i += 1
    return round(sinx,4)

def cos(angle,unit="rad"):
    if unit == "deg":
        angle = deg2rad(angle)
    elif unit == "rad":
        if angle > PI:
            angle -= 2*PI
    else:
        raise ValueError(f"Invalid argument: expected rad or deg but got {unit}")
    cosx = 1
    term = 1
    i = 1
    while abs(term) > 1e-10:
        term *= -1*angle**2/((2*i-1)*2*i)
        cosx += term
        i += 1
    return round(cosx,4)

def tan(angle,unit):
    if cos(angle,unit) == 0:
        raise ValueError(f"tan({angle}) isn't defined at rad({angle})")
    return sin(angle,unit)/cos(angle,unit)

def cot(angle,unit):
    if sin(angle,unit) == 0:
        raise ValueError(f"cot({angle}) isn't defined at rad({angle})")
    return cos(angle,unit)/sin(angle,unit)

def cosec(angle,unit):
    if sin(angle,unit) == 0:
        raise ValueError(f"cosec({angle}) isn't defined at rad({angle})")
    return 1/sin(angle,unit)

def sec(angle,unit):
    if cos(angle,unit) == 0:
        raise ValueError(f"sec({angle}) isn't defined at rad({angle})")
    return 1/cos(angle,unit)

def acos(angle):
    return np.arccos(angle)

def asin(angle):
    return np.arcsin(angle)

def atan(angle):
    return np.arctan(angle)

def acot(angle):
    return np.arcsin(angle)/np.arccos(angle)

def acosec(angle):
    return 1/np.arcsin(angle)

def asec(angle):
    return 1/np.arccos(angle)

def bubbleSort(array):
    for i in range(len(array)):
        for j in range(0,len(array)-i-1):
            if array[j] > array[j+1]:
                array[j],array[j+1] = array[j+1],array[j]
    return array

def quickSort(array):
    if len(array) <= 1:
        return array
    pivot = array[len(array)//2]
    left = [x for x in array if x < pivot]
    middle = [x for x in array if x == pivot]
    right = [x for x in array if x > pivot]
    return quickSort(left)+middle+quickSort(right)

def descendingSort(array):
    for i in range(len(array)):
        for j in range(i+1,len(array)):
            if array[j] > array[i]:
                array[i],array[j] = array[j],array[i]
    return array

def deg2rad(deg):
    return deg*PI/180

def rad2deg(rad):
    return rad*180/PI

def sqrt(number, precision=1e-6):
    if number < 0:
        raise ValueError("Square root is not defined for negative numbers.")
    if number == 0:
        return 0
    x = number
    while abs(x*x-number) > precision:
        x = (x+number/x)/2
    return x

def cbrt(number,precision=1e-6):
    x = number
    while abs(x*x*x-number) > precision:
        x = x-(x*x*x-number)/(3*x*x)
    return x

def power(base,exponent=1):
    return base**exponent

def exp(x=1):
    return E**x

def factorial(number):
    if number == 0:
        return 1
    elif number < 0:
        raise ValueError("number can't be negative!")
    return number*factorial(number-1)

def fibSequence(number):
    seq = [0,1]
    if number <= 0:
        raise ValueError("number can't be negative!")
    elif number == 1:
        return seq[0]
    elif number == 2:
        return seq[1]
    else:
        for i in range(2,number):
            next_int = seq[i-1]+seq[i-2]
            seq.append(next_int)
    return seq

def floor(number):
    if number == int(number):
        return int(number)
    if number < 0:
        return int(number)-1
    return int(number)

def ceil(number):
    if number == int(number):
        return int(number)
    if number < 0:
        return int(number)-1
    return int(number)+1

def quadratic_roots(coefficients):
    if len(coefficients) != 3:
        raise ValueError("there should be only 3 coefficients!")
    D = coefficients[0]**2-4*coefficients[0]*coefficients[2]
    if D < 0:
        x1 = -coefficients[1] + sqrt(abs(D))
        x2 = -coefficients[1] - sqrt(abs(D))
        return [x1,x2]
    x1 = -coefficients[1]+sqrt(D)
    x2 = -coefficients[1]-sqrt(D)
    return [x1,x2]

def log(number):
    if number <= 0:
        raise ValueError("domain error")
    else:
        n = 0
        while number >= 10:
            number /= 10
            n += 1
        if number == 1:
            return n
        else:
            left,right = 0,1
            while number < 1:
                left -= 1
                right -= 1
                number *= 10
            for _ in range(100):
                mid = (left+right)/2
                if 10**mid < number:
                    left = mid
                else:
                    right = mid
            return n+left

def ln(number):
    if number <= 0:
        raise ValueError("domain error")
    return 2.303*log(number)

def logn(number,base = E):
    if number <= 0 or base <= 0 or base == 1:
        raise ValueError("domain error")
    return 2.303*log(number)/(2.303*log(base))

def permutation(n,r):
    return factorial(n)/factorial(n-r)

def combination(n,r):
    return factorial(n)/(factorial(r)*factorial(n-r))

def product(array):
    result = 1
    for x in array:
        result *= x
    return result

def summation(array):
    total = 0
    for x in array:
        total += x
    return total

def mean(array:list):
    return sum(array)/len(array)

def median(array:list):
    sorted_numbers = quickSort(array)
    n = len(sorted_numbers)
    if n%2 == 0:
        middle_right_index = n // 2
        middle_left_index = middle_right_index - 1
        median = (sorted_numbers[middle_left_index]+sorted_numbers[middle_right_index])/2.0
    else:
        middle_index = n // 2
        median = sorted_numbers[middle_index]
    return median

def mode(array:list):
    counts = Counter(array)
    freq = max(counts.values())
    modes = [number for number,count in counts.items() if count == freq]
    return modes

def variance(array:list,kind:str="sample"):
    if kind == "sample":
        d = len(array)-1
    elif kind == "population":
        d = len(array)
    else:
        raise ValueError(f"invalid input {kind}! input should be whether 'population' or 'sample'")
    return summation((x - mean(array))**2 for x in array)/(d)

def standard_deviation(array:list,kind:str="sample"):
    return sqrt(variance(array,kind))

def skewness(array:list):
    if len(array) == 0:
        raise ValueError("length of an array shouldn't be 0")
    return summation((x-mean(array))**3 for x in array)/(len(array)*standard_deviation(array,"population")**3)

def kurtosis(array:list):
    if len(array) == 0:
        raise ValueError("length of an array shouldn't be 0")
    moment = summation((x-mean(array))**4 for x in array)/len(array)
    return (moment/variance(array)**2)-3

def geometric_mean(array:list):
    return product(array)**(1/len(array))

def harmonic_mean(array:list):
    t = 0
    for x in array:
        if x == 0:
            return INFINITY
        t += 1/x
    return len(array)/t

def correlation_coefficient(x:list,y:list):
    if len(x) != len(y):
        raise ValueError("length of x and y aren't the same!")
    xsum = summation(x)
    ysum = summation(y)
    xysum = summation([x[i]*y[i] for i in range(len(x))])
    xsqrsum = summation([x[i]**2 for i in range(len(x))])
    ysqrsum = summation([y[i]**2 for i in range(len(y))])
    n = len(x)*xysum-xsum*ysum
    d = sqrt((len(x)*xsqrsum-xsum**2)*(len(x)*ysqrsum-ysum**2))
    if d == 0:
        return 0
    return n/d

def slope_intercept(array1:list,array2:list):
    if len(array1) != len(array2):
        raise ValueError("the size of array aren't the same!")
    xmean = mean(array1)
    ymean = mean(array2)
    xdiff = [x-xmean for x in array1]
    ydiff = [y-ymean for y in array2]
    slope = summation([xdiff[i]*ydiff[i] for i in range(len(array1))])/summation([d**2 for d in xdiff])
    intercept = ymean-slope*xmean
    return [slope,intercept]

def moving_average(array:list,steps:int):
    if steps <= 0:
        raise ValueError(f"steps must be greater than zero {steps} < {0}")
    if len(array) < steps:
        raise ValueError(f"invalid input {steps} > {len(array)}! array must have atleast as many elements as the number of steps!")
    avgs = []
    for i in range(len(array)-steps+1):
        subset = array[i:i+steps]
        avgs.append(sum(subset)/steps)
    return avgs

def exponential_moving_average(array:list,alpha:int|float):
    if 0 <= alpha <= 1:
        ema = [array[0]]
        for x in range(1,len(array)):
            ema.append(alpha*array[x]+(1-alpha)*ema[x-1])
        return ema
    else:
        raise ValueError("invalid input! the value of alpha should lie between 0 and 1 included")
    
def mean_sqrd_error(actual:list,predicted:list):
    if len(actual) != len(predicted):
        raise ValueError("length of actual and predicted data aren't equal!")
    errors = [(actual[i]-predicted[i])**2 for i in range(len(actual))]
    return summation(errors)/len(actual)

def root_mean_sqrd_error(actual:list,predicted:list):
    return sqrt(mean_sqrd_error(actual,predicted))

def errors(actual:list,predicted:list):
    if len(actual) != len(predicted):
        raise ValueError("length of actual and predicted data aren't equal!")
    return [actual[x]-predicted[x] for x in range(len(actual))]

def mean_error(actual:list,predicted:list):
    return mean(errors(actual,predicted))

def power(base:int|float,exponent:int|float):
    return base**exponent

def power_sum(array:list,exponent:int|float):
    return summation(power_array(array,exponent))

def power_array(array:list,exponent:int|float):
    return [x**exponent for x in array]

def primes(limit:int):
    if limit <= 0:
        raise ValueError("limit must be greater than zero")
    primes = []
    for x in range(2,limit):
        is_prime = True
        for i in range(2,int(sqrt(x))+1):
            if x%i == 0:
                is_prime = FALSE
                break
        if is_prime:
            primes.append(x)
    return primes

def isprime(number:int):
    if number < 2:
        return False
    for x in range(2,int(sqrt(number))+1):
        if number%x == 0:
            return FALSE
    return TRUE

def cost_function(actual:list,predicted:list):
    if len(actual) != len(predicted):
        raise ValueError("length of actual and predicted data aren't equal!")
    errors = [(actual[i]-predicted[i])**2 for i in range(len(actual))]
    return summation(errors)/(2*len(actual))

def scaling(array:list,feature_range:tuple = (0,1)):
    min_val = min(array)
    max_val = max(array)
    scaled_data = [(val - min_val)/(max_val - min_val)*(feature_range[1]-feature_range[0])+feature_range[0] for val in array]
    return scaled_data

def gaussian(array:list):
    result = []
    std_dev = standard_deviation(array)
    m = mean(array)
    for x in array:
        each = (1/(std_dev*sqrt(2*PI)))*exp(-((x-m)**2)/(2*(std_dev**2)))
        result.append(each)
    return result

def sigmoid(x:int):
    return 1/(1+E**(-x))

def zscore(array:list,number:int) -> int|float:
    return (number-mean(array))*standard_deviation(array)

def euclidean_distance(array1:list,array2:list):
    if len(array1) < 3 or len(array2) < 3:
        raise ValueError("arrays must have the same length and have atleast 3 coordinates both x and y")
    return sqrt(summation([(array1[x] - array2[x])**2 for x in range(len(array1))]))

def manhattan_distance(array1:list,array2:list):
    if len(array1) < len(array2) < 3:
        raise ValueError("arrays must have the same length and have atleast 3 coordinates both x and y")
    return summation([abs(array1[x] - array2[x]) for x in range(len(array1))])

def camberra_distance(array1:list,array2:list):
    if len(array1) < len(array2) < 3:
        raise ValueError("arrays must have the same length and have atleast 3 coordinates both x and y")
    return summation([abs(array1[x] - array2[x])/(abs(array1[x] + array2[x])) for x in range(len(array1))])

def integrate(expression:str,wrt:str="x"):
    expr = sympy.sympify(expression)
    integral = sympy.integrate(expr,wrt)
    return integral

def derivate(expression:str,wrt:str="x"):
    expr = sympy.sympify(expression)
    diff = sympy.diff(expr,wrt)
    return diff
