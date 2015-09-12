def answer(x):
    x.sort(key=lambda t: t[0])
    no_overlap = [x[0]]

    for higher_time in x[1:]:
        lower_time = no_overlap[-1]
        if higher_time[0] <= lower_time[1]:
            no_overlap[-1] = (lower_time[0], max(lower_time[1], higher_time[1]))
        else:
            no_overlap.append(higher_time)
    return sum([time2 - time1 for time1, time2 in no_overlap])

print answer([[1, 3], [3, 6]])
print answer([[10, 14], [4, 18], [19, 20], [19, 20], [13, 20], [13, 20]])
