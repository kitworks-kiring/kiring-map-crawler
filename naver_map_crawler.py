import time
import pandas as pd
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from colorama import Fore, Style

from geocoding import KakaoMapGeocoding
from scroll_utils import ScrollManager
from focus_utils import focus_list, focus_detail

# 드라이버 설정
geocoder = KakaoMapGeocoding()
service = Service(ChromeDriverManager().install())
options = Options()
driver = webdriver.Chrome(service=service, options=options)

# 스크롤 매니저 초기화
scroll_manager = ScrollManager(driver)

# 데이터 저장용 리스트
restaurant_data = []

# 네이버 지도 URL (keyword: 당산역 음식점)
KEYWORD = "%EB%8B%B9%EC%82%B0%EC%97%AD%20%EC%9D%8C%EC%8B%9D%EC%A0%90?"
URL = f"http://map.naver.com/p/search/{KEYWORD}?c=14.00,0,0,0,dh"

# 네이버 지도 페이지 열기
driver.get(url=URL)
time.sleep(5)

while True:
	focus_list(driver)

	# 현재 페이지 번호 가져오기 (먼저 가져와서 체크)
	current_page = driver.find_element(By.XPATH, '//a[contains(@class, "mBN2s qxokY")]').text

	# 다음페이지 버튼 활성화여부 체크
	is_next_btn_disabled = driver.find_element(By.XPATH, '//div[@id="app-root"]/div/div[2]/div[2]/a[7]').get_attribute('aria-disabled')
	if is_next_btn_disabled == 'true':
		print("마지막 페이지입니다.")
		break

	# 스크롤을 끝까지 내려 현재 페이지 모든 데이터 불러오기
	scroll_manager.scroll_element_gradually(element_id="_pcmap_list_scroll_container", scroll_step=600, delay=1)
	scroll_manager.scroll_to_position("top")

	# 현재 페이지 번호 가져오기
	current_page = driver.find_element(By.XPATH, '//a[contains(@class, "mBN2s qxokY")]').text

	# 현재 페이지의 음식점 리스트 가져오기
	if current_page == '1':
		elements = driver.find_elements(By.XPATH, '//*[@id="_pcmap_list_scroll_container"]//li')[2:]
	else:
		elements = driver.find_elements(By.XPATH, '//*[@id="_pcmap_list_scroll_container"]//li')

	print(f"{Fore.CYAN}현재 {current_page} 페이지 / 총 {len(elements)}개의 음식점을 찾았습니다.{Style.RESET_ALL}\n")

	for index, element in enumerate(elements, start=1):
		try:
			name = ''
			category = ''
			address = ''
			lat = ''
			lng = ''
			phone_number = ''
			menus = []
			img_url = ''

			# 리스트에서 음식점 이름 클릭
			focus_list(driver)
			element.find_element(By.CLASS_NAME, 'CHC5F').find_element(By.XPATH, ".//div/a/span").click()
			time.sleep(2)

			focus_detail(driver)
			time.sleep(3)

			# 음식점 대표 이미지
			try:
				image_element = driver.find_element(By.XPATH, '//img[@id="ibu_1"]')
				img_url = image_element.get_attribute('src')
			except:
				img_url = ""

			# 음식점 이름 element
			try:
				title_element = driver.find_element(By.CSS_SELECTOR, '.zD5Nm')
				name = title_element.find_element(By.XPATH, ".//div/div/span[1]").text
				category = title_element.find_element(By.XPATH, ".//div/div/span[2]").text
			except:
				name = "이름 없음"
				category = "카테고리 없음"

			# 음식점 정보 element
			try:
				store_element = driver.find_element(By.XPATH, '//div[@id="app-root"]/div/div/div/div[5]/div[@data-nclicks-area-code="btp"]')
				address = store_element.find_element(By.CLASS_NAME, 'LDgIH').text
				lat, lng = geocoder.get_coordinates(address)

				try:
					phone_number = store_element.find_element(By.CLASS_NAME, 'xlx7Q').text
				except:
					phone_number = ""
			except:
				address = ""
				lat, lng = None, None

			# 스크롤을 끝까지 내려 하단 데이터까지 데이터 불러오기
			scroll_manager.scroll_page_gradually()
			scroll_manager.scroll_to_position("top")

			focus_detail(driver)

			# 방문자 리뷰 element (리뷰가 있으면 메뉴 크롤링, 없으면 빈 리스트)
			try:
				review_more_btn = driver.find_element(By.XPATH, './/a[@class="fvwqf" and contains(@href, "review/visitor")]')
				driver.execute_script("arguments[0].click();", review_more_btn)
				time.sleep(3)

				# 방문자 리뷰 태그 리스트 element
				review_detail_elements = driver.find_element(By.XPATH, '//div[@id="_tag_filters"]')
				menu_index = 2

				while True:
					try:
						menu = review_detail_elements.find_element(By.XPATH, f'.//div/div[1]/div/div/div/div/span[{menu_index}]/a/span[1]').text
						if menu:
							menus.append(menu)
							menu_index += 1
						else:
							break
					except:
							break
			except:
				pass

			# 데이터 딕셔너리 생성
			restaurant_info = {
				'번호': len(restaurant_data) + 1,
				'이름': name,
				'카테고리': category,
				'주소': address,
				'위도': lat if lat else '',
				'경도': lng if lng else '',
				'전화번호': phone_number,
				'메뉴': ', '.join(menus) if menus else '',
				'이미지URL': img_url,
				'페이지': current_page,
				'수집일시': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
			}

			# 리스트에 추가
			restaurant_data.append(restaurant_info)

			print(f"{index}. {name} ({category}) - 데이터 수집 완료")

		except Exception as e:
			print(f"{index}. 오류 발생: {e}")
			continue

	# 다음 페이지로 이동
	focus_list(driver)
	if is_next_btn_disabled == 'false':
		driver.find_element(By.XPATH, '//div[@id="app-root"]/div/div[2]/div[2]/a[7]').click()
		time.sleep(3)

# 크롤링 완료 후 엑셀 파일로 저장
try:
	if restaurant_data:
		# DataFrame 생성
		df = pd.DataFrame(restaurant_data)

		# 파일명 생성 (현재 날짜시간 포함)
		filename = f"당산역_음식점_크롤링_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"

		# 엑셀 파일로 저장
		df.to_excel(filename, index=False, engine='openpyxl')

		print(f"\n{Fore.GREEN}크롤링 완료!{Style.RESET_ALL}")
		print(f"총 {len(restaurant_data)}개의 음식점 데이터를 수집했습니다.")
		print(f"파일명: {filename}")

		# 데이터 미리보기
		print(f"\n{Fore.YELLOW}데이터 미리보기:{Style.RESET_ALL}")
		print(df.head())

	else:
		print("수집된 데이터가 없습니다.")

except Exception as e:
	print(f"엑셀 저장 오류: {e}")

finally:
	driver.quit()
