import pandas as pd
from datetime import datetime

def concat(files):
    baemin = pd.read_csv('./data/baemin/Accumulated_data.csv')
    baemin['날짜'] = baemin['주문시각'].str[:10]
    data = {}
    i=0
    for file in files:
        data[i] = pd.read_excel(file, header=3)
        try:
            data[i].drop(['Unnamed: 19'], axis=1, inplace=True)
        except:
            pass
        i += 1

    def find_match(new):
        non_matched = new.copy()
        baemin_index = []
        ind = []

        new['최종매치'] = '-'
        remove_words = ['배달 요청사항:', '배달 요청사항', '배달 요청사', '배달 요청', '배달 요', '배달 ', '배달', '배']
        FMT = '%m-%d %H:%M'
        for idx, row in new.iterrows():
            final = []
            order_amt = row['음식가격']
            order_memo = row['기사메모']
            order_date = datetime.date(row['날짜'])
            ind.extend(baemin[(baemin['날짜'] == str(order_date))].index.tolist())
            indexes = baemin[(baemin['날짜'] == str(order_date)) & (baemin['결제금액'] == order_amt)].index.tolist()
            if type(order_memo) != float:
                order_memo = order_memo.replace('배민 ', '').replace('<관)수정-주소>', '').strip()
                if '배달 요청사항: ' in order_memo:
                    if len(order_memo.split('배달 요청사항: ')[1]) > 1:
                        delivery_memo = order_memo.split('배달 요청사항: ')[1].strip()
                        order_memo = order_memo.split('배달 요청사항: ')[0].strip()
                        for bm_idx in indexes:
                            if (order_memo in str(baemin.loc[bm_idx, '요청사항'])) & (
                                    delivery_memo in baemin.loc[bm_idx, '배달요청사항']):
                                final.append(bm_idx)
                elif len(order_memo) < 1:
                    for bm_idx in indexes:
                        if (str(baemin.loc[bm_idx, '요청사항']) == 'nan') & (str(baemin.loc[bm_idx, '배달요청사항']) == 'nan'):
                            final.append(bm_idx)
                else:
                    for word in remove_words:
                        order_memo = order_memo[:-8] + order_memo[-8:].replace(word, '')
                    order_memo = order_memo.strip()
                    for bm_idx in indexes:
                        if order_memo in str(baemin.loc[bm_idx, '요청사항']):
                            final.append(bm_idx)
                        elif (str(baemin.loc[bm_idx, '요청사항']) == 'nan') | (str(baemin.loc[bm_idx, '요청사항']) == '-'):
                            if (order_memo in str(baemin.loc[bm_idx, '배달요청사항'])): final.append(bm_idx)
            else:
                for bm_idx in indexes:
                    if (type(baemin.loc[bm_idx, '요청사항']) == float) & (type(baemin.loc[bm_idx, '배달요청사항']) == float):
                        final.append(bm_idx)

            if len(final) > 1:
                new_time = f"{str(row['날짜'])[5:10]} {str(row['요청시간'])[:5]}"
                tdiff = {}.fromkeys(final, 0)
                for bm_idx in final:
                    bm_time = baemin.loc[bm_idx, '주문시각'][5:-3]
                    diff_calculated = abs(datetime.strptime(new_time, FMT) - datetime.strptime(bm_time, FMT))
                    tdiff[bm_idx] = diff_calculated
                final = [min(tdiff, key=tdiff.get)]

            new.at[idx, '최종매치'] = final
            if len(final) == 0:
                new.drop(index=idx, inplace=True)

            else:
                non_matched.drop(index=idx, inplace=True)
                baemin_index.append(final[0])

        ind = set(ind)
        all_matches = baemin.loc[ind]

        for idx, row in new.iterrows():
            ba = row['최종매치'][0]
            all_matches.loc[ba, '실제배달료'] = row['배달료'] + 300

        not_baemin = all_matches.drop(index=list(baemin_index), axis=0)
        all_matches = all_matches.drop(['날짜'], axis=1)

        return all_matches, non_matched, not_baemin

    a, b, c= [], [], []
    for temp in range(i):
        matched, non_matched, non_matched_moa = find_match(data[temp])
        a.append(matched)
        b.append(non_matched)
        c.append(non_matched_moa)

    matched = pd.concat(a, axis=0, ignore_index=True)
    if len(matched):
        prev = pd.read_csv('./data/baemin/Accumulated_data.csv')
        df = pd.concat([prev, matched], sort=False)
        df = df.drop_duplicates(['주문번호'], keep='last').sort_values(by=['주문시각'], ascending=False)
        df.to_csv('./data/baemin/Accumulated_data.csv', index=False, encoding='utf-8-sig')

    not_matched = pd.concat(b, axis=0, ignore_index=True)
    not_matched.to_csv("./data/baemin/not_matched.csv", index=False, encoding='utf-8-sig')

    pd.DataFrame().to_csv("./data/baemin/not_matched.csv", index=False, encoding='utf-8-sig',  mode='a')
    not_matched_s = pd.concat(c, axis=0, ignore_index=True)
    # not_matched_s.drop(['진행상황', '결제구분', '카<->현', '남은시간'], axis=1, inplace=True)
    not_matched_s.to_csv("./data/baemin/not_matched.csv", index=False, encoding='utf-8-sig', mode='a')

    if len(not_matched) != 0:
        return True
    return False
