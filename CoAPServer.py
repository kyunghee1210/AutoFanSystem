#-*-coding: utf-8-*-
from coapthon.server.coap import CoAP
import CoAPResource

class CoAPServer(CoAP) :
    def __init__(self, host, port) :
        CoAP.__init__(self, (host, port))    #ip주소와 포트번호로 서버 연결을 합니다 .
        #add_resource를 이용하여 Resource의 사용할 센서 혹은 액츄에이터의 클래스를 추가합니다.
        self.add_resource('humidity/', CoAPResource.HumidityResource(coap_server=self))
        self.add_resource('servomotor/', CoAPResource.ServomotorResource(coap_server=self))
        print("CoAP Server start on " + host + " : " + str(port))

def main() :
    server = CoAPServer("192.168.137.15", 5683)     #ip주소와 포트번호로 서버 연결을 합니다 .
    try :
        server.listen(10)
    except KeyboardInterrupt:
        print("Server Shutdown")
        server.close()
        print("Exiting...")

if __name__ == '__main__' :
    main()
