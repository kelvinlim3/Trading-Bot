class MyUniverseSelectionModel:
    
    def __init__(self, algorithm):
        self.algorithm = algorithm
        
    def SelectCoarse(self, coarse):
        
        # filter by fundamental data and price and sorted by liquidity
        filtered = [x for x in coarse if x.HasFundamentalData and 5 < x.Price < 10]
        most_liquid = sorted(filtered, key=lambda x: x.DollarVolume, reverse=True)
        
        return [x.Symbol for x in most_liquid[:100]]
        
    
    def SelectFine(self, fine):
        
        sectors = [MorningstarSectorCode.FinancialServices, MorningstarSectorCode.ConsumerDefensive, MorningstarSectorCode.Healthcare,
                    MorningstarSectorCode.Energy, MorningstarSectorCode.Technology]
        
        # from each of the 5 sectors above, select the stock with the highest market cap
        universe = []
        for sector in sectors:
            filtered_by_sector = [x for x in fine if x.AssetClassification.MorningstarSectorCode == sector]
            highest_market_caps = sorted(filtered_by_sector, key=lambda x: x.MarketCap, reverse=True)[:1]
            universe += highest_market_caps
            
        self.algorithm.securities = [x.Symbol for x in universe]
        
        return [x.Symbol for x in universe]