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

    def calculate_net_balances(self):
        '''Calculate the net balance of each member (receivables - payables).'''
        num_nodes = len(self.nodes)
        balances = {}
        for i in range(num_nodes):
            name = self.nodes[i]["name"]

            total_debts = sum(self.matrix[i]) # debts (outgoing)
            total_credits = sum(self.matrix[j][i] for j in range(num_nodes)) # receivables (incoming)

            net_balance = total_credits - total_debts # net balance = receivables - payables
            balances[name] = round(net_balance, 2) # rounding to avoid floating-point errors

        return balances
    
    def transaction_optimization(self):
        '''Optimize transactions to minimize the number of payments by using the net balance.'''
        balances = self.calculate_net_balances()
        simplified_transactions = []
        
        # Sort to put the largest debtors and creditors first (optional)
        debtors_list = sorted([(name, -balance) for name, balance in balances.items() if balance < -0.01], key=lambda item: item[1], reverse=True) # debtors (must pay, balance < 0): amount to pay is positive
        creditors_list = sorted([(name, balance) for name, balance in balances.items() if balance > 0.01], key=lambda item: item[1], reverse=True) # creditors (due to receive, balance > 0): amount to be received is positive

        # Minimum settlement algorithm: Make debtors pay creditors until the balances are equalized
        while debtors_list and creditors_list:
            debtor_name, debt_amount = debtors_list.pop(0)
            creditor_name, credit_amount = creditors_list.pop(0)

            # The transaction amount is the minimum of the debt to be paid and the receivable to be received
            transfer_amount = min(debt_amount, credit_amount)
            
            # Adding the total transaction between two members
            simplified_transactions.append({
                "from": debtor_name,
                "to": creditor_name,
                "amount": round(transfer_amount, 2) # rounding to avoid floating-point errors
            })
                
            # Balances update
            remaining_debt = debt_amount - transfer_amount
            remaining_credit = credit_amount - transfer_amount

            # Reinsert the outstanding balance into the list
            if remaining_debt > 0.01: debtors_list.insert(0, (debtor_name, remaining_debt)) # if the debtor still owes money (residual balance > 0.01 for rounding), we put it back in keeping the sorting
            if remaining_credit > 0.01: creditors_list.insert(0, (creditor_name, remaining_credit)) # if the creditor is still owed money, we put it back in keeping the sorting

        # Replace the graph matrix with the new simplified matrix
        num_nodes = len(self.nodes)
        self.matrix = [[0.0] * num_nodes for _ in range(num_nodes)] # reset the matrix to 0
        for txn in simplified_transactions:
            self.add_edge(txn["from"], txn["to"], txn["amount"]) # add the new edges
            
        return balances, simplified_transactions

    def __repr__(self): # for debugging
        return f"Graph(nodes={self.nodes}, matrix={self.matrix})"
