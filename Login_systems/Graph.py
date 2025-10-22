import matplotlib.pyplot as plt
import networkx as nx
from collections import deque


class Graph_structure:
    def __init__(self):
        # เก็บเป็น list ก็ใช้ได้ แต่เดี๋ยวกัน edge ซ้ำตอนวาดแทน
        self.graph = {}

    def add_edge(self, node, neighbor):
        """เพิ่มเส้นเชื่อมระหว่าง node และ neighbor (undirected)"""
        if node not in self.graph:
            self.graph[node] = []
        if neighbor not in self.graph:
            self.graph[neighbor] = []
        # ป้องกัน duplicate ใน adjacency list
        if neighbor not in self.graph[node]:
            self.graph[node].append(neighbor)
        if node not in self.graph[neighbor]:
            self.graph[neighbor].append(node)

    def show_graph(self):
        """แสดงโครงสร้าง Graph"""
        for node, neighbors in self.graph.items():
            print(f"{node} -> {neighbors}")

    def plot_graph(self, highlight_nodes=None, title='Graph Visualization'):
        """วาดกราฟด้วย matplotlib และ networkx"""
        G = nx.Graph()

        # ใส่ edge แบบไม่ซ้ำ: เพิ่มเฉพาะ (u, v) ที่ u < v
        added = set()
        for node, neighbors in self.graph.items():
            for neighbor in neighbors:
                u, v = sorted((node, neighbor))
                if (u, v) not in added:
                    G.add_edge(u, v)
                    added.add((u, v))

        # กรณีกราฟว่าง กันหลุด
        if G.number_of_nodes() == 0:
            print("กราฟว่าง ไม่มีอะไรให้วาดนะ")
            return

        pos = nx.spring_layout(G, seed=42)
        plt.figure(figsize=(10, 8))

        # สี node
        highlight_nodes = set(highlight_nodes) if highlight_nodes else set()
        node_colors = ['lightcoral' if n in highlight_nodes else 'skyblue' for n in G.nodes()]

        nx.draw(
            G, pos,
            with_labels=True,
            node_color=node_colors,
            node_size=1200,
            font_size=12,
            font_weight='bold',
            edge_color='gray'
        )
        plt.title(title)
        plt.tight_layout()
        plt.show()

    def bfs(self, start):
        if start not in self.graph:
            print(f"Node {start} ไม่อยู่ในกราฟ")
            return []

        visited = set([start])
        queue = deque([start])
        result = []

        while queue:
            node = queue.popleft()
            result.append(node)
            print(f"เยี่ยมชม node: {node}")
            # ใช้ลำดับคงที่เพื่อ reproducible
            for neighbor in sorted(self.graph[node]):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        return result

    def dfs(self, start):
        if start not in self.graph:
            print(f"Node {start} ไม่อยู่ในกราฟ")
            return []

        visited = set()
        stack = [start]
        result = []

        while stack:
            node = stack.pop()
            if node not in visited:
                visited.add(node)
                result.append(node)
                print(f"เยี่ยมชม node: {node}")
                # ใส่ reverse เพื่อลง stack แล้ว pop ออกมาจะได้เรียงจากน้อยไปมาก
                for neighbor in sorted(self.graph[node], reverse=True):
                    if neighbor not in visited:
                        stack.append(neighbor)
        return result


if __name__ == "__main__":
    # สร้าง graph
    g = Graph_structure()
    g.add_edge('A', 'B')
    g.add_edge('A', 'C')
    g.add_edge('B', 'D')
    g.add_edge('C', 'D')
    g.add_edge('D', 'E')

    print("=" * 50)
    print("โครงสร้าง Graph:")
    print("=" * 50)
    g.show_graph()

    print("\n" + "=" * 50)
    print("BFS เริ่มจาก node 'A':")
    print("=" * 50)
    bfs_result = g.bfs('A')
    print(f"ลำดับการเยี่ยมชม: {' -> '.join(bfs_result)}")

    print("\n" + "=" * 50)
    print("DFS (Iterative) เริ่มจาก node 'A':")
    print("=" * 50)
    dfs_result = g.dfs('A')
    print(f"ลำดับการเยี่ยมชม: {' -> '.join(dfs_result)}")

    # วาดกราฟ ไฮไลต์ลำดับที่ BFS เยี่ยมชม
    g.plot_graph(highlight_nodes=bfs_result, title='Graph Structure')
