import json

class Graph:
    def __init__(self, json_path="data.json"):
        self.json_path = json_path
        self.nodes = []
        self.matrix = []

    def save(self):
        data = {"nodes": self.nodes, "matrix": self.matrix}
        with open(self.json_path, "w") as f:
            json.dump(data, f, indent=2)

    def add_node(self, name):
        # Avoid duplicates
        if any(node["name"] == name for node in self.nodes):
            return
        new_id = len(self.nodes)
        self.nodes.append({"id": new_id, "name": name})
        # Expand adjacency matrix
        for row in self.matrix:
            row.append(0.0)
        self.matrix.append([0.0] * len(self.nodes))

    def get_node_id(self, name):
        for node in self.nodes:
            if node["name"] == name:
                return node["id"]
        raise ValueError(f"Node '{name}' not found")

    def add_edge(self, from_name, to_name, amount):
        '''Add a directed edge from 'from_name' to 'to_name' with amount.'''
        from_id = self.get_node_id(from_name)
        to_id = self.get_node_id(to_name)

        # If amount < 0, reverse the edge
        if amount < 0:
            amount = abs(amount)
            from_id, to_id = to_id, from_id
            
        self.matrix[to_id][from_id] += amount # the sender and receiver are reversed because the edge represents what the receiver owes, not what the sender gave

    def __repr__(self):
        return f"Graph(nodes={self.nodes}, matrix={self.matrix})"