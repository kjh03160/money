import pandas as pd

def albam_st(dates):
    path = '../data/albam/'
    files = []
    for date in dates:
        files.append(path + date + ".csv")
    li = []
    print(files)
    for file in files:
        df = pd.read_csv(file, sep=',', escapechar='\n')
        li.append(df)

    albam = pd.concat(li, axis=0, ignore_index=True)

    computed = pd.DataFrame()
    computed['이름'] = albam['이름'].apply(lambda row: row[:row.find('(')])
    computed['시급'] = albam['시급'].astype(int)
    computed['근무hrs'] = albam['근무인정시간'].apply(lambda row: row[:row.find('시간')] if row != '-' else 0).astype(int)
    computed['근무mins'] = albam['근무인정시간'].apply(lambda row: row[row.find('간')+1:row.find('분')] if row != '-' else 0).astype(int)
    computed['총급여'] = albam['총급여'].astype(float)

    df = pd.DataFrame()
    df['이름'] = computed['이름'].unique()
    df['세전급여'] = 0
    df['4대보험'] = 0
    df['세후급여'] = 0
    for idx, row in computed.iterrows():
        name = row['이름']
        hrs = computed[computed['이름'] == name]['근무hrs'].sum()
        mins = computed[computed['이름'] == name]['근무mins'].sum()
        if mins > 60:
            hrs += 1
            mins -= 60

        gross_salary = row['총급여']
        insurance = gross_salary * 0.009628

        df.loc[df['이름'] == name, '일한시간'] = f"{hrs}시간 {mins}분"
        df.loc[df['이름'] == name, '세전급여'] += gross_salary
        df.loc[df['이름'] == name, '4대보험'] += round(insurance, 2)
        df.loc[df['이름'] == name, '세후급여'] += round(gross_salary - insurance)

    col = ['이름', '일한시간', '세전급여', '4대보험', '세후급여']
    df[col].to_csv('알밤.csv', index=False, encoding='utf-8-sig')

if __name__ == '__main__':
    albam_st(['2020-08-24', '2020-08-25', '2020-08-26', '2020-08-27', '2020-08-28'])