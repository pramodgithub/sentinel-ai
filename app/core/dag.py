from collections import defaultdict, deque


def compute_levels(nodes, edges):

    graph = defaultdict(list)
    indegree = {n: 0 for n in nodes}

    for src, dst in edges:
        graph[src].append(dst)
        indegree[dst] += 1

    queue = deque()

    for node in nodes:
        if indegree[node] == 0:
            queue.append(node)

    levels = []

    while queue:

        level = []
        for _ in range(len(queue)):

            node = queue.popleft()
            level.append(node)

            for neighbor in graph[node]:

                indegree[neighbor] -= 1

                if indegree[neighbor] == 0:
                    queue.append(neighbor)

        levels.append(level)

    return levels