def answer(words):
    full_alpha = list(set("".join(words)))
    graph = Graph(full_alpha)

    for i in range(0, len(words) - 1):
        w1 = words[i]
        w2 = words[i + 1]
        for c in w1:
            graph.create_vertex(c)
        for c in w2:
            graph.create_vertex(c)
        for j in range(0, min(len(w1), len(w2))):
            if w1[j] != w2[j]:
                graph.add_edge(w1[j], w2[j])
                break

    return graph.top_sort()

class Graph:
    def __init__(self, full_alpha):
        self.edges = {k:[] for k in full_alpha}
        self.alpha = []

    def create_vertex(self, ver):
        if ver not in self.alpha:
            self.alpha.append(ver)

    def add_edge(self, start, end):
        print start, end
        self.edges[start].append(end)

    def top_sort_recurse(self, vertex, visited, stack):
        global letters
        visited[vertex] = True

        for vert in self.edges[vertex]:
            if not visited[vert]:
                self.top_sort_recurse(vert, visited, stack)

        stack.insert(0, vertex)

    def top_sort(self):
        stack = []
        visited = {k:False for k in self.edges.keys()}

        for c in self.alpha:
            if not visited[c]:
                self.top_sort_recurse(c, visited, stack)

        return "".join(stack)

print answer(["y", "z", "xy"])
print answer(["ba", "ab", "cb"])
print answer(["caa", "aaa", "aab"])
print answer(["z", "yx", "yz"])
print answer(["C", "CAC", "CB", "BCC", "BA"])
