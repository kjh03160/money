from albam_code.albam import albam
import time

def albam_main(driver, date, i):
    if i == 0:
        url = "https://web.albamapp.com/today"
        driver.get_url(url)
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

    driver = albam(driver, date)
    return driver