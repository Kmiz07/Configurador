
import configuracion,gc,network,utime,usocket
from machine import Pin
piloto = 2#pin del led rojo para esp32cam usar pin 33,  para esp32 comun usar pin2
invertir = False # si precisamos invertir pin para el encendido.
tiempo_espera = 15 #tiempo que probara de conectar al router

def crea_pagina(valores):
    pagina = '<html>\r\n<head>\r\n</head>\r\n<body>\r\n<form action="configura.html" method="post">\r\n<ul>'
    for k in valores:
        pagina += '\r\n<li>\r\n'
        pagina +='<label for="' + k + '">'+ k +':</label>'
        pagina += '<input type="text" id="' + k +'" name="' + k + '" value="' + valores[k] + '" size="60">\r\n<li/>'
    pagina += '<li class="button">\r\n<button type="submit">Actualizar</button></li>'
    pagina += '\r\n<ul/>\r\n<form/>\r\n</body>\r\n</html>'
    cabecera ='HTTP/1.1 200 OK\r\nContent-Type: text/html \r\nContent-Lengh: ' +str(len(pagina)) +' \r\nConnection: keep-alive\r\n\r\n'
    cabecera += pagina
    return cabecera  
    

                    
def main():
   
#conectamos a wifi segun configuracion en datos.dat
    configuracion.convertir()
    indice = 0
    wlan = network.WLAN(network.STA_IF)
    aplan = network.WLAN(network.AP_IF)
    aplan.active(False)
    wlan.active(True)
# si forzar es True, se forzara el ip al determinado en datos.dat, sino se utilizara el que determine el router.
    if configuracion.forzar == True:
        wlan.ifconfig(configuracion.ST_CONF)
    tiempo = utime.time()
    wlan.connect(configuracion.ST_SSID,configuracion.ST_PASSW)
    while not wlan.isconnected():            
        if utime.time()-tiempo_espera > tiempo:
            break           
    if wlan.isconnected():
        msg_inicio= "conectado como ST en: "+ str(wlan.ifconfig()[0])   
        print(msg_inicio)
#--------------------------------------------------------------
#Aqui llamariamos a la funcion o modulo principal del programa.
#--------------------------------------------------------------
        print('fin del programa. todo ok')#y eliminar esta linea.


#Cuando falla sta se crea un ap y se debe conectar en el y en un navegador enviar: [192.168.4.1/<SSID>,<PASSW>]
#el chip se reseteara con la nueva configuracion, y si no es correcta, volvera al ap de nuevo para reconfigurar.
    
    else:        
        tipo=[]
        motivo=[]
        valores=configuracion.lee()
        pagina= crea_pagina(valores)
        wlan.active(False)
        aplan.active(True)
        aplan.ifconfig(configuracion.AP_CONF)                
        aplan.config(essid = configuracion.AP_SSID, password = configuracion.AP_PASSW)
        print("Conectado como AP en:",aplan.ifconfig())
        p0 = Pin(piloto, Pin.OUT)
        if invertir :
            p0.value(0)
        else:
            p0.value(1)
        confserv = ("",80)
        serv_socket = usocket.socket()
        serv_socket.bind(confserv)
        serv_socket.listen(1)
        while True:
            conn, addr = serv_socket.accept()
            recepcion=''
            datos=''
            datos = conn.readline()
            while datos != b'':
                recepcion += (datos.decode())
                datos = conn.readline()
                if datos == b'\r\n':
                    break
            if recepcion != '':
                lineas = recepcion.splitlines()
                nombres = lineas[0].split(' ')
                tipo=nombres[0]#'GET' o 'POST' 
                motivo=nombres[1]# '/' o 'configura.html'
            else:
                print('no llegaron datos validos')
            a=['GET','/']
            if tipo == 'GET' and motivo =='/':
                conn.sendall(pagina)
                conn.close()
            elif tipo == 'POST' and motivo =='/configura.html':
                for linea in lineas:
                    valores_linea = separa_por_espacios.split(linea)
                    nombre_dato = valores_linea[0]
                    if nombre_dato == 'Content-Length:':
                        longitud = int(valores_linea[1])
                datos = conn.read(longitud).decode()

#         modifica respuestas para poder ingresarlas en el archivo de configuracion
#                 resultados = separa_por_and.split(datos)
                resultados = datos.split('&')
                for resultado in resultados:
                    resultado_ok = resultado.replace("%27","'")
                    resultado = resultado_ok.replace("%5B","[")
                    resultado_ok = resultado.replace("%5D","]")
                    resultado = resultado_ok.replace("%2C",",")
                    resultado_ok = resultado.replace("%3A",":")
                    k,v = resultado_ok.split("=")
                    configuracion.unir(k,v)
                conn.send(b'HTTP/1.1 200 OK\r\nContent-Type: text/html \r\nConnection: close \r\n\r\n<html><body>Cambios realizados</body></html>\r\n\r\n')
                conn.close()
                ahora = utime.time()
                while utime.time() - 5 > ahora:
                    pass
                break
            else:
                conn.send(b'HTTP/1.1 404 Not Found\r\nContent-Type: text/html \r\nConnection: close \r\n\r\n<html><body>Pagina no aceptada</body></html>\r\n\r\n')
                conn.close()
        serv_socket.close()
        if invertir :
            p0.value(1)
        else:
            p0.value(0)
        configuracion.reinicia()
gc.collect()
