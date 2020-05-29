from fractions import Fraction, gcd


def multiply_matrices(a, b):
    # confirm dimensions
    a_rows = len(a)
    a_cols = len(a[0])
    b_cols = len(b[0])
    rows = a_rows
    cols = b_cols
    # create the result matrix c = a*b
    c = make_2d_list(rows, cols)
    # now find each value in turn in the result matrix
    for row in range(rows):
        for col in range(cols):
            dot_product = Fraction(0, 1)
            for i in range(a_cols):
                dot_product += a[row][i] * b[i][col]
            c[row][col] = dot_product
    return c


def multiply_row_of_square_matrix(m, row, k):
    n = len(m)
    row_operator = make_identity(n)
    row_operator[row][row] = k
    return multiply_matrices(row_operator, m)


def make_2d_list(rows, cols):
    a = []
    for row in range(rows):
        a += [[0] * cols]

    print("make_2d_list a :: ",a)
    return a


def make_identity(n):
    result = make_2d_list(n, n)
    for i in range(n):
        result[i][i] = Fraction(1, 1)

    print("make_identity result :: ", result)
    return result


def add_multiple_of_row_of_square_matrix(m, source_row, k, target_row):
    # add k * source_row to target_row of matrix m
    n = len(m)
    row_operator = make_identity(n)
    row_operator[target_row][source_row] = k
    return multiply_matrices(row_operator, m)


def invert_matrix(m):
    n = len(m)
    assert (len(m) == len(m[0]))
    inverse = make_identity(n)
    for col in range(n):
        diagonal_row = col
        assert (m[diagonal_row][col] != 0)
        k = Fraction(1, m[diagonal_row][col])
        m = multiply_row_of_square_matrix(m, diagonal_row, k)
        inverse = multiply_row_of_square_matrix(inverse, diagonal_row, k)
        source_row = diagonal_row
        for target_row in range(n):
            if source_row != target_row:
                k = -m[target_row][col]
                m = add_multiple_of_row_of_square_matrix(m, source_row, k, target_row)
                inverse = add_multiple_of_row_of_square_matrix(inverse, source_row, k, target_row)
    # that's it!
    return inverse


def subtract_identity(q, denominator):
    size = range(len(q))
    for i in size:
        for j in size:
            if i == j:
                q[i][j] = denominator - q[i][j]
            else:
                q[i][j] = - q[i][j]


def transform_matrix(m):
    for row_index, row in enumerate(m):
        row_sum = sum(m[row_index])
        if row_sum == 0:
            m[row_index][row_index] = 1
        else:
            for col_index, col in enumerate(row):
                m[row_index][col_index] = Fraction(col, row_sum)


def get_submatrix(m, rows, cols):
    new_matrix = []

    for row in rows:
        current_row = []
        for col in cols:
            current_row.append(m[row][col])
        new_matrix.append(current_row)
    print("new_matrix for row :: ",row," col :: ",col)
    print(new_matrix)
    return new_matrix


def get_q(m, non_terminal_states):
    return get_submatrix(m, non_terminal_states, non_terminal_states)


def get_r(m, non_terminal_states, terminal_states):
    return get_submatrix(m, non_terminal_states, terminal_states)


def subtract_matrices(a, b):
    new_matrix = []
    for row_index, row in enumerate(a):
        column = []
        for col_index, col in enumerate(row):
            column.append(a[row_index][col_index] - b[row_index][col_index])
        new_matrix.append(column)

    return new_matrix


def lcm(a, b):
    result = a * b / gcd(a, b)

    return result


def lcm_for_arrays(args):
    array_length = len(args)
    if array_length <= 2:
        return lcm(*args)

    initial = lcm(args[0], args[1])
    i = 2
    while i < array_length:
        initial = lcm(initial, args[i])
        i += 1
    return initial


def answer(m):
    terminal_states = []
    non_terminal_states = []
    for index, row in enumerate(m):
        if sum(row) == 0:
            terminal_states.append(index)
        else:
            non_terminal_states.append(index)

    if len(terminal_states) == 1:
        return [1, 1]
    print("before transform")
    print(m)
    transform_matrix(m)
    print("after transform")
    print(m)
    print("terminal_states :: ")
    print(terminal_states)
    print("non_terminal_states :: ")
    print(non_terminal_states)
    q = get_q(m, non_terminal_states)
    print("q :: ",q)
    r = get_r(m, non_terminal_states, terminal_states)
    print("r :: ", r)

    print("* @ "*20)
    result = multiply_matrices(invert_matrix(subtract_matrices(make_identity(len(q)), q)), r)

    denominator = lcm_for_arrays([item.denominator for item in result[0]])

    result = [item.numerator * denominator / item.denominator for item in result[0]]

    result.append(denominator)

    return result


if __name__ == '__main__':
    test_input = [
        [0, 2, 1, 0, 0],
        [0, 0, 0, 3, 4],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]
    ]
    print(answer(test_input))
