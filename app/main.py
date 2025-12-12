import yaml

from graph import Graph

def process_transactions(graph, yaml_path="intent.yaml"):
    with open(yaml_path, "r") as f:
        intent = yaml.safe_load(f)

    # Add all members
    for member in intent.get("members", []):
        graph.add_node(member)

    # Handle transactions
    for txn in intent.get("transactions", []):
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
    
    print("\nGraph constructed")
    g.save() # saving the graph to the data.json file
    print("Graph saved to data.json")

def graph_optimization(graph):
    transactions_before_simplification = sum( # Number of edges without loops (loop = transfer to itself)
        1 for i in range(len(graph.matrix)) 
        for j in range(len(graph.matrix[i])) 
        if i != j and graph.matrix[i][j] != 0.0
    )

    balances, simplified_transactions = graph.transactions_optimization() # transactions optimization
    print("\nOptimized transactions")
    graph.save() # saving the graph to the data.json file
    print("Graph saved to data.json")

    if balances and simplified_transactions:
        print("\nBalances:")
        for name, balance in balances.items():
            if balance>=0: print(f"{name} +CN¥{balance}")
            else: print(f"{name} -CN¥{-balance}")

        print("\nSuggested refund:")
        for transactions in simplified_transactions:
            print(f"- {transactions['from']} owes {transactions['to']} CN¥{transactions['amount']:.2f}")
        print(f"\nNumber of initial transactions: {transactions_before_simplification}")
        print(f"Number of transactions after optimization: {len(simplified_transactions)}")
    else:
        print("\nThe accounts are already balanced or there are no transactions")

if __name__ == "__main__":
    print("\nVisit http://localhost:8080/")

    g = Graph("./data/data.json") # Graph creation
    print("\nGraph created")

    process_transactions(g, "./data/intent.example.yaml") # graph construction

    graph_optimization(g)

    #print(g) # for debugging
