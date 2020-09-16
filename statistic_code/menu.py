import pandas as pd
from datetime import datetime


def df_in_dates(df, dates):
    start_date = datetime.strptime(dates[0], '%Y-%m-%d')
    end_date = datetime.strptime(dates[-1], '%Y-%m-%d') if len(dates) > 1 else start_date
    filtered = df.loc[(df['주문시각'] >= start_date) & (df['주문시각'] <= end_date)]
    return filtered


def menu_st(dates):
    nw = pd.read_csv('./data/now_waiting/Accumulated_data.csv', encoding='utf-8-sig')
    bm = pd.read_csv('./data/baemin/Accumulated_data.csv', encoding='utf-8-sig')

    nw['주문시각'] = pd.to_datetime(nw['주문시각'].str[:10])
    bm['주문시각'] = pd.to_datetime(bm['주문시각'].str[:10])

    nw = df_in_dates(nw, dates)
    bm = df_in_dates(bm, dates)

    if len(nw) == 0 and len(bm) == 0:
        return False

    index1 = pd.MultiIndex.from_product([['샐러드', '메인추가'], ['목살', '닭가슴살', '숲속', '연어']])
    index2 = pd.MultiIndex.from_tuples(
        [('샐러드', '이너프'), ('extra', '고구마'), ('extra', '계란'), ('드레싱', '발사믹'), ('드레싱', '오리엔탈'), ('드레싱', '렌치')])
    columns = ['배달의민족', '키오스크', '챗봇', '현금', '총합', '비율']

    frame = pd.DataFrame(None, index=index1, columns=columns)
    frame = frame + pd.DataFrame(None, index=index2, columns=columns)
    frame.fillna(0, inplace=True)
    frame = frame.sort_index(ascending=False)

    def fill_stats(*dfs):
        df = frame.copy()
        method = None
        for data in dfs:
            data['항목'] = data['항목'] .fillna("")
            for idx, row in data.iterrows():
                if row['결제방법'] == '바로결제' or row['결제방법'] == '만나서결제':
                    method = '배달의민족'
                elif row['서비스타입'] == '현금':
                    method = '현금'
                elif row['서비스타입'] == '나우웨이팅 POS':
                    method = '키오스크'
                elif row['서비스타입'] == '챗봇':
                    method = '챗봇'
                # 샐러드 칼럼
                for item in row['항목'].split(', '):
                    if '이너프' in item:
                        df.loc[('샐러드', '이너프'), method] += 1
                    elif '목살' in item:
                        df.loc[('샐러드', '목살'), method] += 1
                    elif '닭가슴살' in item:
                        df.loc[('샐러드', '닭가슴살'), method] += 1
                    elif '숲속' in item:
                        df.loc[('샐러드', '숲속'), method] += 1
                    elif '연어' in item:
                        df.loc[('샐러드', '연어'), method] += 1

                # 메인추가, extra 칼럼
                if type(row['추가선택']) != float:
                    for item in row['추가선택'].split(', '):
                        if '고구마' in item:
                            if 'X' in item:
                                #                                 df.loc[('extra', '고구마'), method] -= 1
                                pass
                            elif '100' in item:
                                df.loc[('extra', '고구마'), method] += 2
                            else:
                                df.loc[('extra', '고구마'), method] += 1
                        elif '계란' in item or '삶은 달걀' in item or '삶은' in item:
                            if 'X' in item:
                                #                                 df.loc[('extra', '계란'), method] -= 1
                                pass

                            else:
                                df.loc[('extra', '계란'), method] += 1
                        elif '목살' in item:
                            if 'X' in item:
                                #                                 df.loc[('메인추가', '목살'), method] -= 1
                                pass

                            else:
                                df.loc[('메인추가', '목살'), method] += 1
                        elif '닭가슴살' in item:
                            if 'X' in item:
                                #                                 df.loc[('메인추가', '닭가슴살'), method] -= 1
                                pass

                            else:
                                df.loc[('메인추가', '닭가슴살'), method] += 1
                        elif '숲속' in item:
                            if 'X' in item:
                                #                                 df.loc[('메인추가', '숲속'), method] -= 1
                                pass

                            else:
                                df.loc[('메인추가', '숲속'), method] += 1
                        elif '연어' in item:
                            if 'X' in item:
                                #                                 df.loc[('메인추가', '연어'), method] -= 1
                                pass
                            else:
                                df.loc[('메인추가', '연어'), method] += 1

                # 드레싱 칼럼
                if type(row['드레싱']) != float:
                    for item in row['드레싱'].split(', '):
                        if '발사믹' in item:
                            if 'X' in item:
                                #                                 df.loc[('드레싱', '발사믹'), method] -= 1
                                pass

                            else:
                                df.loc[('드레싱', '발사믹'), method] += 1
                        elif '오리엔탈' in item:
                            if 'X' in item:
                                #                                 df.loc[('드레싱', '오리엔탈'), method] -= 1
                                pass

                            else:
                                df.loc[('드레싱', '오리엔탈'), method] += 1
                        elif '렌치' in item:
                            if 'X' in item:
                                #                                 df.loc[('드레싱', '렌치'), method] -= 1
                                pass

                            else:
                                df.loc[('드레싱', '렌치'), method] += 1

        # 총합 칼럼
        df['총합'] = df.sum(axis=1)

        # 비율 칼럼
        salads = df.loc['샐러드', '총합'].sum()
        toppings = df.loc['메인추가', '총합'].sum()
        extras = df.loc['extra', '총합'].sum()
        dressings = df.loc['드레싱', '총합'].sum()
        df = df.fillna(0)

        for idx in df.index:
            pair = (idx[0], idx[1])
            if idx[0] == '샐러드':
                df.loc[pair, '비율'] = f"{int((df.loc[pair, '총합'] / salads) * 100)} %"
            elif idx[0] == '드레싱':
                df.loc[pair, '비율'] = f"{int((df.loc[pair, '총합'] / dressings) * 100)} %"
            elif idx[0] == '메인추가':
                df.loc[pair, '비율'] = f"{int((df.loc[pair, '총합'] / toppings) * 100)} %"
            elif idx[0] == 'extra':
                df.loc[pair, '비율'] = f"{int((df.loc[pair, '총합'] / extras) * 100)} %"
        return df

    menu_stats = fill_stats(bm, nw)
    menu_stats.to_csv('./data/dummy.csv', encoding='utf-8-sig')
    menu_stats = pd.read_csv('./data/dummy.csv', encoding='utf-8-sig')

    n1 = None
    for i in range(len(menu_stats)):
        val = menu_stats.iloc[i]['Unnamed: 0']
        if val != n1:
            n1 = val
        else:
            menu_stats.iloc[i, 0] = ""

    menu_stats = menu_stats.rename(columns={'Unnamed: 0': '종류',
                                            'Unnamed: 1': '메뉴'})
    return menu_stats
