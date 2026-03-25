# import RPi.GPIO as GPIO
# import time


# class waterPump : 
#   def __init__(self):
#     #3. 초기설정
#     # BCM번호 방식 사용
#     ## BCM 번호란? -> GPIO 칩 번호
#     GPIO.setmode(GPIO.BCM) 
#     self.AIA = 6 # 핀 번호  
#     self.AIB = 5 # 핀 번호

#     ## GPIO.IN : 이 핀은 데이터 읽어올거야!
#     ## GPIO.OUT : 이 핀은 데이터 출력할거야!
#     ## GPIO.setup : 핀 모드 설정(IN / OUT)
#     ## GPIO.output : 핀에 신호 보내기(HIGH / LOW)

#     # 이 핀은 출력용!
#     GPIO.setup(self.AIA, GPIO.OUT)
#     # AIA 초기값은 LOW 
#     GPIO.output(self.AIA, GPIO.LOW) 
#     GPIO.setup(self.AIB, GPIO.OUT) 
#     # AIB 초기값은 LOW 
#     GPIO.output(self.AIB, GPIO.LOW) 
#     self.best_dry = 5 # 가장 건조 값
#     self.best_wet = 66 # 수분 충분 값

#   #4. 펌프 작동 함수
#   def pumpOn(self, sec) :
#     # 펌프 켜기
#     # GPIO 신호 보내기
#     # 역방향(물 빨아들이기) -> 호스로 밀어내기
#     GPIO.output(self.AIA, GPIO.LOW)
#     GPIO.output(self.AIB, GPIO.HIGH)

#     # 몇 초 동안 기다렸다가
#     time.sleep(sec)
#     # 펌프 끄기
#     GPIO.output(self.AIA, GPIO.LOW)
#     GPIO.output(self.AIB, GPIO.LOW)

#       # 밑의 두 코드도 펌프를 끄는 코드이나 HIGH/HIGH는 전류가 양쪽에서 막혀있는 상태라 미세하게 전력 소비가 있어서 LOW/LOW로 쓰는 것이 바람직함.
#       #PIO.output(self.AIB, GPIO.HIGH)
#       #GPIO.output(self.AIB, GPIO.HIGH)

#   #5. 메인에서 실행할 함수
#   def runPump(self, moisture_value) :
#   # 만약 펌프가 실행되려면?
#     if moisture_value <= self.best_dry : 
#       self.pumpOn(sec = 10) 
  
#   def cleanuup(self) :
#     GPIO.output(self.AIA, GPIO.LOW)
#     GPIO.output(self.AIB, GPIO.LOW)
  
#   #test
# if __name__ == "__name__" :
#   pump = waterPump()
#   pump.pumpOn(sec = 3)
#   pump.cleanup()

import RPi.GPIO as GPIO
import time


class waterPump:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        self.AIA = 14
        self.AIB = 15

        GPIO.setup(self.AIA, GPIO.OUT)
        GPIO.output(self.AIA, GPIO.LOW)
        GPIO.setup(self.AIB, GPIO.OUT)
        GPIO.output(self.AIB, GPIO.LOW)

        self.best_dry = 5
        self.best_wet = 66

    def pumpOn(self, sec):
        GPIO.output(self.AIA, GPIO.LOW)
        GPIO.output(self.AIB, GPIO.HIGH)
        time.sleep(sec)
        GPIO.output(self.AIA, GPIO.LOW)
        GPIO.output(self.AIB, GPIO.LOW)

    def runPump(self, moisture_value):
        if moisture_value <= self.best_dry:
            self.pumpOn(sec=10)

    def cleanup(self):  # ← 오타 수정
        GPIO.output(self.AIA, GPIO.LOW)
        GPIO.output(self.AIB, GPIO.LOW)
        GPIO.cleanup()  # ← GPIO 리소스 해제 추가 권장


if __name__ == "__main__":  # ← "__name__" 에서 "__main__" 으로 수정
    pump = waterPump()
    pump.pumpOn(sec=5)
    pump.cleanup()
