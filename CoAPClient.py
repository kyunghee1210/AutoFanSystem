from coapthon.client.helperclient import HelperClient
import timer

host = "192.168.137.15"     #ip주소
port = 5683     #포트번호
path_humidity = "humidity"  #온습도센서에 관한 class
path_servomotor = "servomotor"  #서보모터에 관한 class
count = 0
hum = 0

client = HelperClient(server = (host, port))

#Observe를 받았을 때 출력하는 함수
def OnReceiptionOfObserve(response) :
    print('observe callback')
    print(response.pretty_print())
    hum = float(client.get(path_humidity))  #get함수로 습도값을 읽어온 후, 실수 형태로 저장합니다.
    count += 1

mode = raw_input("Select the Mode (Manual / Auto) : ")  #모드선택
if mode == "Manual" :   #수동모드 선택 시
    print("<Manual Mode>")
    ManualMode(True)    #수동모드 함수를 실행합니다.
else :  #자동모드 선택 시
    print("<Auto Mode>")
    AutoMode(True)      #자동모드 함수를 실행합니다.

#수동모드 함수.
def ManualMode(self, first=False) :
    #observe를 이용하여 현재 습도값을 출력합니다.
    response = client.get(path_humidity)
    print(response.pretty_print())
    observe = client.observe(path_humidity, callback=OnReceiptionOfObserve)

    while True :
        if count >= 5:
            count == 0
        motor = input('Motor Operation Setting (On / Off) : ')  #모터 작동 여부를 묻습니다. (On or Off)
        if(motor == 'On') : #모터 On 선택 시
            client.put(path_servomotor) #Resource에서 서보모터 클래스의 Put함수를 호출합니다. (서보모터 작동)
        elif(motor == 'Off') :  #모터 Off 선택 시
            client.delete(path_servomotor)  #Resource에서 서보모터 클래스의 Delete함수를 호출합니다. (서보모터 작동 중지)

#자동모드 함수.
def AutoMode(self, first=False) :
    #observe를 이용하여 현재 습도값을 출력합니다.
    response = client.get(path_humidity)
    print(response.pretty_print())
    observe = client.observe(path_humidity, callback=OnReceiptionOfObserve)

    #습도값 비교.
    if(hum >= 80) : #습도값이 80% 이상일 때
        print('<Motor On>')
        client.put(path_servomotor)    #Resource에서 서보모터 클래스의 Put함수를 호출합니다. (서보모터 작동)
    else :  #습도값이 80% 미만일 때
        print('<Motor Off>')
        client.delete(path_servomotor)   #Resource에서 서보모터 클래스의 Delete함수를 호출합니다. (서보모터 작동 중지)
