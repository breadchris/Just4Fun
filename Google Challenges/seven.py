def answer(x, y, n):
    pass

def num_visible(line_up):
    # line_up must contain unique numbers
    visible_left = 1
    visible_right = 1

    # count left
    highest = line_up[0]
    highest_idx = 0
    for i in range(1, len(line_up)):
        if line_up[i] > highest:
            highest = line_up[i]
            highest_idx = i
            visible_left += 1

    highest = line_up[-1]
    highest_idx = len(line_up) - 1
    for i in range(len(line_up) - 2, 0, -1):
        if line_up[i] > highest:
            highest = line_up[i]
            highest_idx = i
            visible_right += 1

    return visible_left, visible_right

print num_visible([5, 1, 2, 3, 4])
print num_visible([1, 5, 2, 3, 4])
print num_visible([6, 3, 2, 7, 4, 5, 1])
