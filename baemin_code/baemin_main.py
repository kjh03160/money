import datetime
import time

def baemin_main(driver, date, i):
    driver.get_url("https://ceo.baemin.com/self-service/orders/history")
    if driver.driver.title == "ERROR: The request could not be satisfied":
        return print("요청이 너무 많아 차단되었습니다. 잠시 후 다시 시도해주세요")
    if i == 0:
        id = driver.find_by_id("id")
        id.send_keys("")

        pw = driver.find_by_id("pw")
        pw.send_keys("!!")

        login = driver.find_by_id("btnLogin")
        driver.click(login)

    time.sleep(2)

    from baemin_code.baemin import baemin
    from baemin_code.to_csv import to_csv
    from baemin_code.baemin_7 import baemin_7

    rq_date = list(map(int, date.split("-")))
    rq = datetime.datetime(rq_date[0], rq_date[1], rq_date[2])
    now = datetime.datetime.now()

    if (now - rq).days > 6:
        driver = baemin(driver, date)
        try:
            to_csv(date)
        except FileNotFoundError as err:
            print(err)
    else:
        driver = baemin_7(driver, date)
    if not driver:
        return print("요청이 너무 많아 차단되었습니다. 잠시 후 다시 시도해주세요")

    return driver
