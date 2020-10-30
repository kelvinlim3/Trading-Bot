class MyAlphaModel:
    
    def __init__(self):
        self.averages = {1:1}
    
    def AlphaScores(self, algorithm, securities, holdings):
        
        insights = {}
        
        new = list(set(securities) - set(holdings))  # new securities in universe that are not invested
        
        buy_count = 0
        
        for security in new:
            
            if buy_count == 5 - len(holdings):
                break
            
            current_time = algorithm.Time
            current_price = algorithm.Portfolio[security].Price
            
            if security not in self.averages:
                history = algorithm.History(security, 30, Resolution.Daily)
                self.averages[security] = SelectionData(history)
                
            self.averages[security].update(current_time, current_price)
            
            if not self.averages[security].std.IsReady:
                return
            
            # buy security if +ve crossover and its not in portfolio
            if self.averages[security].action(current_price) == 'BUY':
                insights[security] = 'BUY'
                buy_count += 1
            else:
                insights[security] = 'KEEP'
                
        for security in holdings:
            
            current_time = algorithm.Time
            current_price = algorithm.Portfolio[security].Price
            bought_quantity = algorithm.Portfolio[security].Quantity
            bought_price = algorithm.Portfolio[security].AveragePrice
            
            self.averages[security].update(current_time, current_price)
            
            # price at which stock was bought plus 2 times IB fee
            fee = min(max(1, 0.005 * bought_quantity), 0.01 * current_price * bought_quantity)
            sell_threshold = 2 * fee + bought_price
            
            # sell security if -ve crossover and its in portfolio and price above threshold or it is below the stop loss limit
            if (self.averages[security].action(current_price) == 'SELL' and current_price > sell_threshold) or current_price < self.averages[security].loss_limit:
                insights[security] = 'SELL'
            else:
                insights[security] = 'KEEP'
            
        return insights        
        
    
class SelectionData:
    
    def __init__(self, history):
        self.slow = ExponentialMovingAverage(21)
        self.fast = ExponentialMovingAverage(9)
        self.std = StandardDeviation(30)
        for bar in history.itertuples():
            self.slow.Update(bar.Index[1], bar.close)
            self.fast.Update(bar.Index[1], bar.close)
            self.std.Update(bar.Index[1], bar.close)
        self.holding = False
        self.loss_limit = -1
    
    def update(self, time, price):
        self.slow.Update(time, price)
        self.fast.Update(time, price)
        self.std.Update(time, price)
    
    def action(self, price):
        if self.fast.Current.Value > self.slow.Current.Value and not self.holding:
            self.loss_limit = price - 2 * self.std.Current.Value
            self.holding = True
            return 'BUY'
            
        elif self.fast.Current.Value < self.slow.Current.Value:
            self.holding = False
            return 'SELL'
            
        return 'KEEP'