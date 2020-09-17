import json


def now_waiting(driver, date):
    page = 1
    while True:
        url = "https://nowwaiting.co/api/v2/spots/5185/stats/orders?created_on={date}&page={page}&count=1000&order_type=&payment_type=".format(date = date, page = page)
        login_url = "https://ceo.nowwaiting.co/order_sales/history"
        driver.get_url(login_url)

        driver.get_url(url)
        pre = driver.find_by_tag("pre").text
        j = json.loads(pre)['data']['orders']
        if len(j) or page == 1:
            with open('./data/now_waiting/' + date + "_" + str(page) + '.json', 'w', encoding='UTF-8')as file:
                file.write(json.dumps(j))
            page += 1
        else:
            break

    return driver
