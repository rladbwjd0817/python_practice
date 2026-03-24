# 구조
#1. 라이브러리
#2. 클래스 생성
#3. 초기설정 - 생성자 및 멤버변수 같이 초기화
# : GPIO, 핀 번호, 가장 건조 값, 수분 충분 값
#4. 펌프 실행 함수
#5. 메인에서 실행할 함수

#1. 라이브러리
import RPi.GPIO as GPIO # 물리적인 핀 제어
import time

#2. 클래스 생성
class water_pump : 

  # 생성자 및 멤버변수 같이 초기화
  def __init__(self):
    #3. 초기설정
    # BCM번호 방식 사용
    ## BCM 번호란? -> GPIO 칩 번호
    GPIO.setmode(GPIO.BCM) 
    self.AIA = 14 # 핀 번호  
    self.AIB = 5 # 핀 번호

    ## GPIO.IN : 이 핀은 데이터 읽어올거야!
    ## GPIO.OUT : 이 핀은 데이터 출력할거야!
    ## GPIO.setup : 핀 모드 설정(IN / OUT)
    ## GPIO.output : 핀에 신호 보내기(HIGH / LOW)

    # 이 핀은 출력용!
    GPIO.setup(self.AIA, GPIO.OUT)
    # AIA 초기값은 LOW 
    GPIO.output(self.AIA, GPIO.LOW) 
    GPIO.setup(self.AIB, GPIO.OUT) 
    # AIB 초기값은 LOW 
    GPIO.output(self.AIB, GPIO.LOW) 
    self.best_dry = 5 # 가장 건조 값
    self.best_wet = 66 # 수분 충분 값

  #4. 펌프 작동 함수
  def pumpOn(self, sec) :
    # 펌프 켜기
    # GPIO 신호 보내기
    # 역방향(물 빨아들이기) -> 호스로 밀어내기
    GPIO.output(self.AIA, GPIO.LOW)
    GPIO.output(self.AIB, GPIO.HIGH)

    # 몇 초 동안 기다렸다가
    time.sleep(sec)
    # 펌프 끄기
    GPIO.output(self.AIA, GPIO.LOW)
    GPIO.output(self.AIB, GPIO.LOW)

    # 밑의 두 코드도 펌프를 끄는 코드이나 HIGH/HIGH는 전류가 양쪽에서 막혀있는 상태라 미세하게 전력 소비가 있어서 LOW/LOW로 쓰는 것이 바람직함.
    #PIO.output(self.AIB, GPIO.HIGH)
    #GPIO.output(self.AIB, GPIO.HIGH)

  #5. 메인에서 실행할 함수
  def runPump(self, moisture_value) :
    # 만약 펌프가 실행되려면?
   if moisture_value <= self.best_dry : 
      self.pumpOn(sec=10) 
