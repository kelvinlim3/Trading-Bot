class MyExecutionModel:
    
    def __init__(self):
        pass
    
    def ExecuteOrders(self, algorithm, insights):
        
        if not insights:
            return
        
        for security, action in insights.items():
            
            if action == 'BUY':
                algorithm.SetHoldings(security, 0.2)
                algorithm.holdings.append(security)
                
            elif action == 'SELL':
                algorithm.Liquidate(security)
                algorithm.holdings.remove(security)