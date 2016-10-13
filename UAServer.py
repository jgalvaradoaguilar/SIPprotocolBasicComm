#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

import sys
import socket
import SocketServer 
import os
import time
from xml.sax import make_parser
from xml.sax.handler import ContentHandler


# Servidor UA simple.

class UAServerHandler(ContentHandler):
  def __init__ (self):
    self.IP_server = ""
    self.inIP_server = 0
    self.nombre_cliente = ""
    self.innombre_cliente = 0
    self.puerto_server = ""
    self.inpuerto_server = 0
    self.puerto_cancion = ""
    self.inpuerto_cancion = 0
    self.ruta_log_cliente = ""
    self.inruta_log_cliente = 0
    self.ruta_MP32RTP = ""
    self.inruta_MP32RTP = 0
    self.ruta_cancion = ""
    self.inruta_cancion = 0


  def startElement(self, name, attrs):
    if name == 'IP_server':
      self.inIP_server = 1
    if name == 'nombre_cliente':
      self.innombre_cliente = 1
    if name == 'puerto_server':
      self.inpuerto_server = 1
    if name == 'puerto_cancion':
      self.inpuerto_cancion = 1
    if name == 'ruta_log_cliente':
      self.inruta_log_cliente = 1
    if name == 'ruta_MP32RTP':
      self.inruta_MP32RTP = 1
    if name == 'ruta_cancion':
      self.inruta_cancion = 1
    

  def endElement(self, name):
    if name == 'IP_server':
      diccionario['IP_server']=self.IP_server
      self.IP_server = ""
      self.inIP_server = 0
    if name == 'nombre_cliente':
      diccionario['nombre_cliente']=self.nombre_cliente
      self.nombre_cliente = ""
      self.innombre_cliente = 0
    if name == 'puerto_server':
      diccionario['puerto_server']=self.puerto_server
      self.puerto_server = ""
      self.inpuerto_server = 0
    if name == 'puerto_cancion':
      diccionario['puerto_cancion']=self.puerto_cancion
      self.puerto_cancion = ""
      self.inpuerto_cancion = 0
    if name == 'ruta_log_cliente':
      diccionario['ruta_log_cliente']=self.ruta_log_cliente
      self.ruta_log_cliente = ""
      self.inruta_log_cliente = 0
    if name == 'ruta_MP32RTP':
      diccionario['ruta_MP32RTP']=self.ruta_MP32RTP
      self.ruta_MP32RTP = ""
      self.inruta_MP32RTP = 0
    if name == 'ruta_cancion':
      diccionario['ruta_cancion']=self.ruta_cancion
      self.ruta_cancion = ""
      self.inruta_cancion = 0


  def characters(self, char):
    if self.inIP_server:
      self.IP_server = self.IP_server + char
    if self.innombre_cliente:
      self.nombre_cliente = self.nombre_cliente + char
    if self.inpuerto_server:
      self.puerto_server = self.puerto_server + char
    if self.inpuerto_cancion:
      self.puerto_cancion = self.puerto_cancion + char
    if self.inruta_log_cliente:
      self.ruta_log_cliente= self.ruta_log_cliente + char
    if self.inruta_MP32RTP:
      self.ruta_MP32RTP = self.ruta_MP32RTP + char
    if self.inruta_cancion:
      self.ruta_cancion = self.ruta_cancion + char

class UASHandler(SocketServer.DatagramRequestHandler):
   """
   Echo server class
   """

   def handle(self):
     if False:
        pass
     else:
     #if not salir:
         # Leyendo línea a línea lo que nos envía el cliente
         tiempo_actual = time.localtime()
         line = self.rfile.read()
         lista = line.split(' ')
         respuesta = lista[0]

         if respuesta == 'TIMEOUT':    #si se comprueba que se ha pasado su tiemout
            print '504 Server Time-out. Se saldra de la aplicacion'
            # se saldra de la aplicacion (con un break directamente)
            salir = 1
            # se anota el suceso(TIMEOUT) en el fichero de log del cliente
            fichero=open(ruta_log_cliente,'a')
            fichero.write(str(time.strftime("%Y/%m/%d  %H:%M:%S", tiempo_actual))+" TIMEOUT RECEIVED\r\n")
            fichero.close()

         if respuesta == 'ACK':
            metodo_asentido = lista[1]

            if metodo_asentido == 'REGISTER':
               estado = lista[2]
               if estado == 'OK':
                  linea = '200 OK(REGISTER). Se ha registrado correctamente'
               else:
                  linea = '494(REGISTER): Security Agreement Required'
                  salir = 1
            if metodo_asentido == 'INFO':
               linea = '200 OK(INFO)'
            if metodo_asentido == 'INVITE':
               linea = '200 OK(INVITE). Se acepta la llamada'
            if metodo_asentido == 'LOGOUT':
               linea = '200 OK(LOGOUT). Se ha cerrado la sesión'
               salir = 1
            if metodo_asentido == 'BYE':
               linea = '200 OK(BYE CALL). La llamada ha sido terminada'
      
            print linea
            # se anota el suceso(ACK del metodo) en el fichero de log del cliente
            fichero=open(ruta_log_cliente,'a')
            fichero.write(str(time.strftime("%Y/%m/%d  %H:%M:%S", tiempo_actual))+" ACK RECEIVED "+linea+"\r\n")
            fichero.close()



         if respuesta == 'INVITE':
            usr_origen_peticion=lista[1]
            puerto_rx_cancion_origen=lista[2]
            destinatario=lista[3]         #yo(el destinatario recibe esto)
            puerto_rx_cancion_dest = puerto_cancion
            # se anota el suceso(INVITE) en el fichero de log del cliente
            fichero=open(ruta_log_cliente,'a')
            fichero.write(str(time.strftime("%Y/%m/%d  %H:%M:%S", tiempo_actual))+" INVITE received from " + usr_origen_peticion+"\r\n")
            # le envia TRYING 100, RING 180, OK 200 al Servidor Proxy (Sheldon Cooper Server)que se comunico con el UAServer
            # envia directamente su puerto de escucha de audio para que el proxy no lo busque
            entrada_valida = False
            while not entrada_valida:
               print '¿Desea aceptar la llamada de '+usr_origen_peticion+'?'
               print '1: SI'
               print '2: NO'
               opcion=int(raw_input('Elige una opcion de las anteriores'))
               if opcion > 0 and opcion <3:
                  entrada_valida = True
            
            if opcion == 2:
               print 'No se acepto la llamada de '+usr_origen_peticion 
               fichero.write(str(time.strftime("%Y/%m/%d  %H:%M:%S", tiempo_actual))+" LLAMADA NO ACEPTADA from " + usr_origen_peticion+"\r\n")
               fichero.close()

            if opcion == 1:
               print 'Se acepta la llamada de '+usr_origen_peticion
               s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
               try:
                  s.connect(('localhost', 15000))
                  s.send("TRYING_100"+' '+usr_origen_peticion+' '+puerto_rx_cancion_origen+' '+destinatario+' '+puerto_rx_cancion_dest)
                  s.send("RING_180"+' '+usr_origen_peticion+' '+puerto_rx_cancion_origen+' '+destinatario+' '+puerto_rx_cancion_dest)
                  s.send("OK_200"+' '+usr_origen_peticion+' '+puerto_rx_cancion_origen+' '+destinatario+' '+puerto_rx_cancion_dest)
                  s.shutdown(1)
                  print 'Has enviado TRYING_100, RING_180, OK_200 a Sheldon Cooper Server'
               except IOError:
                  print '500 Server Internal Error'
               # se anotan los sucesos enviados al PROXY(TRYING_100, RING_180, OK_200)
               fichero.write(str(time.strftime("%Y/%m/%d  %H:%M:%S", tiempo_actual))+"  TRYING_100, RING_180, OK_200 for Sheldon Cooper Server\r\n")
               fichero.close()         

         if respuesta == 'TRYING_100':
            print 'Has recibido un TRYING_100'
            # se anota el suceso en el fichero de log del cliente
            fichero=open(ruta_log_cliente,'a')
            fichero.write(str(time.strftime("%Y/%m/%d  %H:%M:%S", tiempo_actual))+" TRYING 100 received\r\n")
            fichero.close()
   
         if respuesta == 'RING_180':
            destinatario_llamada = lista[1]
            print 'Has recibido RING_180 de ' + destinatario_llamada
            # se anota el suceso en el fichero de log del cliente
            fichero=open(ruta_log_cliente,'a')
            fichero.write(str(time.strftime("%Y/%m/%d  %H:%M:%S", tiempo_actual))+"RING 180 from " + destinatario_llamada+"\r\n")
            fichero.close()

         if respuesta == 'OK_200':  # si llega esto es xq soy el llamante
            destinatario_llamada = lista[1]
            puerto_rx_cancion_dest = lista[2]
            IP_destinatario = lista[3]
            usr_origen_peticion = nombre_cliente
            puerto_rx_cancion_origen = puerto_cancion
            print 'Has recibido OK_200 de '+destinatario_llamada
            # se anota el suceso recibido(OK_200) en el fichero de log del cliente
            fichero=open(ruta_log_cliente,'a')
            fichero.write(str(time.strftime("%Y/%m/%d  %H:%M:%S", tiempo_actual))+"OK 200 from " + destinatario_llamada+"\r\n")
            # envia un ACK al Servidor Proxy, que se lo redigira al destinatario
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            try:
               s.connect(('localhost', 15000))
               s.send("ACK_INVITE"+' '+usr_origen_peticion+' '+puerto_rx_cancion_origen+' '+destinatario_llamada+' '+puerto_rx_cancion_dest)
               s.shutdown(1)
            except IOError:
               print '500 Server Internal Error'
            # se anota el suceso enviado al servidor PROXY (ACK_INVITE) en el fichero de log del cliente
            fichero.write(str(time.strftime("%Y/%m/%d  %H:%M:%S", tiempo_actual))+"ACK (INVITE) to Sheldon Cooper SERVER\r\n")
            print 'Has enviado ACK (INVITE) a Sheldon Cooper Server'
            # se envia el trafico RTP
            #aEjecutar es un string con lo que se ha de ejecutar en la shell
            print 'Ahora comenzara la transmision de audio por RTP'
            fichero.write(str(time.strftime("%Y/%m/%d  %H:%M:%S", tiempo_actual))+"se esta enviando el trafico RTP\r\n")
            fichero.close()
            aEjecutar = ruta_MP32RTP + 'mp32rtp -i '
            aEjecutar += IP_destinatario + ' -p '+ puerto_rx_cancion_dest
            aEjecutar += ' < '+ ruta_cancion
            os.system(aEjecutar)


         if respuesta == 'INFO':       #metodo terminado
            print line
            # se anota el suceso (INFO) en el fichero de log del cliente
            fichero=open(ruta_log_cliente,'a')
            fichero.write(str(time.strftime("%Y/%m/%d  %H:%M:%S", tiempo_actual))+"INFO received:  " + line+"\r\n")
            fichero.close()

         if respuesta == 'EXISTE':     #para tratar las respuestas a SEARCH
            en_sistema = lista[1]
            usuario_buscado = lista[2]
            if en_sistema == 'SI': 
               linea = 'El usuario '+usuario_buscado+ ' lleva registrado: ' + lista[3]  
            else:
               linea = 'El usuario '+usuario_buscado+ ' no está registrado en este momento'
            print linea
            # se anota el suceso en el fichero de log del cliente
            fichero=open(ruta_log_cliente,'a')
            fichero.write(str(time.strftime("%Y/%m/%d  %H:%M:%S", tiempo_actual))+' '+ linea + "\r\n")
            fichero.close()


         if respuesta == 'BYE':        #me han pedido que cuelgue la llamada
            #line2 = 'BYE'+' '+usr_origen_peticion+' '+puerto_rx_usuario+' 'otro_usuario+' '+puerto_otro_usuario
            usr_origen_peticion=lista[1]
            puerto_origen_peticion =lista[2]
            otro_usuario=lista[3]
            # se anota el suceso en el fichero de log del cliente
            fichero=open(ruta_log_cliente,'a')
            fichero.write(str(time.strftime("%Y/%m/%d  %H:%M:%S", tiempo_actual))+" BYE(colgar) received from " + usr_origen_peticion+ "\r\n")
            fichero.close()
            print 'Has recibido BYE (colgar) de '+usr_origen_peticion
            #le envia un ACK al servidor Proxy
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            try:
               s.connect(('localhost', 15000))
               s.send("ACK_BYE"+" "+usr_origen_peticion+" "+puerto_origen_peticion+' '+otro_usuario)
               s.shutdown(1)
               print 'La llamada ha sido finalizada. Envias ACK (BYE)'
            except IOError:
               print '500 Server Internal Error'
 

         if respuesta == '401':        #esto puede ser un intento de hackear o porque el timeout se paso mientras se hacia la peticion
            print line

# Creamos servidor de eco y escuchamos
if len(sys.argv) != 2:
   print
   print "Forma de ejecutar: $ ./UAServer fichero_usuario"
   print
	# Y paramos aquí si no hay dos parámetros!
   sys.exit()

diccionario = {}
parser = make_parser()
cHandler = UAServerHandler()
parser.setContentHandler(cHandler)
parser.parse(open(sys.argv[1]))

nombre_cliente = diccionario['nombre_cliente']
IP = diccionario['IP_server']
puerto = int(diccionario['puerto_server'])
puerto_cancion = diccionario['puerto_cancion']
ruta_log_cliente = diccionario['ruta_log_cliente']
ruta_MP32RTP = diccionario['ruta_MP32RTP']
ruta_cancion = diccionario['ruta_cancion']
serv = SocketServer.UDPServer((IP,puerto), UASHandler)
print "Lanzando servidor de UAS..."
salir = 0
serv.serve_forever()





