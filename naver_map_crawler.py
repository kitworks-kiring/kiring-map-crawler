import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from colorama import Fore, Style

from geocoding import KakaoMapGeocoding

# 카카오 맵 geocoder 인스턴스 생성
geocoder = KakaoMapGeocoding()

# 크롬 드라이버 설정
service = Service(ChromeDriverManager().install())
options = Options()

# 네이버 지도 URL (keyword: 당산역 음식점)
KEYWORD = "%EB%8B%B9%EC%82%B0%EC%97%AD%20%EC%9D%8C%EC%8B%9D%EC%A0%90?"
URL = f"http://map.naver.com/p/search/{KEYWORD}?c=15.00,0,0,0,dh"

# 네이버 지도 페이지 열기
driver = webdriver.Chrome(service=service, options=options)
driver.get(url=URL)

# 페이지 로딩 대기
time.sleep(5)


def focus_list():
	"""음식점 리스트 포커싱"""
	driver.switch_to.parent_frame()
	iframe = driver.find_element(By.XPATH,'//*[@id="searchIframe"]')
	driver.switch_to.frame(iframe)

def focus_detail():
	"""음식점 상세 정보 포커싱"""
	driver.switch_to.parent_frame()
	iframe = driver.find_element(By.XPATH,'//*[@id="entryIframe"]')
	driver.switch_to.frame(iframe)

while True:
	focus_list()

	# 다음페이지 버튼 활성화여부 체크
	is_next_btn_disabled = driver.find_element(By.XPATH, '//div[@id="app-root"]/div/div[2]/div[2]/a[7]').get_attribute('aria-disabled')
	if is_next_btn_disabled == 'true':
		print("마지막 페이지입니다.")
		break

	# 스크롤을 끝까지 내려 현재 페이지 모든 데이터 불러오기
	# scroll_element = driver.find_element(By.ID, "_pcmap_list_scroll_container")
	# last_height = driver.execute_script("return arguments[0].scrollHeight", scroll_element)

	# while True:
	# 	# 600px씩 스크롤 내리고 데이터 로딩 대기
	# 	driver.execute_script("arguments[0].scrollTop += 600;", scroll_element)
	# 	time.sleep(1)

	# 	# 새로운 높이 계산
	# 	new_height = driver.execute_script("return arguments[0].scrollHeight", scroll_element)

	# 	# 스크롤이 더 이상 늘어나지 않으면 루프 종료
	# 	if (new_height == last_height):
	# 		break

	# 	last_height = new_height

  # 현재 페이지 번호 가져오기
	current_page = driver.find_element(By.XPATH, '//a[contains(@class, "mBN2s qxokY")]').text
	print(f"현재 페이지: {current_page}")

	# 현재 페이지의 음식점 리스트 가져오기 (첫 페이지일 경우 앞의 2개 광고 제외)
	if current_page == '1':
		elements = driver.find_elements(By.XPATH, '//*[@id="_pcmap_list_scroll_container"]//li')[2:]
	else:
		elements = driver.find_elements(By.XPATH, '//*[@id="_pcmap_list_scroll_container"]//li')

	print(f"{Fore.MAGENTA}현재 {current_page} 페이지 / 총 {len(elements)}개의 음식점을 찾았습니다.{Style.RESET_ALL}\n")

	for index, element in enumerate(elements, start=1):
		name = ''
		category = ''
		address = ''
		lat = ''
		lng = ''
		phone_number = ''
		menu_1 = ''
		menu_2 = ''
		menu_3 = ''

		img_url = ''

		# 리스트에서 음식점 이름 클릭
		focus_list()
		element.find_element(By.CLASS_NAME, 'CHC5F').find_element(By.XPATH, ".//div/a/span").click()
		time.sleep(2)

		focus_detail()
		time.sleep(3)

		# 음식점 이름 element
		title_element = driver.find_element(By.CLASS_NAME, 'zD5Nm.undefined')
		name = title_element.find_element(By.XPATH, ".//div/div/span[1]").text
		category = title_element.find_element(By.XPATH, ".//div/div/span[2]").text

		# 음식점 정보 element
		store_element = driver.find_element(By.XPATH, '//div[@id="app-root"]/div/div/div/div[5]/div[@data-nclicks-area-code="btp" and (not(@class)]')
		# store_element = driver.find_element(By.XPATH, '//div[contains(@style, "min-height: calc(-97px + 100vh)")]')

		address = store_element.find_element(By.CLASS_NAME, 'LDgIH').text
		lat, lng = geocoder.get_coordinates(address)
		phone_number = store_element.find_element(By.CLASS_NAME, 'xlx7Q').text

  		# 스크롤을 끝까지 내려 하단 데이터까지 데이터 불러오기
		detail_last_height = driver.execute_script("return document.body.scrollHeight")
		current_height = 0
		while current_height < detail_last_height:
			current_height += 600  # 600px씩 증가
			driver.execute_script(f"window.scrollTo(0, {current_height});")
			time.sleep(1)

			new_height = driver.execute_script("return document.body.scrollHeight")
			if new_height > detail_last_height:
				detail_last_height = new_height

		focus_detail()

		# 방문자 리뷰 element
		review_elements = driver.find_element(By.XPATH, '//div[@id="app-root"]/div/div/div/div[6]/div/div[@data-nclicks-area-code="rrr" and @class="place_section k1QQ5"]')

		review_elements.find_element(By.XPATH, '//a[@class="fvwqf"]').click()
		time.sleep(2)
		review_detail_elements = driver.find_element(By.XPATH, '//[@id="app-root"]/div/div/div/div[6]/div[3]/div[3 and @class="place_section k1QQ5"]')

		for i in range(1, 4):
			try:
				menu_element = review_detail_elements.find_element(By.XPATH, f'.//div[@class="flicking-camera"]/span[{i} and @class="Me4yK"]/a/span')
				if i == 1:
					menu_1 = menu_element.text
				elif i == 2:
					menu_2 = menu_element.text
				elif i == 3:
					menu_3 = menu_element.text
			except Exception as e:
				print(f"메뉴 {i}를 찾을 수 없습니다: {e}")
			finally:
				print(f"{menu_1}, {menu_2}, {menu_3}")

