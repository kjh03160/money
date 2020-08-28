from selenium_class import Driver
import datetime
import pandas as pd

def albam(driver, date):

    url = "https://web.albamapp.com/today"
    driver.get_url(url)

    navs = driver.find_by_css("ul.nav")
    lis = driver.find_by_link_with_obj(navs, "근무기록")
    driver.click(lis)


    date_pickers = driver.find_all_by_css("div.react-datepicker__input-container > button")

    start_date = list(map(int, (date_pickers[0].text.split()[0].split("-"))))
    start_date = datetime.datetime(start_date[0], start_date[1], start_date[2])

    end_date = list(map(int, (date_pickers[1].text.split()[0].split("-"))))
    end_date = datetime.datetime(end_date[0], end_date[1], end_date[2])

    now_date = list(map(int, date.split("-")))
    now = datetime.datetime(now_date[0], now_date[1], now_date[2])

    if start_date != now or end_date != now:
        for i in range(2):
            driver.click(date_pickers[i])
            month = int(driver.find_by_css("div.react-datepicker__current-month").text.split()[0][:-1])
            year = int(driver.find_by_css("div.react-datepicker__current-month").text.split()[1])

            if now_date[1] < month:
                prev = driver.find_by_css("button.react-datepicker__navigation--previous")
                count = month - now_date[1]
                if now_date[0] < year:
                    count += 12
                for i in range(count):
                    driver.click(prev)

            day = driver.find_by_css("div.react-datepicker__month")
            day = driver.find_by_css_with_obj(day, "div[aria-label=day-{day}]".format(day = now_date[2]))
            driver.click(day)

    fitting = driver.find_by_css("div.resize-grid-btn > button:nth-child(2)")
    driver.click(fitting)


    result = []
    while True:
        container = driver.find_by_css("div.ag-body-container")
        if len(container.text.strip()) == 0:
            return driver

        rows = driver.find_all_by_css_with_obj(container, "div.ag-row-position-absolute")
        for i in rows:
            username = driver.find_by_css_with_obj(i, "div[col-id=username]").text
            fullWorkTime = driver.find_by_css_with_obj(i, "div[col-id=fullWorkTime]").text
            totalTime = driver.find_by_css_with_obj(i, "div[col-id=totalTime]").text
            start_time = driver.find_by_css_with_obj(i, "div[col-id=\'0\']")
            start_time = driver.find_by_css_with_obj(start_time, "div.schedule-time-label div:nth-child(2)").text.strip("()")
            end_time = driver.find_by_css_with_obj(i, "div[col-id=\'1\']")
            end_time = driver.find_by_css_with_obj(end_time, "div.schedule-time-label div:nth-child(2)").text.strip("()")


            result.append([username, start_time, end_time, fullWorkTime, totalTime])
        next_btn = driver.find_by_css("button[ref=btNext]")
        if next_btn.get_attribute("disabled"):
            break
        driver.click(next_btn)


    labels = ['이름', '출근시간', '퇴근시간', '총근무시간', '근무인정시간']
    df = pd.DataFrame(result, columns=labels)
    df.to_csv('data/albam/' + date + '.csv', index=False, mode='w', encoding='utf-8-sig')

    return driver

if __name__ == '__main__':
    albam(Driver(), '2020-08-25')
