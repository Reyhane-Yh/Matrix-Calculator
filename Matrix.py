from fractions import Fraction
import copy

class Matrix:
    def __init__(self, matrix=[[]]):
        self.matrix = matrix
        self.rows = len(self.matrix)
        self.cols = len(self.matrix[0])

    def __str__(self):
        matrix = ""
        for row in self.matrix:
            for i in range(len(row)):
                matrix += str(row[i]) + " "
            matrix += "\n"

        return matrix[:-1]

    def __add__(self, other):
        sum = Matrix()

        for i in range(len(self.matrix)):
            for j in range(self.cols):
                sum.matrix[i].append(self.matrix[i][j] + other.matrix[i][j])

            if i < len(self.matrix) - 1:
                sum.matrix.append([])
        return sum

    def __sub__(self, other):
        sub = Matrix()

        for i in range(len(self.matrix)):
            for j in range(self.cols):
                sub.matrix[i].append(self.matrix[i][j] - other.matrix[i][j])

            if i < len(self.matrix) - 1:
                sub.matrix.append([])
        return sub

    def __mul__(self, other):
        mul = Matrix([[0 for i in range(other.cols)] for j in range(self.rows)])

        for i in range(self.rows):
            for j in range(other.cols):
                mul.matrix[i][j] = 0
                for k in range(self.cols):
                    mul.matrix[i][j] += self.matrix[i][k] * other.matrix[k][j]

        return mul

    def get_row(self, n):
        print(*self.matrix[n])

    def get_col(self, n):
        for row in self.matrix:
            print(row[n])

    def get_block(self, p1, p2):
        matrix = ""
        for i in range(int(p1[0]), int(p2[0]) + 1):
            for j in range(int(p1[1]), int(p2[1]) + 1):
                matrix += str(self.matrix[i][j]) + " "
            matrix += "\n"

        print(matrix[:-1])

    def change_rows(self, first, second):
        self.matrix[first], self.matrix[second] = self.matrix[second], self.matrix[first]
        return self

    def multiply(self, num, row):
        for i in range(self.cols):
            self.matrix[row][i] *= num

        return self

    def sum(self, first, second, t):
        for i in range(self.cols):
            self.matrix[second][i] += self.matrix[first][i] * t

        return self

    def rref(self):
        col = 0

        for row in range(self.rows):
            i = row

            while self.matrix[i][col] == 0:     # skips all the 0's until it reaches a non-zero number
                i += 1
                if i == self.rows:  # goes to the next column when it reaches the end of the current one
                    i = row
                    col += 1
                    if col == self.cols:    # not a single non-zero number is found
                        return self

            self.change_rows(i, row)
            denominator = self.matrix[row][col]

            for c in range(self.cols):
                self.matrix[row][c] = self.matrix[row][c] / denominator

            for j in range(self.rows):
                if j != row:
                    m = self.matrix[j][col]
                    for k in range(self.cols):
                        self.matrix[j][k] -= self.matrix[row][k] * m

            col += 1
            if col == self.cols:
                return self

        return self

    def invert(self):
        if self.rows != self.cols:
            return False

        identity = Matrix.identity(self.rows)
        col = 0
        for row in range(self.rows):
            i = row
            while self.matrix[i][col] == 0:  # skips all the 0's until it reaches a non-zero number
                i += 1
                if i == self.rows:  # goes to the next column when it reaches the end of the current one
                    i = row
                    col += 1
                    if col == self.cols:  # not a single non-zero number is found
                        return False

            self.change_rows(i, row)
            identity.change_rows(i, row)
            denominator = self.matrix[row][col]

            for c in range(self.cols):
                self.matrix[row][c] = self.matrix[row][c] / denominator
                identity.matrix[row][c] = identity.matrix[row][c] / denominator

            for j in range(self.rows):
                if j != row:
                    m = self.matrix[j][col]
                    for k in range(self.cols):
                        self.matrix[j][k] -= self.matrix[row][k] * m
                        identity.matrix[j][k] -= identity.matrix[row][k] * m
            col += 1

        return identity

    @staticmethod
    def identity(n):
        func = lambda x, y: 1 if x == y else 0
        identity = Matrix([[func(i, j) for i in range(n)] for j in range(n)])
        return identity


operand = input().split()

if operand[0] == "identity":
    n = int(input())
    print(Matrix.identity(n))

if operand[0] == "rref":
    n, m = map(int, input().split())
    m1 = Matrix([list(map(lambda num: Fraction(num), input().split(" "))) for i in range(n)])
    print(m1.rref())

if operand[0] == "invert":
    n, m = map(int, input().split())
    m1 = Matrix([list(map(lambda num: Fraction(num), input().split(" "))) for i in range(n)])
    print(m1.invert())


if operand[0] == "add" or operand[0] == "subtract" or operand[0] == "multiply":
    n, m = map(int, input().split())
    m1 = Matrix([list(map(lambda num: Fraction(num), input().split(" "))) for i in range(n)])
    x, y = map(int, input().split())
    m2 = Matrix([list(map(lambda num: Fraction(num), input().split(" "))) for i in range(x)])

    if operand[0] == "add":
        print(m1 + m2)

    if operand[0] == "subtract":

        print(m1 - m2)
    if operand[0] == "multiply":
        print(m1 * m2)

if len(operand) > 1:
    n, m = map(int, input().split())
    mat = Matrix([list(map(lambda num: Fraction(num), input().split(" "))) for i in range(n)])

    if operand[1] == "row":
        mat.get_row(int(operand[-1]))

    if operand[1] == "column":
        mat.get_col(int(operand[-1]))

    if operand[1] == "block":
        mat.get_block((operand[2][1:-1], operand[3][:-1]), (operand[-2][1:-1], operand[-1][:-1]))
