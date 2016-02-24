def check_outer_perimeter(field, i_offset, j_offset,
                          ship_direction, checked_cells):
    # left and right perimeter sides
    for i in range(i_offset - 1, i_offset + ship_direction[0] + 1):
        if 0 <= i < 10:
            j = j_offset - 1
            if j >= 0 and not checked_cells[i*10 + j] and field[i][j]:
                return False
            j = j_offset + ship_direction[1]
            if j < 10 and not checked_cells[i*10 + j] and field[i][j]:
                return False

    # down perimeter side
    for j in range(j_offset, j_offset + ship_direction[1]):
        if i < 10:
            i = i_offset + ship_direction[0]
            if field[i][j]:
                return False

    return True


def get_direction(field, i_offset, j_offset):
    i = j = 0  # i - how long to down, j - to right
    while i_offset + i < 10 and field[i_offset+i][j_offset]:
        i += 1
    while j_offset + j < 10 and field[i_offset][j_offset+j]:
        j += 1
    return i, j


def validate_battlefield(field):
    ships_rest = {1: 4,
                  2: 3,
                  3: 2,
                  4: 1}
    checked_cells = [False for _ in range(10*10)]

    if sum(sum(cell for cell in row) for row in field) != 20:
        return False

    for i in range(len(field)):
        for j in range(len(field)):
            if not checked_cells[i*10 + j] and field[i][j]:
                ship_dir = get_direction(field, i, j)
                ship_len = max(ship_dir)

                if ship_len not in ships_rest or ships_rest[ship_len] == 0:
                    return False  # len is 5+ or wrong ships set
                if sum(ship_dir) != ship_len + 1:
                    return False  # linear ships
                if not check_outer_perimeter(field, i, j, ship_dir, checked_cells):
                    return False  # some ships are too close to each other

                for x in range(j, j + ship_dir[1]):
                    checked_cells[i*10 + x] = True
                for y in range(i, i + ship_dir[0]):
                    checked_cells[y*10 + j] = True

                ships_rest[ship_len] -= 1
            else:
                checked_cells[i*10 + j] = True

    return True

battle_field = [[1, 0, 0, 0, 0, 1, 1, 0, 0, 0],
                [1, 0, 1, 0, 0, 0, 0, 0, 1, 1],
                [1, 0, 1, 0, 1, 1, 1, 0, 0, 0],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
                [0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
                [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 1, 0, 0, 0, 0, 0, 0]]

print (validate_battlefield(battle_field))
