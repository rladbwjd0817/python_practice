# 구조
#1. 라이브러리
#2. 클래스 생성
#3. 생성자 호출 및 변수 생성
#4. 초기설정
#5. 센서 값을 읽을 함수
#6. 메인 호출할 함수
#7. 콘솔 출력 + DB 저장

#1. 라이브러리
import time
# 라즈베리파이랑 센서랑 통신하는 도구
import spidev 
# 이 핀을 입력으로 쓸지 출력으로 쓸지 설정하고 제어
import RPi.GPIO as GPIO 
import adafruit_dht
## adafruit_dht 이건 뭘까? 
# -> DHT센서를 제어하는 라이브러리
# -> 온도, 습도 값을 읽어오는 기능 제공 
#  => 센서를 쉽게 쓰게 해주는 도구
import board
## board는 빵판을 뜻하나? 
# -> 라즈베리파이 핀을 이름으로 쓰게 해주는 모듈
# -> 핀 이름 매핑 도구


#2. 클래스 생성
class Temp_sensor :
  #3. 생성자 호출 및 변수 생성
  def __init__(self):
    
    #4. 초기설정
    self.dhtDevice = adafruit_dht.DHT22(board.D17, use_pulseio = False)
    # adafruit_dht.DHT22 -> DHT22 센서를 쓰겠다는 선언 aka.클래스 이름
    ## DHT22는 뭘까? -> 디지털
    ## board.D17은 GPIO 핀 번호인 것 같은데? -> YES!
    ## use_pulseio는 사용하는게 False라는 건가? 아님 센서 작동코드인가? 
    # -> 신호를 읽는 방식 선택 코드!
    # -> True : PulselO (하드웨어 방식)
    # -> False : 소프트웨어 방식 / 라즈베리파이에서는 보통 False를 씀!(충돌, 에러 방지)

    self.temp = 0 # 온도 데이터
    self.humidity = 0 # 습도 데이터
    self.spi = spidev.SpiDev() # 센서연결준비
    self.temp_Channel = 14
    self.times = time.time()
    self.spi.open(0, 0) # 버스 0, 디바이스 0
    self.spi.max_speed_hz = 100000 # 센서 연결 최대 속도는 10000hz

  #5. 온.습도 센서 값을 읽을 함수
  def readTemp(self) :
    ## 함수의 매개변수로 temp, humidity 들어가야하지 않을까? 안 들어 간다면 왜 안들어갈까?
    # -> self.dhtDevice 여기 안에 센서 정보가 다 들어있음

    # 온도 데이터 읽기
    # dhtDevice : 변수명
    # temperature, humidity : 라이브러리에서 제공되는 속성
    temp = self.dhtDevice.temperature
    humidity = self.dhtDevice.humidity
    
    """ temp = self.spi.xfer2([1, 8 + temp << 4, 0])
    humidity = self.spi.xfer2([1, 8 + humidity << 4, 0]) """ # 이건 SPI 방식이라 온.습도 센서방식에 맞지 X 

    # 10비트 숫자 완성(0 ~ 1023)
    #temp_data = ((temp[1] & 3) << 8 + temp[2])
    #humidity_data = ((humidity[1] & 3) << 8 + humidity[2]) => 이미 디지털이라 변환 필요 X

    # 저장된 데이터 전달
    return temp, humidity

  #6. 메인 호출 함수
  def runTemp(self, conn) :
    
    # 만약 온도의 값이 none이 아니고 습도의 값이 none이 아니라면
    if self.temp is not None and self.humidity is not None :
      # 콘솔에 온도, 습도 값 출력
      print(f"temp : {self.temp : .1f} 도, humidity : {self.humidity: .1f} %")
      ## 온도, 습도 값 뒤에 .1f 이건 단위 표시일까?
      ## 그렇다면 저기서 f는 float인가?

      #6. db 연결
      with conn.cursor() as cursor :
        sql = "INSERT INTO namuwiki.Temp_HUMIDITY(TEMP, HUMIDITY) VALUES (%s, %s)"
        # %s : 라이브러리가 안전하게 처리해주고, 여기에 나중에 값을 안전하게 끼워넣을게 표시!
        data = (self.temp, self.humidity)

        cursor.execute(sql, data)
      
    else :
      print("센서 값을 읽지 못했습니다.")

  #def runTemp(self, conn) :
    #self.temp, self.humidity = self.readTemp()
###-----------------------------------------------###
# 센서 보면 이거 먼저 생각하기!
# 디지털 센서인지, 아날로그 센서인지
# 디지털 -> 바로 읽기 (DHT22)
# 아날로그 -> SPI + 변환(MCP3008)

# 디지털 vs 아날로그 구분 기준
# -> 값이 어떻게 나오는지 구분
#   -> 디지털 : 딱 떨어진 값 / 아날로그 : 연속적인 전압
#   -> 핀 갯수로 구분

# -> 디지털 센서 : 보통 3 ~ 4개 핀, DATA 핀 1개
#   -> keyword : Digital output, One-wire, 12C /UART
#   -> GPIO에 바로 연결

# -> 아날로그 센서 : 출력이 전압 , ADC (MCP3008)
#   -> keyword : Analog output, Voltage output(0 ~ 3.3V)
