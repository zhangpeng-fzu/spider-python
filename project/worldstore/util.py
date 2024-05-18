import time


def click(driver, by, condition):
    loop_count = 0
    while loop_count < 10:
        loop_count += 1
        try:
            driver.find_element(by, condition).click()
            if loop_count > 5:
                print(f"在尝试点击了{loop_count}次之后，点击成功。")
            break
        except Exception as e:
            print(e)
            time.sleep(1)
    return False
