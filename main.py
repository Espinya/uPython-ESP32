try:
 import usocket as socket
except:
  import socket
from machine import Pin
import network
import esp
esp.osdebug(None)
import gc
from struct import *
import _thread
import time
 
 
#Thread del servidor con el que esperaremos hasta que un cliente se conecte
def serverThread():
  s_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Creación del socket
  s_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #Para poder reutilizar un puerto
  s_server.bind(('', 9999))#El socket estará escuchando al puerto 9999 
  s_server.listen(1)#Solo aceptará una conexión simultánea
  print('Server: Listening')
  conn, addr = s_server.accept()#Se queda esperando hasta recibir una conexión
  #La conexión con el cliente pasa al socket conn
  print('Server: Got a connection from %s' % str(addr))
  conn.settimeout(20.0)#Establecemos un  tiempo de espera para la respuesta
  request = conn.recv(1024)
  print('Server: Content =', request)
  request_float=unpack('f',request)
  print('Server: float de content = %2f' % (request_float))
  response = 'Server message'
  conn.sendall(response)#Enviamos un mensaje al cliente
  conn.close()#Cerramos el socket del cliente
  s_server.close()#Cerramos el socket que estaba escuchando
  sys.exit()#Cerramos el thread
  
  """El socket se tiene que cerrar, ya que al menos en el IDE uPyCraft, por lo visto el thread sigue
  estando activo aún habiendo cargado otro código, por lo tanto, la manera más simple de eliminar el thread
  es realizar todas las instrucciones de la función del thread, habiendo de suprimir el loop para recibir otras
  conexiones. Estoy mirando otras librerías como threading que es más sencillo eliminar el thread
  desde el main, pero me parece que no está en upython También he probado el gc.collect y no es eficaz"""
  

def clientThread(): #Thread del cliente, se conectará a la dirección local y enviará un mensaje al socket del servidor
  s_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  HOST = '127.0.0.1'#La ip es la dirección local, si se ejecuta el servidor y el cliente desde la máquina, está IP siempre será válida
  PORT = 9999
  valor = 5.2
  print ('Client: valor=', valor)
  bytes_valor=pack('f', valor)
  dada = bytes([3, 5, 8, 9])
  s_client.connect((HOST, PORT))#Nos conectamos al servidor con el puerto 9999
  s_client.setblocking(False) #Blocking desactivado ya que tenemos un timeout, si no quedará bloqueado indefinidamente si no hay respuesta
  s_client.write(bytes_valor)
  s_client.settimeout(5.0)
  data=s_client.recv(1024)
  print('Client: received: =', data)
  s_client.close()
  sys.exit()
 

_thread.start_new_thread(serverThread, ())#Creamos el thread del servidor
time.sleep(2)#Esperamos cierto tiempo, para que el servidor se inicie correctamente
_thread.start_new_thread(clientThread, ())#Creamos el thread para el cliente

