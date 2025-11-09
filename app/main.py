import numpy as n
import yaml

from graph import Graph

print("visit http://localhost:8080/")



def process_transactions(graph, yaml_path="intent.yaml"):
    with open(yaml_path, "r") as f:
        intent = yaml.safe_load(f)

    # Add all members
    for member in intent.get("members", []):
        graph.add_node(member)

    # Handle transactions
    for txn in intent.get("transaction", []):
        sender = txn["from"]
        receivers = txn["to"]
        amount = txn["amount"]

        # Normalize receivers list
        if not isinstance(receivers, list):
            receivers = [receivers]

        # Split amount equally among receivers
        if receivers:
            share = amount / len(receivers)
            for receiver in receivers:
                graph.add_edge(sender, receiver, share)

    graph.save()


if __name__ == "__main__":
    g = Graph("./data/data.json")
    process_transactions(g, "./data/intent.yaml")
    print("Graph built and saved to data.json")
    #print(g)