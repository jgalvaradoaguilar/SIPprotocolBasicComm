#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

import socket
import sys
import time
from xml.sax import make_parser
from xml.sax.handler import ContentHandler

# Cliente UA simple.

class UAClientHandler(ContentHandler):
  def __init__ (self):
    self.nombre_cliente = ""
    self.innombre_cliente = 0
    self.puerto_server = ""
    self.inpuerto_server = 0
    self.puerto_cancion = ""
    self.inpuerto_cancion = 0
    self.ruta_log_cliente = ""
    self.inruta_log_cliente = 0


  def startElement(self, name, attrs):
    if name == 'nombre_cliente':
      self.innombre_cliente = 1
    if name == 'puerto_server':
      self.inpuerto_server = 1
    if name == 'puerto_cancion':
      self.inpuerto_cancion = 1
    if name == 'ruta_log_cliente':
      self.inruta_log_cliente = 1

    

  def endElement(self, name):
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



  def characters(self, char):
    if self.innombre_cliente:
      self.nombre_cliente = self.nombre_cliente + char
    if self.inpuerto_server:
      self.puerto_server = self.puerto_server + char
    if self.inpuerto_cancion:
      self.puerto_cancion = self.puerto_cancion + char
    if self.inruta_log_cliente:
      self.ruta_log_cliente= self.ruta_log_cliente + char


if len(sys.argv) != 2:
   print
   print "Forma de ejecutar: $ ./UAClient  fichero_usuario"
   print
	# Y paramos aquí si no hay dos parámetros!
   sys.exit()


diccionario = {}
parser = make_parser()
cHandler = UAClientHandler()
parser.setContentHandler(cHandler)
parser.parse(open(sys.argv[1]))

nombre_cliente = diccionario['nombre_cliente']
puerto_server = diccionario['puerto_server']  
puerto_cancion = diccionario['puerto_cancion']      
ruta_log_cliente = diccionario['ruta_log_cliente']
salir = 0

# Dirección IP del servidor PROXY-REGISTER (Sheldon Cooper Server).
SERVER = 'localhost'
PORT = 15000      # Porque se va a conectar al servidor proxy-register
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
try:
   s.connect((SERVER, PORT))
except IOError:
   print '500 Server Internal Error. Se saldra de la aplicación'
   salir = 1


#se va a registrar automaticamente al ejecutar UAClient(se pasa el nombre cliente y el puerto donde recibira el audio)
#siempre que me haya conectado al servidor PROXY
if not salir:
   clave=raw_input('Dame tu contrasenia')
   LINE = "REGISTER"+" "+nombre_cliente+" "+puerto_server+" "+clave
   print "Enviando: %s" % LINE
   s.send('%s' % LINE)
   try:
      #tratamos el ACK recibido
      data = s.recv(1024)
      if data == 'ACK REGISTER OK':
         LINE = '200 OK: Se ha registrado correctamente'
      if data == 'ACK REGISTER FAIL':
         LINE = "403 FORBIDDEN: Contrasenia incorrecta. Se saldra del sistema"
         salir = 1
   except IOError:
      #si no se recibe el ACK
      LINE = '503 SERVICE UNAVAILABLE: No se puede registrar ahora. Se saldra de la aplicacion '
      salir = 1

   # se imprime el mensaje guardado en LINE
   print LINE
   # se guarda el evento en el fichero de log, cada vez se crea un nuevo log
   tiempo_actual = time.localtime()
   fichero=open(ruta_log_cliente,'w')
   fichero.write(str(time.strftime("%Y/%m/%d  %H:%M:%S", tiempo_actual))+' '+ LINE + "\r\n")     #ver si se pone str(LINE)
   fichero.close()
   
#hasta aqui entra si se ha registrado
#comienza un bucle para hacer peticiones
while not salir:
   print 'Menu del usuario'
   print '1: Pedir estadísticas'
   print '2: Lamar'
   print '3: Colgar'
   print '4: Buscar usuario'
   print '5: Salir del sistema'
   opcion=int(raw_input('Elige una opcion de las anteriores'))
   opcion_valida = 0

   ###Convenio : como no hay hilos siempre debera devolver por aqui OK sino es q ha pasado el timeout o es un hacker
   ###por lo que debe terminar la ejecución del programa

   #segun el valor de opcion se hara una cosa u otra
   if ((opcion >0 ) and (opcion<6)):
      opcion_valida = 1

   if opcion == 1:    # INFO: Estadisticas
      LINE = "INFO"+" "+nombre_cliente+" "+puerto_server
      line2file = "INFO petition"

   if opcion == 2:    # llamar
      #envio invite y me devuelve TRYING 100
      # prt = INVITE    + originador[0]   + puerto_server +    otro_usuario    + v     +   s            + t  +     m[0]     +     m[1]         + m[2]
      # originador[1] es la IP del cliente que hace el invite
      # Estos datos se trataran en el servidor proxy
      otro_usuario = raw_input('A que usuario quiere llamar?')
      LINE = "INVITE"+" "+nombre_cliente+" "+puerto_server+" "+otro_usuario+' '+'0'+' '+'s=misesion'+' '+'0'+' '+'audio'+' '+puerto_cancion+ ' '+ 'RTP'
      line2file = "INVITE petition"
   

   if opcion == 3:    # colgar
      #Finaliza la llamada (solo puede haber una llamada a la vez, por lo que no necesita decir a quien cuelga)
      LINE = "BYE"+" "+nombre_cliente+" "+puerto_server 
      line2file = "BYE(colgar) petition"

   if opcion == 4:    # buscar un usuario
      # SEARCH usuario@ejemplo.com
      usuario_buscado = raw_input('A que usuario quiere buscar?')
      LINE = "SEARCH" + " "+nombre_cliente+" "+puerto_server+' '+ usuario_buscado
      line2file = "SEARCH petition"
      

   if opcion == 5:    # salir del sistema
      clave=raw_input('Dame tu contrasenia')
      LINE = "BYE"+" "+nombre_cliente+" "+puerto_server+" "+clave
      line2file = "BYE(salir_sistema) petition"
      # se terminara la aplicacion UAClient(dentro del if de opcion_valida, si me asienten la peticion de bye)


   if (opcion_valida):
      # se envia LINE
      print "Enviando: %s" % LINE
      s.send('%s' % LINE)
      # se guarda el evento (la peticion) en el fichero de log
      tiempo_actual = time.localtime()
      fichero=open(ruta_log_cliente,'a')
      fichero.write(str(time.strftime("%Y/%m/%d  %H:%M:%S", tiempo_actual))+' '+ line2file + "\r\n")     #ver si se pone str(line2file)
      fichero.close()

      try:
         # siempre chequeo que no llegue un timeout al UAClient, si me llega timeout del PROXY se terminara el programa
         data = s.recv(1024)
         if data == 'TIMEOUT OCURRED':
            line2file = '504 Server Time-out. Se saldra de la aplicacion'
            # se terminara la aplicacion UAClient
            salir = 1  
         # chequeo otro posible mensaje de data (200 OK)
         if data == 'PETICION ACEPTADA':
            line2file = '200 OK. Se ha procesado su peticion'
         if data == 'BYE ACEPTADO':
            # se terminara la aplicacion UAClient
            line2file = 'ACK BYE. Se saldra de la aplicación'
            salir = 1
         if data == 'BYE NO ACEPTADO':
            line2file = 'BYE FAILED'
         if data == 'FALLO':
            line2file = '407 Proxy Authentication Required'
            salir = 1
      except IOError:
         #si hay algun error en recepcion
         line2file = '503: Service Unavailable'
         salir = 1

      # muestro el evento ocurrido(mensaje recibido)
      print line2file
      # se guarda el evento (mensaje recibido) en el fichero de log
      tiempo_actual = time.localtime()
      fichero=open(ruta_log_cliente,'a')
      fichero.write(str(time.strftime("%Y/%m/%d  %H:%M:%S", tiempo_actual))+' '+ line2file + "\r\n")     #ver si se pone str(line2file)
      fichero.close() 

   if (not(opcion_valida)):
      line2file = '405 Method Not Allowed : Opcion no pemitida'
      print line2file
      # se guarda el evento (mensaje recibido) en el fichero de log
      tiempo_actual = time.localtime()
      fichero=open(ruta_log_cliente,'a')
      fichero.write(str(time.strftime("%Y/%m/%d  %H:%M:%S", tiempo_actual))+' '+ line2file + "\r\n")     #ver si se pone str(line2file)
      fichero.close()

   if (salir):
      # se termina la aplicacion UAClient
      print "Terminando socket..."
      s.shutdown(1)
      print "Fin."
      



