import pandas as pd
import os

def albam_pre(files):
    dfs = []
    for file in files:
        xls = pd.ExcelFile(file)
        albam_new = pd.read_excel(xls, '일별 근무기록 및 급여', header=5)
        columns = ['직원명', '출근 체크 날짜', '기준급여', '근무인정시간\n(B-A)-C', '기본 급여', '주휴수당']
        h = 17
        while True:
            try:
                employee_info = pd.read_excel(xls, '기간별 급여 통계', header=h)
                gets_joohue = {}.fromkeys(employee_info['직원명'].unique(), '-')
                break
            except:
                h += 1
        employees = gets_joohue.keys()
        for name in employees:
            gets_joohue[name] = employee_info.loc[employee_info['직원명']==name, '계약상\n주휴수당 대상'].values[0]

        df = albam_new[columns]
        df['주휴수당 여부'] = df.apply(lambda row: gets_joohue.get(row['직원명']), axis=1)
        df['총급여'] = df['기본 급여'] + df['주휴수당']
        dfs.append(df)

    df = pd.concat(dfs, axis=0, ignore_index=True)

    if os.path.isfile('./data/albam/total.csv'):
        prev = pd.read_csv('./data/albam/total.csv')
        df = pd.concat([prev, df], sort=False)
        df = df.drop_duplicates(['직원명', '출근 체크 날짜', '근무인정시간\n(B-A)-C', '주휴수당'])
    df = df.sort_values(by=['출근 체크 날짜'])

    df.to_csv('./data/albam/total.csv', index=False, mode='w', encoding='utf-8-sig')
