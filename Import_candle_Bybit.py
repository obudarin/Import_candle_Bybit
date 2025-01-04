import aiohttp
import asyncio
import pandas as pd
from datetime import datetime, timedelta
import nest_asyncio

nest_asyncio.apply()

symbol = 'ETHUSDT'
interval = '60'
start_time = int(datetime(2024, 1, 1).timestamp() * 1000)
end_time = int(datetime(2024, 12, 31).timestamp() * 1000)

async def fetch_bybit_ohlcv(session, symbol, interval, start_time, end_time, category='spot', limit=200):
    url = 'https://api.bybit.com/v5/market/kline'
    params = {
        'category': category,
        'symbol': symbol,
        'interval': interval,
        'start': start_time,
        'end': end_time,
        'limit': limit
    }

    async with session.get(url, params=params) as response:
        print(f"Запрос URL: {response.url}")
        print(f"Код состояния ответа: {response.status}")
        data = await response.json()

        if 'result' in data and 'list' in data['result']:
            return data['result']['list']
        else:
            print(f"Неожиданный формат ответа: {data}")
            return None


async def fetch_all_ohlcv(symbol, interval, start_time, end_time, category='spot', limit=200):
    all_data = []
    current_time = start_time
    one_day_in_ms = int(timedelta(days=1).total_seconds() * 1000)

    async with aiohttp.ClientSession() as session:
        tasks = []

        while current_time < end_time:
            next_time = min(current_time + one_day_in_ms, end_time)
            tasks.append(fetch_bybit_ohlcv(session, symbol, interval, current_time, next_time, category, limit))

            current_time = next_time

        results = await asyncio.gather(*tasks)

        for data in results:
            if data:
                all_data.extend(data)

    return all_data


def format_data(data):
    if data is None:
        return None
    df = pd.DataFrame(data, columns=['start_time', 'open', 'high', 'low', 'close', 'volume', 'turnover'])
    df['start_time'] = pd.to_numeric(df['start_time'])
    df['start_time'] = pd.to_datetime(df['start_time'], unit='ms')
    df.set_index('start_time', inplace=True)
    df = df.apply(pd.to_numeric)
    df = df.sort_values(by='start_time')
    return df

def save_to_csv(df, filename):
    df.to_csv(filename, sep=';')
    print(f"Данные сохранены в {filename}")

def format_data_prep(df):
    if df is None:
        return None
    df = df.copy()  # Create a copy to avoid modifying the original DataFrame
    df['DATE'] = df.index.strftime('%m/%d/%Y')
    df['TIME'] = df.index.strftime('%H:%M')
    df = df[['DATE', 'TIME', 'open', 'high', 'low', 'close', 'volume']]
    df.columns = ['DATE', 'TIME', 'OPEN', 'HIGH', 'LOW', 'CLOSE', 'VOL']
    return df

def save_to_prep_csv(df, filename):
    df.to_csv(filename, sep=';', index=False, header=False, float_format='%.8f') # Added float_format
    print(f"Данные сохранены в {filename}")

async def main():
    all_data = await fetch_all_ohlcv(symbol, interval, start_time, end_time)
    df = format_data(all_data)

    if df is not None:
        print(df.head())
        print(df.tail())
        save_to_csv(df, 'data.csv')
        df_prep = format_data_prep(df)
        save_to_prep_csv(df_prep, 'prep_data.csv')
    else:
        print("Нет данных.")


# Запуск асинхронного главного процесса
loop = asyncio.get_event_loop()
loop.run_until_complete(main())