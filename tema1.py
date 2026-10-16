import math
import pathlib

#analizare sistem ecuatii
def load_system(path: pathlib.Path) -> tuple[list[list[float]], list[float]]:
    A: list[list[float]] = []
    B: list[float] = []
    variables = ["x", "y", "z"]

    for line in path.read_text().splitlines():
        line = line.strip()
        if not line:
            continue

        left, right = line.split("=")
        B.append(float(right.strip()))

        row = [0.0, 0.0, 0.0]
        sign = 1.0
        for token in left.split():
            if token == "+":
                sign = 1.0
                continue
            if token == "-":
                sign = -1.0
                continue

            #token de forma 2x,x,-y,3.5z
            var = token[-1]
            coef_str = token[:-1]
            if coef_str in ("", "+"):
                coef = 1.0
            elif coef_str == "-":
                coef = -1.0
            else:
                coef = float(coef_str)

            row[variables.index(var)] += sign * coef
            sign = 1.0
        A.append(row)

    return A, B


#operatiuni cu matrice si vector
def determinant(matrix: list[list[float]]) -> float:
    a = matrix
    return (a[0][0] * (a[1][1] * a[2][2] - a[1][2] * a[2][1])
            - a[0][1] * (a[1][0] * a[2][2] - a[1][2] * a[2][0])
            + a[0][2] * (a[1][0] * a[2][1] - a[1][1] * a[2][0]))


def trace(matrix: list[list[float]]) -> float:
    return sum(matrix[i][i] for i in range(len(matrix)))


def norm(vector: list[float]) -> float:
    return math.sqrt(sum(v ** 2 for v in vector))


def transpose(matrix: list[list[float]]) -> list[list[float]]:
    return [[matrix[i][j] for i in range(len(matrix))] for j in range(len(matrix[0]))]


def multiply(matrix: list[list[float]], vector: list[float]) -> list[float]:
    return [sum(row[j] * vector[j] for j in range(len(vector))) for row in matrix]


#cramer
def replace_column(matrix: list[list[float]], col: int, vector: list[float]) -> list[list[float]]:
    return [[vector[i] if j == col else matrix[i][j] for j in range(len(matrix[i]))]
            for i in range(len(matrix))]


def solve_cramer(matrix: list[list[float]], vector: list[float]) -> list[float]:
    det_a = determinant(matrix)
    if det_a == 0:
        raise ValueError("det(A) = 0 -> sistemul nu are solutie unica")
    return [determinant(replace_column(matrix, j, vector)) / det_a
            for j in range(len(matrix))]


#inversion
def minor(matrix: list[list[float]], i: int, j: int) -> list[list[float]]:
    return [[matrix[r][c] for c in range(len(matrix[r])) if c != j]
            for r in range(len(matrix)) if r != i]


def det2(matrix: list[list[float]]) -> float:
    return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]


def cofactor(matrix: list[list[float]]) -> list[list[float]]:
    n = len(matrix)
    return [[(-1) ** (i + j) * det2(minor(matrix, i, j)) for j in range(n)]
            for i in range(n)]


def adjoint(matrix: list[list[float]]) -> list[list[float]]:
    return transpose(cofactor(matrix))


def inverse(matrix: list[list[float]]) -> list[list[float]]:
    det_a = determinant(matrix)
    if det_a == 0:
        raise ValueError("det(A) = 0 -> matricea nu este inversabila")
    return [[v / det_a for v in row] for row in adjoint(matrix)]


def solve(matrix: list[list[float]], vector: list[float]) -> list[float]:
    return multiply(inverse(matrix), vector)


if __name__ == "__main__":
    A, B = load_system(pathlib.Path("system.txt"))
    print(f"{A=} {B=}")
    print(f"{determinant(A)=}")
    print(f"{trace(A)=}")
    print(f"{norm(B)=}")
    print(f"{transpose(A)=}")
    print(f"{multiply(A, B)=}")
    print(f"{solve_cramer(A, B)=}")
    print(f"{cofactor(A)=}")
    print(f"{adjoint(A)=}")
    print(f"{solve(A, B)=}")

    #verificare A*X trebuie sa dea B
    X = solve(A, B)
    print(f"verificare A*X = {multiply(A, X)}")