def answer_slow(chunk, word):
    from re import finditer

    def recurse_replace_slow(mod_chunk):
        found_words = [i for i in range(len(mod_chunk))
                            if mod_chunk[i:i+len(word)] == word]

        if len(found_words) == 0:
            yield mod_chunk

        for idx in found_words:
            test_word = str(mod_chunk)
            test_word = test_word[:idx] + test_word[len(word) + idx:]
            for result in recurse_replace(test_word):
                yield result

    return sorted([x for x in recurse_replace(chunk)])[0]

def answer(chunk, word):
    #YOLOAMIRITE?!?!
    max_depth = 5

    def recurse_replace(mod_chunk, smallest, depth=1):
        if depth == max_depth:
            return

        for i in range(len(mod_chunk)):
            if mod_chunk[i:i+len(word)] != word:
                continue

            test_word = mod_chunk[:i] + mod_chunk[len(word) + i:]

            if word in test_word:
                result = recurse_replace(test_word, smallest, depth+1)
                if result != None:
                    smallest = result
            else:
                if len(test_word) == len(smallest):
                    if cmp(test_word, smallest) == -1:
                        return test_word
                    else:
                        return smallest
                elif len(test_word) < len(smallest):
                    return test_word
                return smallest

        return smallest

    smallest = chunk.replace(word, "")
    return recurse_replace(chunk, smallest)

print answer("lololololo", "lol")
print answer("gogogogogogogogogogo", "g")

