# 🗺️ 네이버지도 음식점 크롤러

![네이버맵 크롤링 화면 캡쳐](https://github.com/user-attachments/assets/84d77161-03ef-4fda-8bc5-f1d8308dcab9)

**[KIRING 프로젝트](https://github.com/kitworks-kiring/kiring-frontend)** 의 일환으로, **네이버지도에서 음식점 정보를 자동으로 수집**하고,<br />
**데이터를 정제 및 표준화**하여 **엑셀 파일로 저장**하는 **Python 기반 크롤러**입니다.

<br /><br />

## ⚙️ 주요 기능 및 설계 의도

### 1. 🤖 자동화된 네이버지도 크롤링

- **Selenium**을 활용하여 네이버지도 웹페이지를 직접 제어합니다.

- 네이버지도의 iframe 구조를 분석하여, 음식점 리스트와 상세 정보를 안정적으로 추출합니다.

- 동적 로딩/스크롤 등 실제 사용자 환경을 최대한 모방하여 데이터 누락없이 수집합니다.

<br />

### 2. 📝 음식점 상세 정보 수집

- 음식점의 **이름, 카테고리, 주소, 전화번호, 대표 이미지, 메뉴** 등 다양한 정보를 수집합니다.

- 상세 페이지 내 스크롤 및 버튼 클릭 자동화를 통해 추가 정보를 안정적으로 확보합니다.

<br />

### 3. 📍 좌표 변환 (Geocoding)

- 주소 정보를 카카오 지도 API와 연동하여 **위도, 경도**로 변환합니다.

- 환경변수(.env)로 API Key를 관리하여 보안성을 높였습니다.

<br />

### 4. 📊 엑셀 파일 저장 및 데이터 관리

- pandas와 openpyxl을 활용해 데이터프레임을 **엑셀 파일(.xlsx)로 저장**합니다.

- 데이터 정제 및 예외처리를 통해 실제 활용이 가능한 데이터셋을 생성합니다.

<br /><br />

## 🗂️ 폴더 및 코드 구조

```bash
📦kiring-map-crawler
 ┣ 📜.env
 ┣ 📜.gitignore
 ┣ 📜geocoding.py           # 카카오 지도 API 연동 및 좌표 변환
 ┣ 📜naver_map_crawler.py   # 메인 크롤링 로직
 ┣ 📜scroll_utils.py        # 자동 스크롤 유틸리티
 ┗ 📜focus_utils.py         # iframe 포커싱 유틸리티 (리스트/상세)
```

<br /><br />

## 🧩 주요 코드 설명

### 🧾 naver_map_crawler.py

- 크롤러의 메인 엔트리포인트입니다.

- Selenium으로 네이버지도 페이지를 열고, 음식점 리스트/상세정보를 반복적으로 수집합니다.

- 각 요소 별 예외 처리 및 데이터 정제 로직이 포함되어 있습니다.

<br />

### 🧭 geocoding.py

- 카카오 지도 REST API를 활용한 주소 → 좌표(위도, 경도) 변환을 담당합니다.

- 환경변수에서 API를 자동으로 읽어와 보안성을 확보합니다.

<br />

### 🖱️ scroll_utils.py

- 네이버지도와 같이 동적으로 로딩되는 페이지에서 스크롤 자동화를 지원합니다.

- 리스트/상세페이지 등 다양한 상황에 맞는 스크롤 함수가 제공됩니다.

<br />

### 🔎 focus_utils.py

- 네이버지도 내 음식점 리스트/상세 정보 iframe 포커스 스위칭을 담당합니다.

- 크롤링 코드에서 iframe 전환이 필요한 구간에 import하여 사용합니다.

<br /><br />

## 🚀 실행 방법

1. **필요 패키지 설치**

   ```bash
   pip install -r requirements.txt
   ```

2. **카카오 REST API 키 발급 후 .env 파일에 등록**

   ```bash
   KAKAO_REST_API_KEY=발급받은_키
   ```

3. **스크립트 실행**

   ```bash
   python naver_map_crawler.py
   ```

4. **엑셀 파일 확인**

   <img src="https://github.com/user-attachments/assets/ab237722-84b4-4f99-b3cf-6aefd31dc7af" height="500" alt="엑셀 출력 결과" />

   - 실행 폴더 (또는 별도 지정 경로)에 결과 파일이 생성됩니다.

<br />

---

<div align="center">via. <a href="https://github.com/hansololiviakim" target="_blank">@hansololiviakim</a>　|　Last Updated. 2025-06-17
</div>
