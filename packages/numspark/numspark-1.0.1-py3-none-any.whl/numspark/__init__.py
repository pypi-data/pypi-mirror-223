PI = 3.1415926535897932384626433832795
E = 2.7182818284590452353602874713527
INFINITY = float("inf")
NAN = float("nan")
TRUE = true = True
FALSE = false = False


class NumSparkArray:
    def __init__(self, data):
        if isinstance(data, (list,tuple)):
            self.data = data
        else:
            raise TypeError("Input data must be a list or tuple")

    def __repr__(self):
        return f"NumSparkArray({self.data})"

    def __getitem__(self, index):
        return self.data[index]

    def __setitem__(self, index, value):
        self.data[index] = value

    def __add__(self, other):
        if isinstance(other,(int,float)):
            result = [x+other for x in self.data]
            return NumSparkArray(result)
        elif isinstance(other, NumSparkArray) and len(self.data) == len(other.data):
            result = [x+y for x,y in zip(self.data, other.data)]
            return NumSparkArray(result)
        else:
            raise ValueError("Both arrays must have the same length")

    def __sub__(self, other):
        if isinstance(other,(int,float)):
            result = [x-other for x in self.data]
            return NumSparkArray(result)
        elif isinstance(other, NumSparkArray) and len(self.data) == len(other.data):
            result = [x-y for x,y in zip(self.data, other.data)]
            return NumSparkArray(result)
        else:
            raise ValueError("Both arrays must have the same length")

    def __mul__(self, other):
        if isinstance(other,(int,float)):
            result = [x*other for x in self.data]
            return NumSparkArray(result)
        elif isinstance(other,NumSparkArray) and len(self.data) == len(other.data):
            result = [x*y for x,y in zip(self.data,self.data)]
            return NumSparkArray(result)
        else:
            raise ValueError("Both arrays must have the same length")

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        if isinstance(other,(int,float)):
            result = [x/other for x in self.data]
            return NumSparkArray(result)
        elif isinstance(other,NumSparkArray) and len(self.data) == len(other.data):
            result = [x/y for x,y in zip(self.data,self.data)]
            return NumSparkArray(result)
        else:
            raise ValueError("Both arrays must have the same length")

    def length(self):
        count = 0
        for x in zip(self.data):
            count += 1
        return count

class Vector:
    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return f"Vector({self.x}i {self.y}j {self.z}k)"
    
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar, self.z * scalar)

    def __rmul__(self, scalar):
        return self.__mul__(scalar)

    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other):
        cross_x = self.y * other.z - self.z * other.y
        cross_y = self.z * other.x - self.x * other.z
        cross_z = self.x * other.y - self.y * other.x
        return Vector(cross_x, cross_y, cross_z)

    def magnitude(self):
        return sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

class ComplexNumber:
    def __init__(self, real, imag):
        self.real = real
        self.imag = imag

    def __repr__(self):
        return f"Re({self.real}), Img({self.imag})"

    def __add__(self, other):
        return ComplexNumber(self.real + other.real, self.imag + other.imag)

    def __sub__(self, other):
        return ComplexNumber(self.real - other.real, self.imag - other.imag)

    def __mul__(self, other):
        real_part = self.real * other.real - self.imag * other.imag
        imag_part = self.real * other.imag + self.imag * other.real
        return ComplexNumber(real_part, imag_part)

    def __truediv__(self, other):
        denominator = other.real ** 2 + other.imag ** 2
        real_part = (self.real * other.real + self.imag * other.imag) / denominator
        imag_part = (self.imag * other.real - self.real * other.imag) / denominator
        return ComplexNumber(real_part, imag_part)

    def modulus(self):
        return sqrt(self.real ** 2 + self.imag ** 2)

    def conjugate(self):
        return ComplexNumber(self.real, -self.imag)
    
class Matrix:
    def __init__(self, matrix):
        self.matrix = matrix
        self.rows = len(matrix)
        self.cols = len(matrix[0])

    def __repr__(self):
        return str(self.matrix)

    def __add__(self, other):
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrices must have the same dimensions for addition.")
        result = [[self.matrix[i][j] + other.matrix[i][j] for j in range(self.cols)] for i in range(self.rows)]
        return Matrix(result)

    def __sub__(self, other):
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrices must have the same dimensions for subtraction.")
        result = [[self.matrix[i][j] - other.matrix[i][j] for j in range(self.cols)] for i in range(self.rows)]
        return Matrix(result)

    def __mul__(self, scalar):
        result = [[self.matrix[i][j] * scalar for j in range(self.cols)] for i in range(self.rows)]
        return Matrix(result)

    def __rmul__(self, scalar):
        return self.__mul__(scalar)

    def __matmul__(self, other):
        if self.cols != other.rows:
            raise ValueError("Number of columns of the first matrix must be equal to the number of rows of the second matrix.")
        result = [[sum(self.matrix[i][k] * other.matrix[k][j] for k in range(self.cols)) for j in range(other.cols)] for i in range(self.rows)]
        return Matrix(result)

    def transpose(self):
        result = [[self.matrix[j][i] for j in range(self.rows)] for i in range(self.cols)]
        return Matrix(result)
    
    def adjoint(self):
        if self.rows != self.cols:
            raise ValueError("The matrix must be square to calculate the adjoint.")
        adjoint_matrix = [[self.cofactor(j, i) for j in range(self.cols)] for i in range(self.rows)]
        return Matrix(adjoint_matrix)

    def inverse(self):
        if self.rows != self.cols:
            raise ValueError("The matrix must be square to calculate the inverse.")
        determinant = self.determinant()
        if determinant == 0:
            raise ValueError("The matrix is singular and does not have an inverse.")
        adjoint_matrix = self.adjoint()
        inverse_matrix = (1 / determinant) * adjoint_matrix
        return inverse_matrix

    def trace(self):
        if self.rows != self.cols:
            raise ValueError("The matrix must be square to calculate the trace.")
        return sum(self.matrix[i][i] for i in range(self.rows))

    def cofactor(self, row, col):
        minor = [[self.matrix[i][j] for j in range(self.cols) if j != col] for i in range(self.rows) if i != row]
        return (-1) ** (row + col) * Matrix(minor).determinant()

    def determinant(self):
        if self.rows != self.cols:
            raise ValueError("The matrix must be square to calculate the determinant.")
        if self.rows == 1:
            return self.matrix[0][0]
        if self.rows == 2:
            return self.matrix[0][0] * self.matrix[1][1] - self.matrix[0][1] * self.matrix[1][0]
        determinant = 0
        for j in range(self.cols):
            determinant += self.matrix[0][j] * self.cofactor(0, j)
        return determinant


class Statistics:
    @staticmethod
    def mean(data):
        if not data:
            raise ValueError("Data list is empty")
        return sum(data)/len(data)
    
    @staticmethod
    def median(data):
        if not data:
            raise ValueError("Data list is empty.")
        sorted_data = sorted(data)
        n = len(sorted_data)
        if n%2 == 1:
            return sorted_data[n//2]
        else:
            mid1 = sorted_data[(n//2)-1]
            mid2 = sorted_data[n//2]
            return (mid1+mid2)/2

    @staticmethod
    def mode(data):
        if not data:
            raise ValueError("Data list is empty.")
        data_count = {}
        for num in data:
            data_count[num] = data_count.get(num,0)+1
        max_count = max(data_count.values())
        mode_values = [num for num, count in data_count.items() if count == max_count]
        return mode_values

    @staticmethod
    def variance(data,kind="population"):
        if not data:
            raise ValueError("Data list is empty.")
        mean_val = Statistics.mean(data)
        squared_diff = [(x - mean_val)**2 for x in data]
        if kind == "sample":
            return sum(squared_diff)/(len(data)-1)
        return sum(squared_diff)/len(data)
    
    @staticmethod
    def standard_deviation(data,kind="population"):
        return sqrt(Statistics.variance(data,kind=kind))


def sqrt(number,precise=1e-10):
    guess = number
    while abs(guess*guess-number) > precise:
        guess = (guess+number/guess) / 2
    return guess

def cbrt(number,precise=1e-10):
    if number >= 0:
        guess = number
    else:
        guess = -number
    while abs(guess ** 3 - number) > precise:
        guess = (2 * guess + number / (guess ** 2)) / 3
    if number < 0:
        guess = -guess
    return guess

def factorial(number):
    if number == 0:
        return 1
    else:
        return number * factorial(number-1)
    
def deg2rad(angle):
    return angle*PI/180

def rad2deg(angle):
    return angle*180/PI
    
def exp(number):
    return E**number

def power(base,exponent):
    return base**exponent

def absolute(number):
    if number < 0:
        return -number
    return number

def sin(angle,unit="rad"):
    angle %= 2*PI
    if angle > PI:
        angle -= 2*PI
    sinx = 0
    term = angle
    i = 1
    while absolute(term) > 1e-10:
        sinx += term
        term *= -1*angle**2/((2*i)*(2*i+1))
        i += 1
    return sinx

def cos(angle):
    angle %= 2*PI
    if angle > PI:
        angle -= 2*PI
    cosx = 1
    term = 1
    i = 1
    while absolute(term) > 1e-10:
        term *= -1*angle**2/((2*i-1)*2*i)
        cosx += term
        i += 1
    return cosx

def tan(angle):
    if cos(angle) == 0:
        raise ValueError(f"tan({angle}) isn't defined at rad({angle})")
    return sin(angle)/cos(angle)

def cot(angle):
    if sin(angle) == 0:
        raise ValueError(f"tan({angle}) isn't defined at rad({angle})")
    return cos(angle)/sin(angle)

def sec(angle):
    if cos(angle) == 0:
        raise ValueError(f"sec({angle}) isn't defined at rad({angle})")
    return 1/cos(angle)

def cosec(angle):
    if sin(angle) == 0:
        raise ValueError(f"sec({angle}) isn't defined at rad({angle})")
    return 1/sin(angle)

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

def logn(number,base=E):
    if number <= 0 or base <= 0 or base == 1:
        raise ValueError("domain error")
    return 2.303*log(number)/(2.303*log(base))