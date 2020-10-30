from universe_selection import MyUniverseSelectionModel
from alpha import MyAlphaModel
from execution import MyExecutionModel


class EMACrossover(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2000, 1, 1)
        #self.SetEndDate(2019, 12, 31)
        self.SetCash(1000)
        self.SetWarmup(timedelta(30))
        self.Settings.FreePortfolioValuePercentage = 0.1
        self.SetBrokerageModel(BrokerageName.InteractiveBrokersBrokerage, AccountType.Cash)
        
        # Universe Selection Model
        self.securities = []    # stores 5 'best' securities
        self.UniverseSettings.Resolution = Resolution.Hourly
        self.UniverseSelectionModel = MyUniverseSelectionModel(self)
        self.AddUniverse(self.UniverseSelectionModel.SelectCoarse, self.UniverseSelectionModel.SelectFine)
        
        # Alpha Model
        self.AlphaModel = MyAlphaModel()
        self.holdings = []
        
        # Execution Model
        self.ExecutionModel = MyExecutionModel()
        
        # Schedule rebalancing
        self.AddEquity('SPY', Resolution.Daily)
        self.Schedule.On(self.DateRules.EveryDay('SPY'), self.TimeRules.At(9, 30), Action(self.RebalancePortfolio))
        
        
    def RebalancePortfolio(self):
        
        insights = self.AlphaModel.AlphaScores(self, self.securities, self.holdings)
        self.ExecutionModel.ExecuteOrders(self, insights)
        
        
    def OnData(self, data):
        pass