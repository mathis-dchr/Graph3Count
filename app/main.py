import yaml

from graph import Graph

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

if __name__ == "__main__":
    print("Visit http://localhost:8080/")

    g = Graph("./data/data.json") # Graph creation
    print("\nGraph created")

    process_transactions(g, "./data/intent.yaml") # graph construction
    print("Graph constructed")
    g.save() # saving the graph to the data.json file
    print("Graph saved to data.json")

    transactions_before_simplification = len(g.matrix[0])*len(g.matrix) - sum(row.count(0.0) for row in g.matrix) # number of non-zero edges
    simplified_transactions = []

    simplified_transactions = g.transaction_optimization() # transaction optimization
    print("Optimized transactions")
    g.save() # saving the graph to the data.json file
    print("Graph saved to data.json")

    print("\nBalances:")
    if simplified_transactions:
        for txn in simplified_transactions:
            print(f"- {txn['from']} owes {txn['to']} CN¥{txn['amount']:.2f}")
        print(f"\nNumber of initial transactions: {transactions_before_simplification}")
        print(f"Number of transactions after optimization: {len(simplified_transactions)}")
    else:
        print("The accounts are already balanced or there are no transactions")

    #print(g) # for debugging
