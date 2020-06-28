from typing import Optional

lines = (
    ((0, 0), (1, 0), (2, 0), (3, 0)),  # Horizontal
    ((0, 0), (0, 1), (0, 2), (0, 3)),  # Vertical
    ((0, 0), (1, 1), (2, 2), (3, 3)),  # Diag 1
    ((0, 0), (1, -1), (2, -2), (3, -3)),  # Diag 2
)


def winner(columns) -> Optional[str]:
    for c in range(len(columns)):
        for r in range(len(columns[c])):
            for line in lines:
                count = 1
                player = columns[c][r]
                for c_offset, r_offset in line[1:]:
                    c_i = c + c_offset
                    r_i = r + r_offset
                    if 0 <= c_i < len(columns) and 0 <= r_i < len(columns[c_i]) and player == columns[c_i][r_i]:
                        count += 1
                    else:
                        break
                if count == 4:
                    return player
    return None


def who_is_winner(pieces_position_list):
    columns = [[] for _ in range(7)]

    for move in pieces_position_list:
        col_letter, player = move.split('_')
        col_index = ord(col_letter) - ord('A')
        columns[col_index].append(player)
        res = winner(columns)
        if res:
            return res

    return "Draw"


if __name__ == '__main__':
    assert who_is_winner([
        "C_Yellow", "E_Red", "G_Yellow", "B_Red", "D_Yellow", "B_Red", "B_Yellow", "G_Red", "C_Yellow", "C_Red",
        "D_Yellow", "F_Red", "E_Yellow", "A_Red", "A_Yellow", "G_Red", "A_Yellow", "F_Red", "F_Yellow", "D_Red",
        "B_Yellow", "E_Red", "D_Yellow", "A_Red", "G_Yellow", "D_Red", "D_Yellow", "C_Red"
    ]) == "Yellow"

    assert who_is_winner([
        "C_Yellow", "B_Red", "B_Yellow", "E_Red", "D_Yellow", "G_Red", "B_Yellow", "G_Red", "E_Yellow", "A_Red",
        "G_Yellow", "C_Red", "A_Yellow", "A_Red", "D_Yellow", "B_Red", "G_Yellow", "A_Red", "F_Yellow", "B_Red",
        "D_Yellow", "A_Red", "F_Yellow", "F_Red", "B_Yellow", "F_Red", "F_Yellow", "G_Red", "A_Yellow", "F_Red",
        "C_Yellow", "C_Red", "G_Yellow", "C_Red", "D_Yellow", "D_Red", "E_Yellow", "D_Red", "E_Yellow", "C_Red",
        "E_Yellow", "E_Red"
    ]) == "Yellow"

    assert who_is_winner([
        "F_Yellow", "G_Red", "D_Yellow", "C_Red", "A_Yellow", "A_Red", "E_Yellow", "D_Red", "D_Yellow", "F_Red",
        "B_Yellow", "E_Red", "C_Yellow", "D_Red", "F_Yellow", "D_Red", "D_Yellow", "F_Red", "G_Yellow", "C_Red",
        "F_Yellow", "E_Red", "A_Yellow", "A_Red", "C_Yellow", "B_Red", "E_Yellow", "C_Red", "E_Yellow", "G_Red",
        "A_Yellow", "A_Red", "G_Yellow", "C_Red", "B_Yellow", "E_Red", "F_Yellow", "G_Red", "G_Yellow", "B_Red",
        "B_Yellow", "B_Red"
    ]) == "Red"

    assert who_is_winner([
        "A_Yellow", "B_Red", "B_Yellow", "C_Red", "G_Yellow", "C_Red", "C_Yellow", "D_Red", "G_Yellow", "D_Red",
        "G_Yellow", "D_Red", "F_Yellow", "E_Red", "D_Yellow"
    ]) == "Red"

    assert who_is_winner([
        "A_Red", "B_Yellow", "A_Red", "B_Yellow", "A_Red", "B_Yellow", "G_Red", "B_Yellow"
    ]) == "Yellow"

    assert who_is_winner([
        "A_Red", "B_Yellow", "A_Red", "E_Yellow", "F_Red", "G_Yellow", "A_Red", "G_Yellow"
    ]) == "Draw"
