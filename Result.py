#-*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import Adafruit_DHT
import time

#온습도센서 설정
sensor = Adafruit_DHT.DHT11 #사용할 센서를 저장합니다.
pin = 14    #핀번호를 저장합니다.

#서보모터 설정
GPIO.setmode(GPIO.BCM)  #GPIO핀 번호를 읽는 방법을 설정합니다.
GPIO.setup(16, GPIO.OUT)    #서보모터의 출력 핀 번호와 출력모드로 설정합니다.
pwm_pin = GPIO.PWM(16, 50)  #PWM : 펄스 폭 변조. 주파수는 50Hz
pwm_pin.start(0)    #duty cycle : 0부터 시작

#습도값을 읽어서 출력하는 함수
def humidity() :
        h, t = Adafruit_DHT.read_retry(sensor, pin) #온습도 센서로부터 습도, 온도값을 읽어들입니다.
        if h is not None and t is not None:
            print("Humidity = {0:0.1f}%".format(h)) #습도값만 출력 합니다.
            return h   #습도값을 반환 해 줍니다.
        else :
            print("Read error")

#서보모터 동작을 제어하는 함수 (모터 작동 or 중지)
def servomotor(mode) :
    try :
        if mode == "On" :   #모터 On
            print("** ServoMotor On **")
            for i in range(5) :    #모터 회전을 5번 반복 합니다 .
                pwm_pin.ChangeDutyCycle(2.5)    #pwm을 2.5%로 하여 모터를 작동시킵니다.
        elif mode == "Off":  #모터 Off
            print("** ServoMotor Off **")
            pwm_pin.ChangeDutyCycle(0)  #pwm을 0%로 하여 모터를 작동 중지시킵니다.
    except :
        pwm_pin.stop()

#수동모드 함수
def ManualMode(first=False) :
    while True :
        for i in range(5):   #습도값 출력을 5번 반복합니다.
            humidity()  #습도값을 출력합니다 .
            time.sleep(1)   #1초 간격
        motor = str(raw_input("Motor Operation Setting (On / Off) : "))  #모터 작동 여부를 묻습니다. (On or Off)
        servomotor(motor)   #사용자가 설정한 대로 서보모터를 제어합니다. (서보모터 제어 함수 호출)

#자동모드 함수
def AutoMode(first=False) :
    try :
        while True :
            h = float(humidity())   #습도값을 반환 받는다.
            if h >= 80 :    #습도값이 80% 이상일 때
                servomotor("On")    #서보모터 On
            else :  #습도값이 80% 미만일 때
                servomotor("Off")   #서보모터 Off
    except keyboardInterrupt :
        print("keyboardInterrupt")


mode = raw_input("Select the Mode (Manual / Auto) : ")  #모드선택
if mode == "Manual" :   #수동모드 선택 시
    print("<Manual Mode>")
    ManualMode(True)    #수동모드 함수를 실행합니다.
else :  #자동모드 선택 시
    print("<Auto Mode>")
    AutoMode(True)      #자동모드 함수를 실행합니다.
