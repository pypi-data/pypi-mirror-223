# improved_math.py

import math

class ImprovedMath:
    class Arithmetic:
        @staticmethod
        def factorial_recursive(n):
            """Calculate the factorial of a non-negative integer n using recursion."""
            if n < 0:
                raise ValueError("Factorial is not defined for negative numbers.")
            elif n == 0:
                return 1
            else:
                return n * ImprovedMath.Arithmetic.factorial_recursive(n - 1)

        @staticmethod
        def gcd(a, b):
            """Calculate the greatest common divisor (GCD) of two integers using Euclid's algorithm."""
            while b:
                a, b = b, a % b
            return abs(a)

        @staticmethod
        def lcm(a, b):
            """Calculate the least common multiple (LCM) of two integers."""
            return abs(a * b) // ImprovedMath.Arithmetic.gcd(a, b)

        @staticmethod
        def is_prime(n):
            """Check if a positive integer n is a prime number."""
            if n < 2:
                return False
            for i in range(2, int(math.sqrt(n)) + 1):
                if n % i == 0:
                    return False
            return True

        @staticmethod
        def factorial_iterative(n):
            """Calculate the factorial of a non-negative integer n using iteration."""
            if n < 0:
                raise ValueError("Factorial is not defined for negative numbers.")
            result = 1
            for i in range(1, n + 1):
                result *= i
            return result

    class Geometry:
        @staticmethod
        def area_of_circle(radius):
            """Calculate the area of a circle with the given radius."""
            return math.pi * radius ** 2

        @staticmethod
        def area_of_triangle(base, height):
            """Calculate the area of a triangle with the given base and height."""
            return 0.5 * base * height

        @staticmethod
        def area_of_square(side):
            """Calculate the area of a square with the given side length."""
            return side ** 2

        @staticmethod
        def area_of_rectangle(length, width):
            """Calculate the area of a rectangle with the given length and width."""
            return length * width

        @staticmethod
        def perimeter_of_circle(radius):
            """Calculate the perimeter of a circle with the given radius."""
            return 2 * math.pi * radius

        @staticmethod
        def perimeter_of_triangle(side1, side2, side3):
            """Calculate the perimeter of a triangle with the given side lengths."""
            return side1 + side2 + side3

        # Add more geometry functions here

    class Algebra:

        # Add more algebra functions here
        @staticmethod
        def quadratic_formula(a, b, c):
            """Calculate the roots of a quadratic equation of the form ax^2 + bx + c = 0."""
            discriminant = b**2 - 4*a*c
            if discriminant < 0:
                return None
            elif discriminant == 0:
                root = -b / (2 * a)
                return root, root
            else:
                root1 = (-b + math.sqrt(discriminant)) / (2 * a)
                root2 = (-b - math.sqrt(discriminant)) / (2 * a)
                return root1, root2

        @staticmethod
        def linear_equation(x, m, c):
            """Calculate the value of y for a given x in a linear equation y = mx + c."""
            return m * x + c

        @staticmethod
        def quadratic_equation(x, a, b, c):
            """Calculate the value of y for a given x in a quadratic equation y = ax^2 + bx + c."""
            return a * x**2 + b * x + c

        @staticmethod
        def nth_term_arithmetic_sequence(a, d, n):
            """Calculate the nth term of an arithmetic sequence."""
            return a + (n - 1) * d

        @staticmethod
        def nth_term_geometric_sequence(a, r, n):
            """Calculate the nth term of a geometric sequence."""
            return a * r**(n - 1)

        # Add more algebra functions here

    class Calculus:
        @staticmethod
        def differentiate_polynomial(coefficients, x):
            """Differentiate a polynomial with given coefficients at a given point x."""
            degree = len(coefficients) - 1
            result = 0
            for i, coef in enumerate(coefficients):
                result += coef * (x ** (degree - i))
            return result

        @staticmethod
        def integrate_polynomial(coefficients, a, b):
            """Integrate a polynomial with given coefficients between the limits a and b."""
            degree = len(coefficients) - 1
            result = 0
            for i, coef in enumerate(coefficients):
                result += coef / (degree - i + 1) * (b ** (degree - i + 1) - a ** (degree - i + 1))
            return result

        # Add more calculus functions here

    class Statistics:
        @staticmethod
        def mean(data):
            """Calculate the mean (average) of a list of numbers."""
            return sum(data) / len(data)

        @staticmethod
        def median(data):
            """Calculate the median of a list of numbers."""
            sorted_data = sorted(data)
            n = len(sorted_data)
            if n % 2 == 0:
                mid = n // 2
                return (sorted_data[mid - 1] + sorted_data[mid]) / 2
            else:
                return sorted_data[n // 2]

        @staticmethod
        def variance(data):
            """Calculate the variance of a list of numbers."""
            mean_value = ImprovedMath.Statistics.mean(data)
            return sum((x - mean_value) ** 2 for x in data) / len(data)

        @staticmethod
        def standard_deviation(data):
            """Calculate the standard deviation of a list of numbers."""
            return math.sqrt(ImprovedMath.Statistics.variance(data))

        # Add more statistics functions here