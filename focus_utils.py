from selenium.webdriver.common.by import By

def focus_list(driver):
    """음식점 리스트 포커싱"""
    driver.switch_to.parent_frame()
    iframe = driver.find_element(By.XPATH, '//*[@id="searchIframe"]')
    driver.switch_to.frame(iframe)

def focus_detail(driver):
    """음식점 상세 정보 포커싱"""
    driver.switch_to.parent_frame()
    iframe = driver.find_element(By.XPATH, '//*[@id="entryIframe"]')
    driver.switch_to.frame(iframe)
