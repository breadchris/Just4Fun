def answer(document, searchTerms):
    from collections import Counter

    def issubset(c1, c2):
        return not c1 - (c1 & c2)

    document = document.split(" ")
    target_hist = Counter(searchTerms)
    current_hist = Counter()

    for idx, elem in enumerate(document):
        if elem in target_hist:
            document = document[idx:]
            break

    doc_iter = iter(document)
    current = []
    while not issubset(target_hist, current_hist):
        word = next(doc_iter)
        current.append(word)
        current_hist[word] += 1

    minlen = len(current)
    shortest = list(current)
    for word in doc_iter:
        if word == current[0]:
            current_hist = Counter(current)

            for idx, elem in enumerate(current[1:], 1):
                if not current_hist[elem] - target_hist[elem]:
                    break
                current_hist[elem] -= 1
            current = current[idx:]

        if len(current) < minlen:
            minlen = len(current)
            shortest = list(current)
        else:
            current.append(word)
            current_hist[word] += 1

    return " ".join(shortest)

def answer(document, searchTerms):
    from collections import defaultdict
    document = document.split(' ')
    min_seq = document
    found_words = defaultdict(lambda : [-1,-1])
    linked = []
    for i, word in enumerate(document):
        if word in searchTerms:
            found_words[word][0] = i
            if found_words[word][1] != -1:
                del(linked[found_words[word][1]])

            linked.append(word)

            for i, _word in enumerate(linked):
                found_words[_word][1] = i

            if len(linked) == len(searchTerms):
                startPos = found_words[linked[0]][0]
                endPos = found_words[linked[-1]][0]
                if (endPos - startPos + 1) < len(min_seq):
                    min_seq = document[startPos:endPos + 1]

    return ' '.join(min_seq)

print answer("a b c d a", ["a", "c", "d"])
print answer("many google employees can program", ["google", "program"])
print answer("a b b d a d c a", ["a", "c", "d"])
