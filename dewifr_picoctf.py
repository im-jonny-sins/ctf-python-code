SQUARE_SIZE = 6
alphabet = "0fkdwu6rp8zvsnlj3iytxmeh72ca9bg5o41q"
ciphertext = "herfayo7oqxrz7jwxx15ie20p40u1i"

def generate_square(alphabet):
    assert len(alphabet) == SQUARE_SIZE ** 2
    matrix = []
    for i in range(SQUARE_SIZE):
        row = list(alphabet[i * SQUARE_SIZE:(i + 1) * SQUARE_SIZE])
        matrix.append(row)
    return matrix

def get_index(letter, matrix):
    for r in range(SQUARE_SIZE):
        for c in range(SQUARE_SIZE):
            if matrix[r][c] == letter:
                return (r, c)
    raise ValueError(f"{letter} not found")

def decrypt_pair(pair, matrix):
    p1 = get_index(pair[0], matrix)
    p2 = get_index(pair[1], matrix)

    if p1[0] == p2[0]:
        # same row → shift left
        return matrix[p1[0]][(p1[1] - 1) % SQUARE_SIZE] + matrix[p2[0]][(p2[1] - 1) % SQUARE_SIZE]
    elif p1[1] == p2[1]:
        # same column → shift up
        return matrix[(p1[0] - 1) % SQUARE_SIZE][p1[1]] + matrix[(p2[0] - 1) % SQUARE_SIZE][p2[1]]
    else:
        # rectangle → swap columns
        return matrix[p1[0]][p2[1]] + matrix[p2[0]][p1[1]]

def decrypt_string(s, matrix):
    result = ""
    for i in range(0, len(s), 2):
        result += decrypt_pair(s[i:i+2], matrix)
    return result

m = generate_square(alphabet)
plaintext = decrypt_string(ciphertext, m)
print("there is " ,plaintext)
