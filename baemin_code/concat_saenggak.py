import pandas as pd
from datetime import datetime

def concat(files):
    baemin = pd.read_csv('./data/baemin/Accumulated_data.csv')
    data = {}
    i=0
    for file in files:
        data[i] = pd.read_csv(file, encoding='CP949')
        try:
            data[i].drop(['Unnamed: 19'], axis=1, inplace=True)
        except:
            pass
        i += 1

    def find_match(data):
        data_date = data['진행시간'][0][:5].replace('/', '-')
        if data_date[-1] == '-':
            data_date = data['진행시간'][0][5:10].replace('/', '-')
        # 날짜 필터
        indexes = []
        for idx, row in baemin.iterrows():
            if row['주문시각'][5:10] == data_date:
                indexes.append(idx)
        all_matches = baemin.iloc[indexes]
        all_matches['배달요청사항'] = all_matches['배달요청사항'].str.replace(",", "")
        all_matches['요금요청'] = all_matches.apply(
            lambda row: data.loc[(row['결제금액'] == data['음식요금']) & ((row['배달요청사항'] == data['기타'].str.lstrip(": ")) | (row['요청사항'] == data['기타'].str.lstrip(": ")))].index.values,
            axis=1)
        matched = all_matches.copy()
        non_matched = all_matches.copy()
        non_matched_saenggak = data.copy()

        for idx, row in all_matches.iterrows():
            if len(row['요금요청']) == 0:
                matched.drop(idx, inplace=True)
            elif len(row['요금요청']) == 1:
                non_matched.drop(idx, inplace=True)
            else:
                non_matched.drop(idx, inplace=True)

        non_matched.drop('요금요청', axis=1, inplace=True)
        # -- clear --
        matched_idx = []

        for idx, row in matched.iterrows():
            # print(min([row['주문시각'], row['접수시각']])[5:])
            matched_dt = min([row['주문시각'], row['접수시각']])[5:].replace('-', '/')
            tdiff = {}.fromkeys(row['요금요청'].tolist(), 0)
            if len(row['요금요청']) == 1:
                best_match = row['요금요청'][0]
            else:
                for i in row['요금요청']:
                    data_dt = f"{data.loc[i, '진행시간'][:5]} {data.loc[i, '요청시간']}"
                    if data.loc[i, '진행시간'][:5][-1] == '-':
                        data_dt = f"{data.loc[i, '진행시간'][5:10].replace('-', '/')} {data.loc[i, '요청시간']}"
                    # print(data_dt, matched_dt)
                    FMT = '%m/%d %H:%M'
                    diff_calculated = abs(datetime.strptime(matched_dt, FMT) - datetime.strptime(data_dt, FMT))
                    tdiff[i] = diff_calculated
                best_match = min(tdiff, key=tdiff.get)

            matched.loc[idx, '최소시간차'] = best_match
            matched_idx.append(best_match)
            # 실제 배달료 계산
            matched.loc[idx, '실제배달료'] = data.loc[best_match, '배달요금'] + 300
        non_matched_saenggak.drop(matched_idx, inplace=True)
        return matched, non_matched, non_matched_saenggak

    a, b, c= [], [], []
    for temp in range(i):
        matched, non_matched, non_matched_saenggak = find_match(data[temp])
        a.append(matched)
        b.append(non_matched)
        c.append(non_matched_saenggak)

    matched = pd.concat(a, axis=0, ignore_index=True)
    if len(matched):
        matched.drop(['요금요청', '최소시간차'], axis=1, inplace=True)
        prev = pd.read_csv('./data/baemin/Accumulated_data.csv')
        df = pd.concat([prev, matched], sort=False)
        df = df.drop_duplicates(['주문번호'], keep='last').sort_values(by=['주문시각'], ascending=False)
        df.to_csv('./data/baemin/Accumulated_data.csv', index=False, encoding='utf-8-sig')

    not_matched = pd.concat(b, axis=0, ignore_index=True)
    not_matched.to_csv("./data/baemin/not_matched.csv", index=False, encoding='utf-8-sig')

    pd.DataFrame().to_csv("./data/baemin/not_matched.csv", index=False, encoding='utf-8-sig',  mode='a')
    not_matched_s = pd.concat(c, axis=0, ignore_index=True)
    not_matched_s.drop(['진행상황', '결제구분', '카<->현', '남은시간'], axis=1, inplace=True)
    not_matched_s.to_csv("./data/baemin/not_matched.csv", index=False, encoding='utf-8-sig', mode='a')

    if len(not_matched) != 0:
        return True
    return False

if __name__ == '__main__':
    concat(['C:/Users/kis03/Desktop/까치/data/saenggak/36fa8a94-e668-4413-a91b-85e4e2b69dbe.csv'])