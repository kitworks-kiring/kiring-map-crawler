# scroll_utils.py
import time
from selenium.webdriver.common.by import By

class ScrollManager:
    def __init__(self, driver):
      self.driver = driver

    def scroll_page_gradually(self, scroll_step=600, delay=1):
      """페이지 전체를 점진적으로 스크롤"""
      detail_last_height = self.driver.execute_script("return document.body.scrollHeight")
      current_height = 0

      while current_height < detail_last_height:
        current_height += scroll_step
        self.driver.execute_script(f"window.scrollTo(0, {current_height});")
        time.sleep(delay)

        new_height = self.driver.execute_script("return document.body.scrollHeight")
        if new_height > detail_last_height:
          detail_last_height = new_height

    def scroll_element_gradually(self, element_id, scroll_step=600, delay=1):
      """특정 요소를 점진적으로 스크롤"""
      try:
        scroll_element = self.driver.find_element(By.ID, element_id)
        last_height = self.driver.execute_script("return arguments[0].scrollHeight", scroll_element)

        while True:
          self.driver.execute_script(f"arguments[0].scrollTop += {scroll_step};", scroll_element)
          time.sleep(delay)

          new_height = self.driver.execute_script("return arguments[0].scrollHeight", scroll_element)
          if new_height == last_height:
            break
          last_height = new_height
        print(f"요소 스크롤 완료: {element_id}")
      except Exception as e:
        print(f"요소 스크롤 오류: {e}")

    def scroll_to_position(self, position):
      """특정 위치로 스크롤"""
      if isinstance(position, str):
        if position == "top":
          self.driver.execute_script("window.scrollTo(0, 0);")
        elif position == "bottom":
          self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        elif position == "middle":
          self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 2);")
      else:
        self.driver.execute_script(f"window.scrollTo(0, {position});")
      time.sleep(1)

    def scroll_to_element(self, element):
      """특정 요소까지 스크롤"""
      self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
      time.sleep(2)
