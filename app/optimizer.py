import heapq
from typing import Dict, List, Any

def calculate_net_balances(graph) -> Dict[str, float]:
    """
    Calculates the net balance for each member by reading the adjacency matrix.
    
    Logic based on your Graph structure:
    - matrix[row][col] = Amount that 'row' owes to 'col'.
    - To calculate Balance: (Total Credit) - (Total Debt).
    
    Args:
        graph: The Graph instance containing .nodes and .matrix.
        
    Returns:
        Dict[str, float]: { 'Name': net_amount }.
                          Positive (+) = Creditor (should receive money).
                          Negative (-) = Debtor (should pay money).
    """
    nodes = graph.nodes  # List of dicts: [{'id': 0, 'name': '...'}, ...]
    matrix = graph.matrix
    num_nodes = len(nodes)
    
    # Initialize balances to 0.0 for every member
    balances = {node['name']: 0.0 for node in nodes}

    # Iterate through the matrix to process all debts
    for i in range(num_nodes):        # i = Index of the Debtor (Row)
        for j in range(num_nodes):    # j = Index of the Creditor (Column)
            
            amount = matrix[i][j] # "User i owes User j this amount"
            
            if amount > 0:
                debtor_name = nodes[i]['name']
                creditor_name = nodes[j]['name']

                # The creditor receives credit (+)
                balances[creditor_name] += amount
                # The debtor incurs debt (-)
                balances[debtor_name] -= amount

    # Round to 2 decimal places to avoid floating-point precision errors (e.g., 0.0000001)
    return {k: round(v, 2) for k, v in balances.items()}


def optimize_debts(balances: Dict[str, float]) -> List[Dict[str, Any]]:
    """
    Implements a Greedy Algorithm to minimize the total number of transactions.
    It iteratively matches the person with the highest debt to the person with the highest credit.

    Args:
        balances (Dict): The net balances calculated from the graph.

    Returns:
        List[Dict]: Optimized transactions [{'from': 'Debtor', 'to': 'Creditor', 'amount': 10.0}, ...]
    """
    debtors = []
    creditors = []

    # 1. Separate users into Debtors and Creditors lists using Heaps
    for person, amount in balances.items():
        if amount < -0.01:
            # Min-Heap for debtors. 
            # We push the negative amount directly. The smallest number (e.g., -100) 
            # represents the largest debt and will be popped first.
            heapq.heappush(debtors, (amount, person))
        
        elif amount > 0.01:
            # Max-Heap simulation for creditors.
            # Python's heapq is a Min-Heap. To pop the largest creditor first (e.g., +100),
            # we invert the value to negative (e.g., -100).
            heapq.heappush(creditors, (-amount, person))

    optimized_transactions = []

    # 2. Match Debts until everyone is settled
    while debtors and creditors:
        # Extract the biggest debtor and the biggest creditor
        debt_val, debtor = heapq.heappop(debtors)            # e.g., (-50, 'Alice')
        credit_val_neg, creditor = heapq.heappop(creditors)  # e.g., (-100, 'Bob') -> represents +100
        
        # Convert credit value back to positive for calculation
        credit_val = -credit_val_neg
        
        # Calculate the settlement amount:
        # It is the minimum of what the debtor owes vs what the creditor needs.
        amount = min(abs(debt_val), credit_val)
        
        # Record the optimized transaction
        optimized_transactions.append({
            "from": debtor,
            "to": creditor,
            "amount": round(amount, 2)
        })

        # 3. Update remaining balances
        remaining_debt = debt_val + amount      # e.g., -50 + 50 = 0
        remaining_credit = credit_val - amount  # e.g., 100 - 50 = 50

        # If the debtor still owes money, push them back to the heap
        if remaining_debt < -0.01:
            heapq.heappush(debtors, (remaining_debt, debtor))
            
        # If the creditor is still owed money, push them back to the heap
        if remaining_credit > 0.01:
            heapq.heappush(creditors, (-remaining_credit, creditor))

    return optimized_transactions