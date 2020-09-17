
import pandas as pd
import os
import datetime
import time
def baemin_7(driver, date):
    if driver.driver.title == "ERROR: The request could not be satisfied":
        return False

    # nav = driver.find_all_by_css("nav.Paging ul li")[-2]
    result = []
    flag = False

    while True:
        time.sleep(0.3)
        trs = driver.find_all_by_css("tbody tr")

        for row in trs:
            order_date = driver.find_by_css_with_obj(row, "td:nth-child(2)").text[4:]
            test = order_date.replace(".", '')
            test = list(map(int, test.split()[:3]))

            order_time = datetime.datetime(2000 + test[0], test[1], test[2])
            rq = list(map(int, date.split("-")))
            rq = datetime.datetime(rq[0], rq[1], rq[2])
            if order_time < rq:
                flag = True
                break

            if order_time != rq:
                # if (order_time - rq).days > 3:
                #     break
                continue

            order = driver.find_by_css_with_obj(row, "a")
            temp = {'주문번호': None, '수령방법': None, '결제방법': None, '항목': [], '추가선택': [],
                    '드레싱': [], '서비스타입': '배민', '주문금액': 0,
                    '배달팁': 0, '결제금액': 0, '주문시각': None, '접수시각': None,
                    '배달시각': None, '주소': None, '요청사항': None, '배달요청사항' : None, '실제배달료' : None}
            driver.click(order)
            time.sleep(0.5)

            tbodys = driver.find_all_by_css("div.content tbody")

            trs2 = driver.find_all_by_tag_with_obj(tbodys[1], "tr")
            text_ = driver.find_by_tag_with_obj(trs2[6], "td").text

            temp['주문시각'] = text_.replace(". ", "-")
            trs = driver.find_all_by_tag_with_obj(tbodys[0], "tr")

            count = 1

            for tr in trs:
                tds = driver.find_all_by_tag_with_obj(tr, "td")
                if tr.get_attribute('class'):
                    if '드레싱' in tr.text:
                        for _ in range(count):
                            temp['드레싱'].append(tr.text.strip().split()[1])
                    elif '추가' in tr.text:
                        for _ in range(count):
                            temp['추가선택'].append((tr.text.strip().split(" 추가")[0][2:]))
                else:
                    count = int(tds[2].text.strip())
                    item_ = tds[0].text.strip()
                    if '추가' in item_:
                        for _ in range(count):
                            temp['드레싱'].append(' '.join(item_.split()[1:3]))
                    else:
                        for _ in range(count):
                            temp['항목'].append(item_)

            temp['수령방법'] = driver.find_by_tag_with_obj(trs2[0], "td").text
            temp['결제방법'] = driver.find_by_tag_with_obj(trs2[1], "td").text.split(" | ")[0]
            temp['주소'] = driver.find_by_tag_with_obj(trs2[2], "td").text
            temp['요청사항'] = driver.find_by_tag_with_obj(trs2[3], "td").text
            temp['배달요청사항'] = driver.find_by_tag_with_obj(trs2[4], "td").text
            temp['접수시각'] = driver.find_by_tag_with_obj(trs2[7], "td").text.replace(". ", "-")
            temp['배달시각'] = driver.find_by_tag_with_obj(trs2[8], "td").text.replace(". ", "-")

            footer = driver.find_all_by_css("tfoot tr")
            temp['배달팁'] = int(driver.find_by_css_with_obj(footer[0], "td.text-right").text.split()[0].replace(",", ""))
            temp['결제금액'] = int(driver.find_by_css_with_obj(footer[1], "td.text-right").text.split()[0].replace(",", ""))

            temp['주문번호'] = driver.find_by_css("div.order-detail-orderNo").text.split()[1]
            temp['주문금액'] = temp['결제금액'] - temp['배달팁']

            temp['드레싱'] = ", ".join(temp['드레싱'])
            temp['추가선택'] = ", ".join(temp['추가선택'])
            temp['항목'] = ", ".join(temp['항목'])
            result.append(temp)
            close = driver.find_by_css( "button.popup")
            driver.click(close)


        nav = driver.find_all_by_css("nav.Paging ul li")[-2]

        if flag or nav.get_attribute("class") != "":
            break
        a = driver.find_by_tag_with_obj(nav, 'a')
        driver.click(a)
        time.sleep(0.2)


    df = pd.DataFrame(result)
    df.to_csv("data/baemin/" + date + '.csv', encoding='utf-8-sig', index=False)

    if os.path.isfile('./data/baemin/Accumulated_data.csv'):
        prev = pd.read_csv('./data/baemin/Accumulated_data.csv')
        filter1 = prev['주문시각'].str.contains(date)
        filter2 = prev['서비스타입'] == "배민"
        dup = prev[filter1 & filter2].index
        prev = prev.drop(dup)
        df = pd.concat([prev, df], sort=False)
    df = df.sort_values(by=['주문시각'], ascending=False)

    df.to_csv('./data/baemin/Accumulated_data.csv', index=False, mode='w', encoding='utf-8-sig')
    return driver