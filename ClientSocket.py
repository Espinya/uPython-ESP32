from machine import Pin
import network 
import threading
import sleep

class ClientSocket:
  
  def __init__(self, IP, PORT):
      self.__s_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      self.__s_client.connect((HOST, PORT))#Nos conectamos al servidor con el puerto 9999
      self.__s_client.setblocking(False) #Blocking desactivado ya que tenemos un timeout, si no quedar谩 bloqueado indefinidamente si no hay respuesta
      s_client.write(bytes_valor)
      s_client.settimeout(5.0)
      self.__mode = 0x00
      self.__channel = 0x00
    



  def client(self):
    self.__mode = 0xA0
    self.__channel = 0x00
    self.sendData()#Pedir TECH
    sleep(1)
    self.getData()


    self.__mode = 0xA0
    self.__channel = 0x04
    self.sendData()#Pedir TECH
    sleep(1)
    self.getData()



  def getData(self):
    data=s_client.recv(1024)
    if (self.__mode == 0xA0):
      print("print TEDS", data)
    elif(self.__mode == 1):
      print("print float", data)
        #unc=unpack('B',request) 
        #chann=unpack('B',request)
  def sendData(self):
    data = bytearray(2)
    data[0] = self.__mode
    data[1] = self.__channel
    self.__s_client.sendall(data) 
        

 
