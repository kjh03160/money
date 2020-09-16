import time

def now_waiting_main(driver, date, i):
    if i == 0:
        login_url = "https://ceo.nowwaiting.co/order_sales/history"
        driver.get_url(login_url)

        id_box = driver.find_by_id("email")
        id_box.send_keys("2753034@naver.com")

        pw_box = driver.find_by_id("password")
        pw_box.send_keys("@@a1s2d3f4\n")
    time.sleep(2)

    from nowdata_code.now_waiting import now_waiting
    driver = now_waiting(driver, date)
    return driver

# if __name__ == '__main__':
#     driver = Driver()
#     import datetime
#     dates = []
#     x = datetime.datetime(2020, 9, 4)
#     t = x + datetime.timedelta(days=1)
#     while t.strftime('%Y-%m-%d') != "2020-09-13":
#         dates.append(t.strftime('%Y-%m-%d'))
#         t = t + datetime.timedelta(days=1)
#     try:
#         for i in range(len(dates)):
#             date = dates[i]
#             now_waiting_main(driver, date, i)
#     except Exception as e:
#         print(e)
