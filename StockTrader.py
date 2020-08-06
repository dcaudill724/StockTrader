import alpaca_trade_api as tradeapi
import yahoo_fin as yf
from yahoo_fin import stock_info as si
import datetime

BASE_URL = "https://paper-api.alpaca.markets"
ACCOUNT_URL = "{}/v2/account".format(BASE_URL);

APCA_API_KEY_ID = "PK88C7MWSJ41JHQ9Y8XD"
APCA_API_SECRET_KEY = "BkCQaeyIy/HmcsEfrWGObGCZ81CRJZfMKRIyN7eG"

class StockBot :
    def __init__(self):
        print(">>> Initializing Stock Bot <<<")
        #Initialize all of the data to be evaluated
        #Stockdata will be updated as quickly as is allowed by the api
        self.api = tradeapi.REST(APCA_API_KEY_ID, APCA_API_SECRET_KEY, BASE_URL, api_version='v2')
        self.stocklist = ["AAPL", "MSFT", "GOGO"]
        self.stockdata = []
        for i in self.stocklist:
            self.stockdata.append(si.get_data(i))

        #Settings
        self.movingAverageDays = 200
        self.movingAverage = 0.0

        #Used to keep track of time if the api requires
        self.lastTime = float(datetime.datetime.now().second)

        #call init functions
        self.fetch_stock_data()
        self.calculate_moving_averages()

    def run(self):
        print(">>> Baking Bread <<<")
        
        #while(True):
            #if (float(datetime.datetime.now().second) - self.lastTime > float(1)):
        #self.eval_prices()
        self.lastTime = float(datetime.datetime.now().second)
        #print(self.api.get_account())
    
    #used to calculate the 200 day moving average
    def calculate_moving_averages(self):
        for stockHistory in self.stockdata:
            sum = 0.0
            denominator = 0.0
            
            for j in stockHistory['high']:
                sum += float(j)
                denominator += 1
            for j in stockHistory['low']:
                sum += float(j)
                denominator += 1
            for j in stockHistory['open']:
                sum += float(j)
                denominator += 1
            for j in stockHistory['close']:
                sum += float(j)
                denominator += 1

            self.movingAverage = sum / denominator

            print(str(sum) + " / " + str(denominator) + " = " + str(self.movingAverage) + " : " + stockHistory["ticker"][0])

    def fetch_stock_data(self):
        today = datetime.datetime.now().date()
        backdate = today - datetime.timedelta(days=self.movingAverageDays)

        for i in range(len(self.stocklist)):
            self.stockdata[i] = si.get_data(self.stocklist[i], backdate)
        #print(self.stockdata)

    def eval_prices(self):
        for i in range(len(self.stocklist)):
            print(str(self.stocklist[i]) + " : " + str(si.get_live_price(self.stocklist[i])))

sb = StockBot()
sb.run()