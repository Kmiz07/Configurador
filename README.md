Estos son los scripts que uso para el inicio en mis proyectos con conexion a red.
Existe un archivo 'datos.dat' que incluye un json con la configuracion de conexion, aunque se puede personalizar con cualquier variable o lista que quieras poder configurar en el inicio del programa.
El modo mas correcto de incluir nuevas variables si quieres no tener problemas es utilizando el mismo modulo configuracion.
Cuando estas conectado en modo Repl por serie, si, por ejemplo, quisieras incluir una variable:valor tal que nombre= 'variable', podrias hacerlo escribiendo en la terminal de thonny lo siguiente:

import configuracion

configuracion.unir("nombre", "'variable'")

Para conocer las variables existentes podemos escribir configuracion.lista() y nos listara todas las variables que tenemos en el json.

Podemos eliminar cualquier variable con el comando configuracion.eliminar(clave).
Tambien podremos editar todas las opciones existentes por web cuando iniciemos por AP, pero no podremos crear nuevas ni eliminarlas.
 
Y en el archivo 'datos.dat' se habra incluido en el json esa variable y su valor.
Del mismo modo, en el interior del codigo se podria hacer esto mismo para editar una variable existente o crear una nueva.
Como puedes apreciar, al inicio del modulo wifi.py, se abre el archivo de configuracion y se toman los datos para la conexion.
En caso que los datos de conexion sean incorrectos, pasado el tiempo configurado, (esta configurado a 15 segundos pero se puede modificar) se cerrara la conexion en modo estacion y se abrira una nueva en modo punto de acceso. En el archivo 'datos.dat' viene configurada como SSDI = 'micropython12' y PASSW = 'elpassword'. Deberemos conectar a ese AP y abrir un navegador en 192.168.4.1. Nos enviara un formulario con las opciones de 'datos.dat' para ser editadas. Una vez editadas y al enviar el formulario, el chip se reiniciara y arrancara con la nueva configuracion. Si esta fuera incorrecta deberiamos volver a empezar. 
