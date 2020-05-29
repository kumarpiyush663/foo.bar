def calculate_steps(n):
    # pad size
    size = n + 1

    # create zero-filled matrix
    matrix = [[0 for _ in range(size)] for _ in range(size)]

    # base value is always padded and skipped
    matrix[0][0] = 1
    for prev in range(1, size):
        for left in range(0, size):
            matrix[prev][left] = matrix[prev - 1][left]
            if left >= prev:
                matrix[prev][left] += matrix[prev - 1][left - prev]

    for i in range(0, size):
        for j in range(0, size):
            print("matrix[{}][{}]".format(i,j), end=" ")
        print()

    for i in range(0, size):
        for j in range(0, size):
            print(matrix[i][j], end=" ")
        print()
    return matrix[n][n] - 1


def answer(n):
    return calculate_steps(n)


print(answer(4))
print(answer(5))
print(answer(6))
# print(answer(200))
