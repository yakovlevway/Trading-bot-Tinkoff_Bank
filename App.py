from datetime import datetime, timedelta
from operator import itemgetter
from numpy import insert

from tinkoff.invest import Client, OrderDirection, OrderType
from tinkoff.invest.services import SandboxService, InstrumentsService, MarketDataService

from pandas import DataFrame
from ta.trend import ema_indicator
from tinkoff.invest import Client, RequestError, CandleInterval, HistoricCandle
import tok
import pandas as pd
import matplotlib.pyplot as plt

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


                                                        #zayavka na pokupku
from PyQt5 import QtWidgets
from ui_app import Ui_App
class AppWindow(QtWidgets.QMainWindow,Ui_App):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()
        self.savefunction()
        self.savefunc()
        self.savefunc1()
        self.pokupka.clicked.connect(self.pok_pressed)
        self.prodaja.clicked.connect(self.prod_pressed)
        self.ema.clicked.connect(self.ema_pressed)
        self.infa.clicked.connect(self.status_pressed)
        self.searchb.clicked.connect(self.search_pressed)
        self.vvod= ''
        self.vvodc= ''
        self.item= ''
    def Buy(self,item):
        print("Песочница API v2 Тинькофф Инвестиции")

        with Client(tok.token) as cl:
            sb: SandboxService = cl.sandbox
            r = sb.post_sandbox_order(
                figi=item,
                quantity=4,
                # price=Quotation(units=1, nano=0),
                account_id=tok.account_id,
                order_id=datetime.now().strftime("%Y-%m-%dT %H:%M:%S"),
                direction=OrderDirection.ORDER_DIRECTION_BUY,
                order_type=OrderType.ORDER_TYPE_MARKET
            )
            r=sb.get_sandbox_portfolio(account_id=tok.account_id).positions 
            #d = sb.get_sandbox_order_state(account_id=tok.account_id, order_id="e86c42f7-0234-4ae9-b827-5f0c3809957e")
            print(type(r),"kskdkdkk")
            return r
                                                    ### zayavka na prodahu
    def Sell(self,item):
        print("Песочница API v2 Тинькофф Инвестиции")

        with Client(tok.token) as cl:
            sb: SandboxService = cl.sandbox
            r = sb.post_sandbox_order(
                figi=item,
                quantity=4,
                # price=Quotation(units=1, nano=0),
                account_id=tok.account_id,
                order_id=datetime.now().strftime("%Y-%m-%dT %H:%M:%S"),
                direction=OrderDirection.ORDER_DIRECTION_SELL,
                order_type=OrderType.ORDER_TYPE_MARKET
            )
            #r=to_df(sb.get_sandbox_portfolio(account_id=tok.account_id).positions) 
            r=sb.get_sandbox_portfolio(account_id=tok.account_id).positions 
            print(type(r),"kskdkdkk")
            return r
                                                            #### график Ema

    def create_df(self,candles : [HistoricCandle]):
        df = DataFrame([{
            'time': c.time,
            'volume': c.volume,
            'open': self.cast_money(c.open),
            'close': self.cast_money(c.close),
            'high': self.cast_money(c.high),
            'low': self.cast_money(c.low),
        } for c in candles])

        return df

    #global vvodc
    def candles(self,vvodc):
        try:
            with Client(tok.token) as client:
                r = client.market_data.get_candles(
                    figi=vvodc,
                    from_=datetime.utcnow() - timedelta(days=60),
                    to=datetime.utcnow(),
                    interval=CandleInterval.CANDLE_INTERVAL_DAY 
                )
                print(r)

                df = self.create_df(r.candles)
                df['ema'] = ema_indicator(close=df['close'], window=9)

                print(df[['time', 'close', 'ema']].tail(30))
                ax=df.plot(x='time', y='close')
                df.plot(ax=ax, x='time', y='ema')
                plt.show()
                return df
        except RequestError as e:
            print(str(e))

    def cast_money(self,v):
        """
        https://tinkoff.github.io/investAPI/faq_custom_types/
        :param v:
        :return:
        """
        return v.units + v.nano / 1e9 # nano - 9 нулей
   
                                                                            ### inform account

    def status(self):
        print("Песочница API v2 Тинькофф Инвестиции")
        account_id = 'b63f6725-b4d8-4b8f-8c70-4a8efe9ee780'
        with Client(tok.token) as cl:
            sb: SandboxService = cl.sandbox
            d = sb.get_sandbox_portfolio(account_id=account_id).positions
            print(d)  
            return d

    
    
    def Figi(self,vvod):
        with Client(tok.token) as cl:
            instruments: InstrumentsService = cl.instruments
            market_data: MarketDataService = cl.market_data
    
    
            l = []
            for method in ['shares', 'bonds', 'etfs']: # , 'currencies', 'futures']:
                for item in getattr(instruments, method)().instruments:
                    l.append({
                        'ticker': item.ticker,
                        'figi': item.figi,
                        'type': method,
                        'name': item.name,
                    })
            TICKER = vvod
            df = DataFrame(l)
            # df.to_json()
    
            df = df[df['ticker'] == TICKER]
            if df.empty:
                print(f"Нет тикера {TICKER}")
                return
    
            # print(df.iloc[0])
            print(df['figi'].iloc[0])
            return df
    

    def set_key(self):
        self.item = str(self.lineEdit.text())
        return self.item

    def savefunction(self):
        self.save.clicked.connect(lambda: self.set_key())

    def set_key2(self):
        self.vvod = str(self.paste.text())
        return self.vvod
        
    def savefunc(self):
        self.save_2.clicked.connect(lambda: self.set_key2())

    def set_key3(self):
        self.vvodc = str(self.paste_2.text())
        return self.vvodc
        
    def savefunc1(self):
        self.save_3.clicked.connect(lambda: self.set_key3())

    def pok_pressed(self):
        self.vivod.setText(str(self.Buy(self.set_key())))
    def prod_pressed(self):
        self.vivod.setText(str(self.Sell(self.set_key())))   
    def ema_pressed(self):
        self.vivod.setText(str(self.candles(self.set_key3()))) 
    def status_pressed(self):
        self.vivod.setText(str(self.status())) 
    def search_pressed(self):
        self.vivod.setText(str(self.Figi(self.set_key2()))) 




        