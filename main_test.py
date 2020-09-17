from selenium_class import Driver
from baemin_code.baemin_main import baemin_main
from nowdata_code.now_waiting_main import now_waiting_main
from albam_code.albam_main import albam_main
from statistic_code import albam_statistic
import time

def main(dates):
    driver = Driver()
    driver.driver.implicitly_wait(10)
    for i in range(len(dates)):
        date = dates[i]

        # 배민 수집
        try:
            driver = baemin_main(driver, date, i)
            if driver is None:
                raise Exception
        except Exception as err:
            print(err)
            driver.close()
            return date

        # 나우 웨이팅 수집
        driver = now_waiting_main(driver, date, i)

        time.sleep(1)

        driver = albam_main(driver, date, i)
        print(date, "수집 완료")

    driver.close()





if __name__ == '__main__':
    # date = input("날짜를 입력해주세요(형식 : 2020-00-00) : ")
    # JSONDecodeError
    import datetime
    date = []
    x = datetime.datetime(2020, 8, 31)
    t = x + datetime.timedelta(days=1)
    while t.strftime('%Y-%m-%d') != "2020-09-05":
        date.append(t.strftime('%Y-%m-%d'))
        t = t + datetime.timedelta(days=1)
    try:
        main(date)
    except Exception as e:
        print(e)
