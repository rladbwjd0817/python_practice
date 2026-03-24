#구조
#1. 라이브러리 import
#2. 클래스생성
#3. 초기 설정 - 생성자 및 멤버변수 같이 초기화
# : 수분토양변수, spidev, time, GPIO가 몇 번 핀에 꽂혔는지 저장하는 channel변수
#4. 값을 읽는 함수
#5. 우리가 사용할 함수 생성 - db연결
#6. 콘솔 출력 + DB저장 - 메인

#1. 라이브러리
import spidev
import time # 시간자체는 main에서 통제해서 없어도 됨!
import RPi.GPIO as GPIO

#2. 클래스
class soil_moisture : 
  # 생성자 및 멤버변수 초기화
  def __init__(self):
    #3. 초기설정
    # 토양수분 데이터
    self.moisture = 0
    # 센서연결준비
    self.spi = spidev.SpiDev()
    # 시간 설정
    self.time = time.time()
    # GPIO가 몇 번 핀에 꽂혔는지 저장하는 channel변수 생성
    self.moisture_channel = 7
    # 버스, 디바이스 포트 연결
    self.spi.open(0, 0)
    # 센서 연결 최대속도 설정
    self.spi.max_speedc_hz = 100000

  #4. 값을 읽는 함수 생성 -> 값을 읽은 raw값(0 ~ 1023 숫자)
  def readChannel(self) : 
    # 수분토양 채널에 8을 더하고 4비트 왼쪽으로 밀어낸 데이터를 val에 저장
    val = self.spi.xfer([1, (8 + self.moisture_channel) << 4, 0])
    # data는 상위 2비트를 8간 왼쪽으로 밀고 하위 8비트 붙임 => 10비트 숫자 완성 (0 ~ 1023) , 즉 data는 0 ~ 1023의 숫자가 저장
    data = ((val[1] & 3) << 8) + val[2]
    # data 리턴
    return data
  
  #5. 토양 수분 값을 저장할 data
  # 0~ 1023 value가 들어오고, 1023이 수분함량 최솟값
  ## 위에 readChannel이랑 뭐가 달라? 실질적인 값인가? -> readChannel은 MCP3008이 읽은 raw값, convertPercent는 그 숫자를 %로 변환하는 역할
  def convertPercent(self, data) :
    return 100.0 - round(((data *100) / float(1023)) ,1)
  
  #6. 메인에서 실행할 함수 생성 - db연결
  def readMoisture(self, conn):
    # 값을 읽는 함수 호출하여 변수에 저장
    val = self.readChannel() # <= raw값 저장
    moisture_value = self.convertPercent (val) # <= raw값 저장된 val을 %로 변환하여 moisture_value 에 저장

    # 만약 토양수분의 값이 정상이면 
    # raw 값으로 비교하기!
    if val != 0 :
      # f: 문자열 안에 변수 끼워넣기
      print(f"토양 수분 : {moisture_value}%")

      # db도 연결
      with conn.cursor() as cursor :
        sql = "INSERT INTO numuwiki.SOIL_MOISTURE (SOIL_MOISTURE_VALUE) VALUES (%s)"
        # sql을 실제로 실행
        cursor.execute(sql, (moisture_value, ))