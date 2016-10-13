#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

import sys
import SocketServer
import socket
import time 
from xml.sax import make_parser
from xml.sax.handler import ContentHandler


# Servidor de REGISTRO-PROXY simple.

class FicheroProxyHandler(ContentHandler):
  def __init__ (self):
    self.nombre = ""
    self.innombre = 0
    self.IP = ""
    self.inIP = 0
    self.puerto = ""
    self.inpuerto = 0
    self.ruta_log = ""
    self.inruta_log = 0
    self.ruta_base_usuarios = ""
    self.inruta_base_usuarios = 0
    self.timeout = ""
    self.intimeout = 0
    self.usuario1 = ""
    self.inusuario1 = 0
    self.clave_usuario1 = ""
    self.inclave_usuario1 = 0
    self.usuario2 = ""
    self.inusuario2 = 0
    self.clave_usuario2 = ""
    self.inclave_usuario2 = 0
    self.usuario3 = ""
    self.inusuario3 = 0
    self.clave_usuario3 = ""
    self.inclave_usuario3 = 0

  def startElement(self, name, attrs):
    if name == 'nombre':
      self.innombre = 1
    if name == 'IP':
      self.inIP = 1
    if name == 'puerto':
      self.inpuerto = 1
    if name == 'ruta_log':
      self.inruta_log = 1
    if name == 'ruta_base_usuarios':
      self.inruta_base_usuarios = 1
    if name == 'timeout':
      self.intimeout = 1
    if name == 'usuario1':
      self.inusuario1 = 1
    if name == 'clave_usuario1':
      self.inclave_usuario1 = 1
    if name == 'usuario2':
      self.inusuario2 = 1
    if name == 'clave_usuario2':
      self.inclave_usuario2 = 1
    if name == 'usuario3':
      self.inusuario3 = 1
    if name == 'clave_usuario3':
      self.inclave_usuario3 = 1
   
    

  def endElement(self, name):
    if name == 'nombre':
      diccionario['nombre']=self.nombre
      self.nombre = ""
      self.innombre = 0
    if name == 'IP':
      diccionario['IP']=self.IP
      self.IP = ""
      self.inIP = 0
    if name == 'puerto':
      diccionario['puerto']=self.puerto
      self.puerto = ""
      self.inpuerto = 0
    if name == 'ruta_log':
      diccionario['ruta_log']=self.ruta_log
      self.ruta_log = ""
      self.inruta_log = 0
    if name == 'ruta_base_usuarios':
      diccionario['ruta_base_usuarios']=self.ruta_base_usuarios
      self.ruta_base_usuarios = ""
      self.inruta_base_usuarios = 0
    if name == 'timeout':
      diccionario['timeout']=self.timeout
      self.timeout = ""
      self.intimeout = 0
    if name == 'usuario1':
      diccionario['usuario1']=self.usuario1
      self.usuario1 = ""
      self.inusuario1 = 0
    if name == 'clave_usuario1':
      diccionario['clave_usuario1']=self.clave_usuario1
      self.clave_usuario1 = ""
      self.inclave_usuario1 = 0
    if name == 'usuario2':
      diccionario['usuario2']=self.usuario2
      self.usuario2 = ""
      self.inusuario2 = 0
    if name == 'clave_usuario2':
      diccionario['clave_usuario2']=self.clave_usuario2
      self.clave_usuario2 = ""
      self.inclave_usuario2 = 0
    if name == 'usuario3':
      diccionario['usuario3']=self.usuario3
      self.usuario3 = ""
      self.inusuario3 = 0
    if name == 'clave_usuario3':
      diccionario['clave_usuario3']=self.clave_usuario3
      self.clave_usuario3 = ""
      self.inclave_usuario3 = 0



  def characters(self, char):
    if self.innombre:
      self.nombre = self.nombre + char
    if self.inIP:
      self.IP = self.IP + char
    if self.inpuerto:
      self.puerto = self.puerto + char
    if self.inruta_log:
      self.ruta_log = self.ruta_log + char
    if self.inruta_base_usuarios:
      self.ruta_base_usuarios = self.ruta_base_usuarios + char
    if self.intimeout:
      self.timeout = self.timeout + char
    if self.inusuario1:
      self.usuario1 = self.usuario1 + char
    if self.inclave_usuario1:
      self.clave_usuario1 = self.clave_usuario1 + char
    if self.inusuario2:
      self.usuario2 = self.usuario2 + char
    if self.inclave_usuario2:
      self.clave_usuario2 = self.clave_usuario2 + char
    if self.inusuario3:
      self.usuario3 = self.usuario3 + char
    if self.inclave_usuario3:
      self.clave_usuario3 = self.clave_usuario3 + char



class EchoProxyHandler(SocketServer.DatagramRequestHandler):
   """
   Echo server class
   """

   def handle(self):
      # Leyendo línea a línea lo que nos envía el cliente
      line = self.rfile.read()
      IP_origen_peticion = str(self.client_address[0])
      print "Un cliente nos manda " + line
      lista = line.split(' ')
      # Chequeo que peticion es
      peticion = lista[0]
      usr_origen_peticion = lista[1]
      puerto_rx_usuario = lista[2]
      tiempo_mostrar = time.localtime()

      if peticion == 'REGISTER':
         registrado = 0
         clave_usr = lista[3]
         # Miro el tiempo de recepcion
         tiempo_rg = time.time()
         if clave_usr == dicc_claves[usr_origen_peticion]:
            # Guardo el suceso(REGISTER) en el fichero de log del servidor proxy
            fichero=open(ruta_log_proxy,'a')
            fichero.write( str(time.strftime("%Y/%m/%d  %H:%M:%S", tiempo_mostrar))+" REGISTER received from "+usr_origen_peticion + "\r\n")
            fichero.close()
            # Los REGISTER's ademas se vuelcan en un fichero de base de datos de usuarios registrados que se actualiza con el tiempo
            dicc_registers[usr_origen_peticion] = usr_origen_peticion + ' ' + IP_origen_peticion+" "+puerto_rx_usuario + ' ' + clave_usr+" "+str(time.strftime("%Y/%m/%d  %H:%M:%S", tiempo_mostrar)) + " " + str(tiempo_rg)
            fichero=open(ruta_base_usuarios,'w')
            for x in dicc_registers.keys():
               fichero.write( dicc_registers[x] +"\r\n")  
            fichero.close()
            # Asiento el REGISTER (ACK clave) al UAClient      #sin clave xq el usuario se registro con una!!!
            self.wfile.write("ACK REGISTER OK")
            registrado = 1
         else:
            self.wfile.write("ACK REGISTER FAIL")
            registrado = 0
            # se guarda el suceso (REGISTER FAILED) en el fichero de log del servidor proxy
            fichero=open(ruta_log_proxy,'a')
            fichero.write( str(time.strftime("%Y/%m/%d  %H:%M:%S", tiempo_mostrar))+"  REGISTER received from "+usr_origen_peticion + " HAS FAILED\r\n")
            fichero.close()

         # tambien le debe comunicar el suceso al UAServer (ya que no usa hilos!!!)   
         try:
            aux = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            aux.connect((IP_origen_peticion, int(puerto_rx_usuario)))
            if registrado:
               line2 = 'ACK REGISTER OK'
            else:
               line2 = 'ACK REGISTER FAIL'
            aux.send('%s' % line2)
            aux.shutdown(1)
         except IOError:
            print '480 Temporarily Unavailable. No se puede comunicar con el UAServer'


      # siempre que la peticion no sea REGISTER lo primero que se hara es actualizar mi diccionario de registers (y el fichero tambien)
      # si el usuario ha excedido su tiempo ademas le envio un timeout y no se procesara su peticion
      if (not(peticion == 'REGISTER')):
         timeout_origen_peticion = 0
         tiempo_actual = time.time()
         for x in dicc_registers.keys():
            lista2 = dicc_registers[x].split(' ')
            tiempo_transcurrido = tiempo_actual - float(lista2 [-1])    #menos el t de registro
            # si tiempo_transcurrido > timeout, se dara de baja al usuario
            if (tiempo_transcurrido > timeout):
               # Guardo el suceso(timeout) en el fichero de log del servidor proxy
               fichero=open(ruta_log_proxy,'a')
               fichero.write(str(time.strftime("%Y/%m/%d  %H:%M:%S", tiempo_mostrar))+"  TIMEOUT for "+ lista2[0] + "\r\n")
               fichero.close()
               # se envia el timeout para informarle al UAServer que ha sido dado de baja
               try:
                  aux = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                  aux.connect(( lista2[1], int(lista2[2]) ))      # IP, puerto
                  line2 = 'TIMEOUT OCURRED'
                  aux.send('%s' % line2)
                  aux.shutdown(1)
               except IOError:
                  print '480 Temporarily Unavailable'
               # si hay timeout de quien envia el mensaje(UAClient) se le comunica por el mismo socket, ya que debe terminar el programa en ambos
               if (x == usr_origen_peticion):
                  self.wfile.write("TIMEOUT OCURRED")
                  timeout_origen_peticion = 1
               # borro al usuario del registro
               del(dicc_registers[x])
         #actualizo tambien de la base de datos de register
         fichero=open(ruta_base_usuarios,'w')
         for x in dicc_registers.keys():
            fichero.write( dicc_registers[x] +"\r\n")  
         fichero.close()

         # Comprobamos que el usuario exista en el diccionario de registers y si existe puedo cumplir sus peticiones
         existe = dicc_registers.has_key(usr_origen_peticion)
   
         # se comprueba que existe y luego el tipo de peticion que hace
         if (existe) : 
            # le digo que todo esta correcto al UAClient
            # si se ha elegido salir del sma (y la contraseña es correcta)se enviara otro mensaje
            if (not(peticion == 'BYE')):
               self.wfile.write("PETICION ACEPTADA")
            
            # y tambien al UAServer (se hace dentro de cada metodo: ACK metodo_asentido)
            if peticion == 'INFO':  #metodo terminado
               # Guardo el suceso(INFO) en el fichero de log del servidor proxy
               fichero=open(ruta_log_proxy,'a')
               fichero.write(str(time.strftime("%Y/%m/%d  %H:%M:%S", tiempo_mostrar))+"  INFO from "+ usr_origen_peticion + "\r\n")
               fichero.close()
               # se envia ACK y la info de los usarios conectados en ese momento
               try:
                  aux = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                  aux.connect((IP_origen_peticion, int(puerto_rx_usuario)))
                  aux.send("ACK INFO")
                  for x in dicc_registers.keys():
                     line2 = 'INFO' + ' ' + x + " ha estado registrado durante " + str(time.strftime("%H:%M:%S", time.gmtime(tiempo_transcurrido)))
                     aux.send('%s' % line2)
                  aux.shutdown(1)
               except IOError:
                  print '480 Temporarily Unavailable'
              


      # prt = INVITE    + originador[0]   +    m[1]       +    otro_usuario    + v     +   s            + t  +     m[0]     + m[2]
      # originador[1] es la IP del cliente que hace el invite
      # Estos datos se trataran en el servidor proxy
      #LINE = "INVITE"+" "+nombre_cliente+" "+puerto_server+" "+otro_usuario+' '+'0'+' '+'misesion'+' '+'0'+' '+'audio'+' '+'RTP'



            if peticion == 'INVITE' :
               org_0= lista[1]
               destinatario = lista[3]
               v=lista[4]
               s=lista[5]
               t=lista[6]
               m_0 = lista[7]
               m_1 = lista[8]
               m_2 = lista[9]
               # Guardo el suceso(INVITE) en el fichero de log del servidor proxy
               fichero=open(ruta_log_proxy,'a')
               fichero.write(str(time.strftime("%Y/%m/%d  %H:%M:%S", tiempo_mostrar))+' INVITE'+' '+destinatario+' '+'received from '+ usr_origen_peticion
                              + "\r\n")
               fichero.write('v='+v+'\r\n')
               fichero.write('o='+org_0+' '+IP_origen_peticion+'\r\n')
               fichero.write('s='+s+'\r\n')
               fichero.write('t='+t+'\r\n')
               fichero.write('m='+m_0+' '+m_1+' '+m_2+'\r\n')
               #miro que exista el usuario destino
               existe = dicc_registers.has_key(destinatario)
               ocupado = dicc_llamadas.has_key(destinatario)
               # se comprueba que exista y ademas no este ocupado
               if (existe and (not ocupado)):
                  # se envia TRYING 100 y RING 180, ademas del  OK 200 al UAClient y UAServer
                  try:
                     aux = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                     aux.connect( (IP_origen_peticion, int(puerto_rx_usuario)) )
                     aux.send("TRYING_100")
                     aux.shutdown(1)
                     # Guardo el suceso enviado(TRYING_100)
                     fichero.write(str(time.strftime("%Y/%m/%d  %H:%M:%S", tiempo_mostrar))+' TRYING_100 to ' +usr_origen_peticion+ "\r\n")
                     #redirijo la peticion de INVITE al usuario (UAServer) llamado
                     lista2 = dicc_registers[destinatario].split(' ')
                     aux2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                     aux2.connect((lista2[1], int(lista2[2])))
                     line2 = "INVITE"+" "+usr_origen_peticion+" "+m_1+" "+destinatario
                     aux2.send('%s' % line2)
                     aux2.shutdown(1) 
                     # Guardo el suceso enviado(INVITE redirigido) en el fichero de log del servidor proxy
                     fichero.write(str(time.strftime("%Y/%m/%d  %H:%M:%S", tiempo_mostrar))+' INVITE to '+ destinatario + "\r\n")                  
                     fichero.close()
                  except IOError:
                     print '480 Temporarily Unavailable' 
               else:
                  fichero.write("No se puede redirigir el INVITE\r\n")
                  fichero.close()


            if peticion == 'TRYING_100':
               destinatario = lista[3]
               # Guardo el suceso(TRYING_100) en el fichero de log del servidor proxy
               fichero=open(ruta_log_proxy,'a')
               fichero.write(str(time.strftime("%Y/%m/%d  %H:%M:%S", tiempo_mostrar))+"  TRYING 100 from "+ destinatario+ "\r\n")
               fichero.close()
               
            if peticion == 'RING_180':
               destinatario = lista[3]
               puerto_rx_cancion_dest = lista[4]
               # Guardo el suceso recibido(RING_180) en el fichero de log del servidor proxy
               fichero=open(ruta_log_proxy,'a')
               fichero.write(str(time.strftime("%Y/%m/%d  %H:%M:%S", tiempo_mostrar))+"  RING 180 from "+ destinatario+ "\r\n")
               # Guardo el suceso enviado(RING_180) en el fichero de log del servidor proxy
               fichero.write(str(time.strftime("%Y/%m/%d  %H:%M:%S", tiempo_mostrar))+"  RING 180 to"+ usr_origen_peticion+ "\r\n") 
               fichero.close()
               # Envio el correspondiente RING_180 al llamante(UAServer)
               lista2 = dicc_registers[usr_origen_peticion].split(' ')
               aux2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
               aux2.connect((lista2[1], int(lista2[2])))
               line2 = "RING_180"+" "+destinatario+" "+puerto_rx_cancion_dest
               aux2.send('%s' % line2)
               aux2.shutdown(1)  
      
            if peticion == 'OK_200':
               destinatario = lista[3]
               puerto_rx_cancion_dest = lista[4]
               # Guardo el suceso recibido(OK_200) en el fichero de log del servidor proxy
               fichero=open(ruta_log_proxy,'a')
               fichero.write(str(time.strftime("%Y/%m/%d  %H:%M:%S", tiempo_mostrar))+"  OK_200 from "+ destinatario+ "\r\n")
               # Guardo el suceso enviado(OK_200) en el fichero de log del servidor proxy
               fichero.write(str(time.strftime("%Y/%m/%d  %H:%M:%S", tiempo_mostrar))+"  OK 200 to"+ usr_origen_peticion+ "\r\n") 
               fichero.close()
               # los anoto como que estan cursando una llamada
               dicc_llamadas[destinatario] = usr_origen_peticion
               dicc_llamadas[usr_origen_peticion] = destinatario
               # Envio el correspondiente OK_200 al llamante(UAServer)
               lista2 = dicc_registers[usr_origen_peticion].split(' ')
               aux2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
               aux2.connect((lista2[1], int(lista2[2])))
               IP_destinatario = lista2[1]
               line2 = "OK_200"+" "+destinatario+" "+puerto_rx_cancion_dest+" "+IP_destinatario
               aux2.send('%s' % line2)
               aux2.shutdown(1)

            if peticion == 'ACK_INVITE':
               destinatario = lista[3]
               puerto_rx_destinatario = lista[4]
               # Guardo el suceso recibido(ACK_INVITE) en el fichero de log del servidor proxy
               fichero=open(ruta_log_proxy,'a')
               fichero.write(str(time.strftime("%Y/%m/%d  %H:%M:%S", tiempo_mostrar))+"  ACK_INVITE from "+ usr_origen_peticion+ "\r\n")
               # Guardo el suceso enviado(ACK_INVITE) en el fichero de log del servidor proxy
               fichero.write(str(time.strftime("%Y/%m/%d  %H:%M:%S", tiempo_mostrar))+"  ACK_INVITE to"+ destinatario+ "\r\n") 
               fichero.close()
               # Envio el correspondiente ACK_INVITE al llamante(UAServer)
               lista2 = dicc_registers[destinatario].split(' ')
               aux2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
               aux2.connect((lista2[1], int(lista2[2])))
               line2 = "ACK INVITE"
               aux2.send('%s' % line2)
               aux2.shutdown(1)


            if peticion == 'SEARCH' :           #metodo terminado
               usuario_buscado = lista[3]
               # Guardo el suceso(INFO) en el fichero de log del servidor proxy
               fichero=open(ruta_log_proxy,'a')
               fichero.write(str(time.strftime("%Y/%m/%d  %H:%M:%S", tiempo_mostrar))+"  SEARCH from "+ usr_origen_peticion + ' [' + usuario_buscado +']'+ "\r\n")
               #confirmar que existe en el diccionario de registers
               existe = dicc_registers.has_key(usuario_buscado)
               #depende si existe o no envio una cosa u otra
               if existe:
                  lista2 = dicc_registers[usuario_buscado].split(' ')
                  tiempo_actual = time.time()
                  tiempo_transcurrido = tiempo_actual - float(lista2 [-1])    #menos el t de registro
                  line2 = "EXISTE" + " " + "SI" + " " + usuario_buscado+" "+ str(time.strftime("%H:%M:%S", time.gmtime(tiempo_transcurrido)))
               else:
                  line2 = "EXISTE" + " " + "NO" + " " + usuario_buscado
               # Guardo el suceso(info de EXISTE) en el fichero de log del servidor proxy
               fichero.write(str(time.strftime("%Y/%m/%d  %H:%M:%S", tiempo_mostrar))+ ' '+ line2 +"\r\n")
               fichero.close()
               # se le envia la info de EXISTE al UAServer
               try:
                  aux = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                  aux.connect((IP_origen_peticion, int(puerto_rx_usuario)))
                  aux.send('%s' % line2)
                  aux.shutdown(1)
               except IOError:
                  print '480 Temporarily Unavailable. Se saldra de la aplicación'


            if peticion == 'BYE' :
               if len(lista) == 3:     # para colgar la llamada BYE usr_origen_peticion puerto_rx_usuario
                  self.wfile.write("PETICION ACEPTADA")
                  # Guardo el suceso(BYE recibido) en el fichero de log del servidor proxy
                  fichero=open(ruta_log_proxy,'a')
                  fichero.write(str(time.strftime("%Y/%m/%d  %H:%M:%S", tiempo_mostrar))+ "  BYE(colgar) from "+ usr_origen_peticion + "\r\n")
                  fichero.close()
                  # se confirma que tenga una llamada en curso(existe en dicc_llamadas)
                  existe = dicc_llamadas.has_key(usr_origen_peticion)
                  if existe:
                     otro_usuario = dicc_llamadas[usr_origen_peticion]
                     lista2 = dicc_registers[otro_usuario].split(' ')
                     aux = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                     puerto_otro_usuario = lista2[2]
                     # se envia el BYE al otro usuario
                     aux.connect((lista2[1], int(puerto_otro_usuario)))
                     line2 = 'BYE'+' '+usr_origen_peticion+' '+puerto_rx_usuario+' '+otro_usuario+' '+puerto_otro_usuario
                     aux.send('%s' % line2)
                     aux.shutdown(1)
                     # Guardo el suceso(envio de BYE) en el fichero de log del servidor proxy
                     fichero=open(ruta_log_proxy,'a')
                     fichero.write(str(time.strftime("%Y/%m/%d  %H:%M:%S", tiempo_mostrar))+ "  BYE(colgar) to "+ otro_usuario + "\r\n")
                     fichero.close()
               
                     
                

               if len(lista) == 4:      # para darse de baja del sistema BYE usr_origen_peticion puerto_rx_usuario contrasenia
                  contrasenia = lista[3]
                  # Guardo el suceso(BYE recibido) en el fichero de log del servidor proxy
                  fichero=open(ruta_log_proxy,'a')
                  fichero.write(str(time.strftime("%Y/%m/%d  %H:%M:%S", tiempo_mostrar))+ "  BYE from "+ usr_origen_peticion + "\r\n")
                  fichero.close()
                  if contrasenia == dicc_claves[usr_origen_peticion]:
                     self.wfile.write('BYE ACEPTADO')
                     del(dicc_registers[usr_origen_peticion])
                     #actualizo tambien de la base de datos de register
                     fichero=open(ruta_base_usuarios,'w')
                     for x in dicc_registers.keys():
                        fichero.write( dicc_registers[x] +"\r\n")  
                     fichero.close()
                     # se lo elimina también del diccionario de llamadas en curso, si estuviera hablando
                     # al otro tambien, para que solo haya una llamada a la vez
                     existe = dicc_llamadas.has_key(usr_origen_peticion)
                     if existe:
                           # se le dice al otro usuario que su llamada se ha terminado
                           otro_usuario = dicc_llamadas[usr_origen_peticion]
                           lista2 = dicc_registers[otro_usuario].split(' ')
                           aux = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                           puerto_otro_usuario = lista2[2]
                           # se envia el BYE al otro usuario
                           aux.connect((lista2[1], int(puerto_otro_usuario)))
                           line2 = 'BYE'+' '+usr_origen_peticion+' '+puerto_rx_usuario+' '+otro_usuario+' '+puerto_otro_usuario
                           aux.send('%s' % line2)
                           aux.shutdown(1)
                           # Guardo el suceso(envio de BYE) en el fichero de log del servidor proxy
                           fichero=open(ruta_log_proxy,'a')
                           fichero.write(str(time.strftime("%Y/%m/%d  %H:%M:%S", tiempo_mostrar))+ "  BYE(colgar) to "+ otro_usuario + "\r\n")
                           fichero.close()
                     # se le envia la info al UAServer
                     aux = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                     try:
                        aux.connect((IP_origen_peticion, int(puerto_rx_usuario)))
                        line2 = 'ACK LOGOUT'
                        aux.send('%s' % line2)
                        aux.shutdown(1)
                     except IOError:
                        print '480 Temporarily Unavailable. Se saldra de la aplicación'
                     # Guardo el suceso(ACK LOGOUT) en el fichero de log del servidor proxy
                     fichero=open(ruta_log_proxy,'a')
                     fichero.write(str(time.strftime("%Y/%m/%d  %H:%M:%S", tiempo_mostrar))+"  ACK LOGOUT to "+ usr_origen_peticion + "\r\n")
                     fichero.close()
                  else:
                     self.wfile.write("BYE NO ACEPTADO")

            if peticion == 'ACK_BYE':
               # se le envia el ACK_BYE al UAServer que origino el fin de llamada
               aux = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
               try:
                  aux.connect((IP_origen_peticion, int(puerto_rx_usuario )))
                  line2 = 'ACK BYE'
                  aux.send('%s' % line2)
                  aux.shutdown(1)
               except IOError:
                  print '480 Temporarily Unavailable. Se saldra de la aplicación'  
               # Guardo el suceso enviado (ACK_BYE) en el fichero de log del servidor proxy
               fichero=open(ruta_log_proxy,'a')
               fichero.write(str(time.strftime("%Y/%m/%d  %H:%M:%S", tiempo_mostrar))+"  ACK_BYE for "+ usr_origen_peticion + "\r\n")
               fichero.close()         
               # cuelga la llamada
               otro_usuario = lista[3]
               del(dicc_llamadas[usr_origen_peticion])
               del(dicc_llamadas[otro_usuario])
    
         else:                   # si no existe quien hizo la peticion
            # compruebo que no se haya borrado por un timeout, ya que si no es por timeout, es un hacker!!
            if (not(timeout_origen_peticion)):
               line2 = '401 Unauthorized. Se ha intentado acceder de forma no valida al servidor!!!'
               print line2
               # Guardo el suceso(acceso no autorizado) en el fichero de log del servidor proxy
               fichero=open(ruta_log_proxy,'a')
               fichero.write(str(time.strftime("%Y/%m/%d  %H:%M:%S", tiempo_mostrar))+"  401 Unauthorized for "+ usr_origen_peticion + "\r\n")
               fichero.close()
               # le digo que hubo un fallo al UAClient
               self.wfile.write("FALLO")
               # se envia la info del suceso al usuario o hacker
               aux = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
               try:
                  aux.connect((IP_origen_peticion, int(puerto_rx_usuario)))  
                  aux.send('%s' % line2)
                  aux.shutdown(1)    
               except IOError:
                  print '480 Temporarily Unavailable. Se saldra de la aplicación'
     


# Creamos servidor de eco y escuchamos
if len(sys.argv) != 2:
   print
   print "Forma de ejecutar: $ ./ServidorREGPRX fichero_configuracion"
   print
	# Y paramos aquí si no hay dos parámetros!
   sys.exit()

diccionario = {}
dicc_claves = {}
dicc_registers = {}
dicc_llamadas = {}
parser = make_parser()
cHandler = FicheroProxyHandler()
parser.setContentHandler(cHandler)
parser.parse(open(sys.argv[1]))

nombre_proxy = diccionario['nombre']
IP_proxy = diccionario['IP']
puerto_proxy = int(diccionario['puerto'])        
ruta_log_proxy = diccionario['ruta_log']
ruta_base_usuarios = diccionario['ruta_base_usuarios']
timeout = float(diccionario['timeout'])
usuario1 = diccionario['usuario1']
clave_usuario1 = diccionario['clave_usuario1']
usuario2 = diccionario['usuario2']
clave_usuario2 = diccionario['clave_usuario2']
usuario3 = diccionario['usuario3']
clave_usuario3 = diccionario['clave_usuario3']
# ahora lo ubico en un diccionario de claves!!! (este se usara en el codigo)
dicc_claves[usuario1] = clave_usuario1
dicc_claves[usuario2] = clave_usuario2
dicc_claves[usuario3] = clave_usuario3
# se borra el contenido anterior del fichero log del servidor proxy
fichero=open(ruta_log_proxy,'w')
fichero.close()
#se borra el contenido de la base de datos de usuarios registrados del servidor proxy
fichero=open(ruta_base_usuarios,'w')
fichero.close()

#se lanza el servidor
serv = SocketServer.UDPServer((IP_proxy,puerto_proxy), EchoProxyHandler)
print "Lanzando el servidor UDP " + nombre_proxy
serv.serve_forever()





