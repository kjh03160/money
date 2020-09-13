import pandas as pd
from datetime import datetime

def df_in_dates(df, dates):
    start_date = datetime.strptime(dates[0], '%Y-%m-%d')
    end_date = datetime.strptime(dates[-1], '%Y-%m-%d') if len(dates) > 1 else start_date
    filtered = df.loc[(df['주문시각'] >= start_date) & (df['주문시각'] <= end_date)]
    return filtered

def service_st(dates):
    baemin = pd.read_csv('./data/baemin/Accumulated_data.csv')
    now_waiting = pd.read_csv('./data/now_waiting/Accumulated_data.csv')

    now_waiting['주문시각'] = pd.to_datetime(now_waiting['주문시각'].str[:10])
    baemin['주문시각'] = pd.to_datetime(baemin['주문시각'].str[:10])

    now_waiting = df_in_dates(now_waiting, dates)
    baemin = df_in_dates(baemin, dates)

    if len(now_waiting) == 0 or len(baemin) == 0:
        return False

    def method_stats(*l):
        df = pd.DataFrame(0, index=['포장', '매장식사', '배달'], columns=['키오스크', '챗봇', '배달의민족', '총합', '비율'])
        for data in l:
            data.loc[data['수령방법'].isnull(), '수령방법'] = 'X'
            for idx, row in data.iterrows():
                for method in row['수령방법'].replace(',','').split():
                    if method=='포장':
                        if str(row['주문번호'])[0]=='B': df.loc['포장', '배달의민족'] += len(row['항목'].split(', '))
                        elif row['서비스타입'] == '챗봇': df.loc['포장', '챗봇'] += len(row['항목'].split(', '))
                        else: df.loc['포장', '키오스크'] += len(row['항목'].split(', '))
                    elif method == '매장식사':
                        if str(row['주문번호'])[0]=='B': df.loc['매장식사', '배달의민족'] += len(row['항목'].split(', '))
                        else: df.loc['매장식사', '키오스크'] += len(row['항목'].split(', '))
                    # elif method == '배달':
                    #     if str(row['주문번호'])[0]=='B': df.loc['배달', '배달의민족'] += 1
                    #     else: df.loc['배달', '키오스크'] += 1
        df.loc['포장', '총합'] = df.loc['포장'][:-2].sum()
        df.loc['매장식사', '총합'] = df.loc['매장식사'][:-2].sum()
        method_total = df['총합'].sum()
        df['비율'] = df['총합'].apply(lambda row: f"{int(round((row/method_total)*100))} %")
        return df

    df = method_stats(baemin, now_waiting)
    df = df.reset_index()
    df = df.rename(columns={"index": "구분"})

    return df