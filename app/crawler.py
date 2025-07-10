import ccxt
import pandas as pd
from database import get_db, OHLCV, Trade, Price

from config import EXCHANGE, TIMEFRAME, SYMBOL
from datetime import datetime, timedelta, timezone
def fetch_ohlcv():
    db = next(get_db())
    time_7_days_ago = datetime.now(timezone.utc) - timedelta(days=7)
    since = int(time_7_days_ago.timestamp() * 1000)
    until = int(datetime.now(timezone.utc).timestamp()) * 1000
    try: 
        ohlcv = EXCHANGE.fetch_ohlcv(SYMBOL, timeframe=TIMEFRAME, since = since, params={'until': until})
        for candle in ohlcv:
            ts = datetime.fromisoformat(EXCHANGE.iso8601(candle[0]).replace("Z", "+00:00"))
            record = OHLCV(
                symbol = SYMBOL,
                timestamp = ts,
                open = candle[1],
                high = candle[2],
                low = candle[3],
                close = candle[4],
                volume = candle[5], 
                timeframe = TIMEFRAME
            )
            db.merge(record)
        db.commit()
    except Exception as e:
        print(f"Lỗi lấy OHLCV: {e}")
    finally:
        pass

def fetch_trades():
    db = next(get_db())
    try:
        since = int((datetime.now(timezone.utc) - timedelta(hours = 1)).timestamp()) * 1000
        until = int(datetime.now(timezone.utc).timestamp()) * 1000
        trades = EXCHANGE.fetch_trades(SYMBOL, since = since, params={'until': until})
        
        for trade in trades:
            record = Trade(
                trade_id = trade['id'],
                symbol = SYMBOL,
                timestamp = datetime.fromisoformat(EXCHANGE.iso8601(trade['timestamp']).replace("Z", "+00:00")),
                price = trade['price'],
                amount = trade['amount'],
                cost = trade['cost'],
                side = trade['side']
            )
            db.merge(record)
        db.commit()
    except Exception as e:
        print(f"Lỗi lấy trade history: {e}")
    finally:
        pass


def fetch_price():
    db = next(get_db())
    time_7_days_ago = datetime.now(timezone.utc) - timedelta(days=7)
    since = int(time_7_days_ago.timestamp() * 1000)
    until = int(datetime.now(timezone.utc).timestamp()) * 1000
    try: 
        ohlcv = EXCHANGE.fetch_ohlcv(SYMBOL, timeframe=TIMEFRAME, since = since, params={'until': until})
        for candle in ohlcv:
            ts = datetime.fromisoformat(EXCHANGE.iso8601(candle[0]).replace("Z", "+00:00"))
            high = candle[2]
            low = candle[3]
            record = Price(
                symbol = SYMBOL,
                timestamp = ts,
                price = (high + low) / 2
            )
            db.merge(record)
        db.commit()
    except Exception as e:
        print(f"Lỗi lấy Price: {e}")
    finally:
        pass




fetch_ohlcv()
fetch_trades()
fetch_price()
