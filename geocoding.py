import os
import requests
from dotenv import load_dotenv

load_dotenv()

class KakaoMapGeocoding:
  def __init__(self):
    self.api_key = os.getenv('KAKAO_REST_API_KEY')

    if not self.api_key:
      raise ValueError("KAKAO_REST_API_KEY 환경변수를 찾을 수 없습니다.")

    self.base_url = "https://dapi.kakao.com/v2/local/search/address.json"

  def get_coordinates(self, address):
    headers = {"Authorization": f"KakaoAK {self.api_key}"}
    params = {"query": address}

    try:
      response = requests.get(self.base_url, headers=headers, params=params)
      if response.status_code == 200:
        data = response.json()
        if data['documents']:
          lat = data['documents'][0]['y']
          lng = data['documents'][0]['x']
          return lat, lng
      else:
        print(f"API 요청 실패: {response.status_code}")
    except Exception as e:
      print(f"Geocoding 오류: {e}")

    return None, None
