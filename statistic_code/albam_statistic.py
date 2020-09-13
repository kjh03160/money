import pandas as pd


def albam_st(dates):
    albam = pd.read_csv("./data/albam/total.csv", encoding="utf-8-sig")
    albam['출근 체크 날짜'] = pd.to_datetime(albam['출근 체크 날짜'])

    from datetime import datetime

    def df_in_dates(dates):
        start_date = datetime.strptime(dates[0], '%Y-%m-%d')
        end_date = datetime.strptime(dates[-1], '%Y-%m-%d') if len(dates) > 1 else start_date
        filtered = albam.loc[(albam['출근 체크 날짜'] >= start_date) & (albam['출근 체크 날짜'] <= end_date)]
        return filtered

    albam = df_in_dates(dates)

    if len(albam) == 0:
        return False

    gets_joohue = {}.fromkeys(albam['직원명'].unique(), '-')
    employees = gets_joohue.keys()
    for name in employees:
        gets_joohue[name] = albam.loc[albam['직원명'] == name, '주휴수당 여부'].values[0]

    computed = pd.DataFrame()
    computed['직원명'] = albam['직원명']
    computed['기준급여'] = albam['기준급여'].astype(int)
    computed['근무hrs'] = albam['근무인정시간\n(B-A)-C'].apply(lambda row: row[:row.find('시간')] if '시간' in row else 0).astype(
        int)
    computed['근무mins'] = albam['근무인정시간\n(B-A)-C'].apply(
        lambda row: row[row.find('간') + 1:row.find('분')] if row != '-' else 0).astype(int)
    computed['총급여'] = albam['총급여'].astype(float)
    computed['주휴수당 여부'] = computed.apply(lambda row: gets_joohue.get(row['직원명']), axis=1)
    computed['주휴수당'] = albam['주휴수당']

    df = pd.DataFrame()
    df['직원명'] = computed['직원명'].unique()
    df['세전급여'] = 0
    df['주휴수당'] = 0
    df['4대보험'] = 0
    df['세후급여'] = 0
    df['주휴수당 여부'] = None
    for idx, row in computed.iterrows():
        name = row['직원명']
        hrs = computed[computed['직원명'] == name]['근무hrs'].sum()
        mins = computed[computed['직원명'] == name]['근무mins'].sum()
        if mins > 60:
            hrs += 1
            mins -= 60

        insurance = 0
        gross_salary = computed[computed['직원명'] == name]['총급여'].sum()
        if row['주휴수당 여부'] == 'O':
            joohue = row['주휴수당']
            df.loc[df['직원명'] == name, '주휴수당'] += joohue
            df.loc[df['직원명'] == name, '주휴수당 여부'] = "O"
            insurance = gross_salary * 0.09799
            df.loc[df['직원명'] == name, '4대보험'] = "{:,}".format(int(round(insurance, 0))) + " 원"
        else:
            df.loc[df['직원명'] == name, '주휴수당 여부'] = "X"
            df.loc[df['직원명'] == name, '주휴수당'] = '-'
            df.loc[df['직원명'] == name, '4대보험'] = "-"


        df.loc[df['직원명'] == name, '근무시간'] = f"{hrs}시간 {mins}분"
        df.loc[df['직원명'] == name, '세전급여'] = "{:,}".format(int(gross_salary)) + " 원"
        df.loc[df['직원명'] == name, '세후급여'] = "{:,}".format(int(round(gross_salary - insurance))) + " 원"

    for name in list(gets_joohue.keys()):
        if df.loc[df['직원명'] == name, '주휴수당'].values[0] != "-":
            df.loc[df['직원명'] == name, '주휴수당'] = "{:,}".format(df.loc[df['직원명'] == name, '주휴수당'].values[0]) + " 원"
    col = ['직원명', '주휴수당 여부', '근무시간', '세전급여', '주휴수당', '4대보험', '세후급여']
    df = df.sort_values(by=['근무시간'], ascending=False)
    # df[col].to_csv('알밤.csv', index=False, encoding='utf-8-sig')
    return df[col]


if __name__ == '__main__':
    albam_st(['2020-09-01'])
