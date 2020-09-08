import pandas as pd
from datetime import datetime


def df_in_dates(df, dates):
    start_date = datetime.strptime(dates[0], '%Y-%m-%d')
    end_date = datetime.strptime(dates[-1], '%Y-%m-%d') if len(dates) > 1 else start_date
    filtered = df.loc[(df['주문시각'] >= start_date) & (df['주문시각'] <= end_date)]
    return filtered


def deliver_st(dates):
    data = pd.read_csv('./data/baemin/Accumulated_data.csv')
    data['주문시각'] = pd.to_datetime(data['주문시각'].str[:10])
    data = df_in_dates(data, dates)

    if len(data) == 0:
        return False

    data = data.dropna(subset=['실제배달료'])

    # data = data.d
    baemin_delivery_tip = dict()
    actual_delivery_tip = dict()
    food_price = dict()
    count = dict()

    for idx, row in data.iterrows():
        for address in row['주소'].split():
            if '동' in address:
                if address in count:
                    baemin_delivery_tip[address] += row['배달팁']
                    actual_delivery_tip[address] += row['실제배달료']
                    food_price[address] += row['주문금액']
                    count[address] += 1
                else:
                    baemin_delivery_tip[address] = row['배달팁']
                    actual_delivery_tip[address] = row['실제배달료']
                    food_price[address] = row['주문금액']
                    count[address] = 1

    baemin_delivery_tip = dict((k, round(baemin_delivery_tip[k] / count[k])) for k in baemin_delivery_tip)
    actual_delivery_tip = dict((k, round(actual_delivery_tip[k] / count[k])) for k in actual_delivery_tip)
    food_price = dict((k, round(food_price[k] / count[k])) for k in food_price)
    baemin_actual_diff = dict((k, baemin_delivery_tip[k] - actual_delivery_tip[k]) for k in baemin_delivery_tip)

    columns = list(count.keys()) + ['총합']
    df = pd.DataFrame(0, index=['배민배달팁', '실제배달료', '차액', '음식값'], columns=columns)

    if len(data) == 0:
        df = df.reset_index()
        df = df.rename({"index" : "구분"})
        return df
    col_num = len(df.columns) - 1
    df.loc['배민배달팁'] = baemin_delivery_tip
    df.loc['배민배달팁', '총합'] = round(df.loc['배민배달팁'].sum() / col_num)

    df.loc['실제배달료'] = actual_delivery_tip
    df.loc['실제배달료', '총합'] = round(df.loc['실제배달료'].sum() / col_num)

    df.loc['음식값'] = food_price
    df.loc['음식값', '총합'] = round(df.loc['음식값'].sum() / col_num)

    df.loc['차액'] = baemin_actual_diff
    df.loc['차액', '총합'] = round(df.loc['차액'].sum() / col_num)

    df = df.reset_index()
    df = df.rename(columns={"index": "구분"})

    return df