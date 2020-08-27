from selenium_class import Driver
import time
from urllib import parse

def main():
    date = input("날짜를 입력해주세요(형식 : 2020-00-00) : ")
    while len(date) != len("2020-00-00") or date[4] != "-" or date[7] != "-":
        print("날짜 형식을 다시 확인해주세요!")
        date = input("날짜를 입력해주세요(형식 : 2020-00-00) : ")

    driver = Driver()


    driver.get_url("https://ceo.baemin.com/self-service/orders/history")

    driver.driver.implicitly_wait(10)

    id = driver.find_by_id("id")
    id.send_keys("sudaje1")

    pw = driver.find_by_id("pw")
    pw.send_keys("sujung4710!!")

    login = driver.find_by_id("btnLogin")
    driver.click(login)

    time.sleep(1)
    url = "https://ceo.baemin.com/v1/orders?__ts=1598455546716&sort=ORDER_DATETIME&shopNo=&adInventoryKey=&purchaseType=&orderStatus=CLOSED&startDate={start}&endDate={end}&offset=0&limit={limit}&token="
    url = url.format(start = date, end = date, limit=1000)
    driver.get_url(url)
    pre = driver.find_by_tag("pre").text

    with open('data/dummy.json', 'w', encoding='UTF-8')as file:
        file.write(pre)


    import json
    import pandas as pd
    with open('data/dummy.json', 'r', encoding='UTF-8')as file:
        x = json.load(file)['data']['histories']
        if len(x) == 0:
            print("주문 내역이 없습니다.")
            return

    df = pd.DataFrame(x)
    orders = list(df['orderNo'])

    urls  = ["https://ceo.baemin.com/v1/orders/"+  id + "?__ts=1598459367645" for id in orders]

    time.sleep(1)
    with open('data/' + date + '.json', 'w', encoding='UTF-8') as file:
        temp = []
        for i in urls:
            driver.get_url(parse.unquote(i))
            pre = driver.find_by_tag("pre").text
            temp.append(json.loads(pre)['data'])
        file.write(json.dumps(temp))

    driver.close()

    from result_df import to_csv
    print("수집 완료")
    print("csv 생성 중")
    to_csv(date)

    from graph import graph
    graph()

if __name__ == '__main__':
    main()