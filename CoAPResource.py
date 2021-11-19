#-*-coding: utf-8-*-
from coapthon.resources.resource import Resource
import threading
import logging as logger
import time
import Adafruit_DHT
import RPi.GPIO as GPIO

#온/습도센서.
class HumidityResource(Resource) :
    def __init__(self, name="HumidityResource", coap_server=None) :
        super(HumidityResource, self).__init__(name, coap_server, visible=True, observable=True, allow_children=False)
        self.payload = ""
        self.period = 5

        #센서와 GPIO PIN 설정.
        self.sensor = Adafruit_DHT.DHT11
        GPIO.setmode(GPIO.BCM)        #GPIO핀 번호를 읽는 방법 설정 합니다.
        self.sensor_pin = 14             #온습도센서 핀번호 저장.

        h, t = Adafruit_DHT.read_retry(self.sensor, self.sensor_pin)  #습도와 온도를 읽어옵니다. (전역변수 사용)
        # Adafruit_DHT는 임포트 하여 갖고 오기 때문에 자동으로 전역변수처럼 사용할 수 있습니다 .

        self.payload = "%s/%s"%(h,t) # "(습도)/(온도)"형식으로 페이로드에 저장합니다 .
        #페이로드는 실제로 메세지를 보낼때 담기는 데이터를 의미합니다 .

        self.update(True) # 옵저빙을 위해서 update 함수를 활성화 합니다 .

    def render_GET(self, request) :    #습도값 전송.
        h, t = Adafruit_DHT.read_retry(self.sensor, self.sensor_pin)
        self.payload = "%s"%(h) # "습도"형식으로 페이로드에 저장합니다.
        return self

    def update(self, first = False):   #observe 기능.
        if not self._coap_server.stopped.isSet():
            # 옵저빙은 주기적으로 재실행되는 쓰래드를 이용해서 구현된 듯 합니다.
            timer = threading.Timer(self.period, self.update) # __init__에서 선언한 self.period를 주기로 반복되는 쓰래드를 생성합니다 .
            timer.setDaemon(True)
            timer.start() # 쓰래드 시작
            if not first and self._coap_server is not None: # 실제로 쓰래드에서 동작하는 부분
                h, t = Adafruit_DHT.read_retry(self.sensor, self.sensor_pin) # 습도값을 읽어옵니다 .
                value = "Humidity : %s"%(h)
                if self.payload != value :  #이전 payoad값과 비교. 바뀌었을 경우 옵저브 메세지를 송신합니다.
                    logger.debug("Value Changed")
                    self.payload = value
                    self._coap_server.notify(self) #옵저브 메세지 송신
                    self.observe_count += 1

#서보모터.
class ServomotorResource(Resource) :
    def __init__(self, name="ServomotorResource", coap_server=None) :
        super(ServomotorResource, self).__init__(name, coap_server, visible=True, observable=True, allow_children=True)
        self.payload = ("** ServoMotor : Off **")

        #서보모터 설정
        GPIO.setmode(GPIO.BCM)  #GPIO핀 번호를 읽는 방법을 설정합니다.
        GPIO.setup(16, GPIO.OUT)    #서보모터의 출력 핀 번호와 출력모드로 설정합니다.
        pwm_pin = GPIO.PWM(16, 50)  #PWM : 펄스 폭 변조. 주파수는 50Hz
        pwm_pin.start(0)    #duty cycle : 0부터 시작

    #모터 On 함수.
    def render_PUT(self, request) :
        print("** ServoMotor On **")
        for i in range(5) :    #모터 회전을 5번 반복 합니다 .
            pwm_pin.ChangeDutyCycle(2.5)    #pwm을 2.5%로 하여 모터를 작동시킵니다.

    #모터 Off 함수.
    def render_DELETE(self, request) :
        print("** ServoMotor Off **")
        pwm_pin.ChangeDutyCycle(0)  #pwm을 0%로 하여 모터를 작동 중지시킵니다.
