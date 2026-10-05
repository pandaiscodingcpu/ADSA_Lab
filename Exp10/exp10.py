from collections import deque

def ford_fulkerson(capacity, s, t):
    n = len(capacity)
    residual = [row[:] for row in capacity]
    max_flow = 0

    while True:
        parent = [-1] * n
        parent[s] = s
        q = deque([s])

        while q and parent[t] == -1:
            u = q.popleft()
            for v in range(n):
                if parent[v] == -1 and residual[u][v] > 0:
                    parent[v] = u
                    q.append(v)

        if parent[t] == -1:
            break

        flow = float('inf')
        v = t
        while v != s:
            u = parent[v]
            flow = min(flow, residual[u][v])
            v = u

        v = t
        while v != s:
            u = parent[v]
            residual[u][v] -= flow
            residual[v][u] += flow
            v = u

        max_flow += flow

    return max_flow


# Example
capacity = [
    [0, 16, 13, 0, 0, 0],
    [0, 0, 10, 12, 0, 0],
    [0, 4, 0, 0, 14, 0],
    [0, 0, 9, 0, 0, 20],
    [0, 0, 0, 7, 0, 4],
    [0, 0, 0, 0, 0, 0]
]

print("Maximum Flow:", ford_fulkerson(capacity, 0, 5))
