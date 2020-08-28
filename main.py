from selenium_class import Driver
import time
from urllib import parse

def main(dates):
    driver = Driver()
    driver.driver.implicitly_wait(10)
    #
    # while len(date) != len("2020-00-00") or date[4] != "-" or date[7] != "-":
    #     print("날짜 형식을 다시 확인해주세요!")
    #     date = input("날짜를 입력해주세요(형식 : 2020-00-00) : ")
    for i in range(len(dates)):
        date = dates[i]
        driver.get_url("https://ceo.baemin.com/self-service/orders/history")

        if i == 0:
            id = driver.find_by_id("id")
            id.send_keys("sudaje1")

            pw = driver.find_by_id("pw")
            pw.send_keys("sujung4710!!")

            login = driver.find_by_id("btnLogin")
            driver.click(login)

        time.sleep(2)

        from baemin import baemin
        from result_df import to_csv
        driver = baemin(driver, date)
        if not driver:
            return print("요청이 너무 많아 차단되었습니다. 잠시 후 다시 시도해주세요")
        try:
            to_csv(date)
        except FileNotFoundError:
            pass


        # from graph import graph
        # graph()
        if i  == 0:
            login_url = "https://ceo.nowwaiting.co/order_sales/history"
            driver.get_url(login_url)

            id_box = driver.find_by_id("email")
            id_box.send_keys("2753034@naver.com")

            pw_box = driver.find_by_id("password")
            pw_box.send_keys("@@a1s2d3f4\n")
        time.sleep(2)

        from now_waiting import now_waiting
        driver = now_waiting(driver, date)


        time.sleep(1)

        url = "https://web.albamapp.com/today"
        driver.get_url(url)
        if i == 0:
            id_box = driver.find_by_name("account")
            id_box.send_keys("01068863034")

            pw_box = driver.find_by_name("userPassword")
            pw_box.send_keys("@@a1s2d3f4")

            login_btn = driver.find_by_css("button.LoginButton")
            driver.click(login_btn)

        time.sleep(2)

        navs = driver.find_by_css("ul.nav")
        lis = driver.find_by_link_with_obj(navs, "근무기록")
        driver.click(lis)

        from albam import albam
        driver = albam(driver, date)
        print(date, "수집 완료")

    driver.close()



if __name__ == '__main__':
    # date = input("날짜를 입력해주세요(형식 : 2020-00-00) : ")
    date = ['2020-08-23',
            '2020-08-24', '2020-08-25', '2020-08-26', '2020-08-27']
    main(date)