# Notelocked

Notelocked es un simple editor para guardar textos cifrados con contraseña, mantiene un aspecto sencillo y una fácil manera de uso, es software libre y multiplataforma (escrito en Python 3)

``` Notelocked is a simple editor to save encrypted texts with a password, it maintains a simple aspect and an easy way of use (writted on Python 3)```

La interfaz de uso está en Ingles porque consideré que es un idioma más usado, aunque parte de la documentación está en inglés y opcionalmente en español.

Aunque si digo simple hablo de aspecto, tiene funcionalidades que lo hacen un programa completo y con características únicas y objetivas para proteger.

El código lo programe minuciosamente y logre algo perfeccionado o muy completo, todo el código es propio y me ha llevado mucho tiempo y he aprendido mucho.

He usado la **librería** por defecto de **Python** para interfaces graficas de **Tkinter** ya que tengo mucha experiencia con esta librería, así que probablemente no hay que complicarse para instalar librerías de interfaz GUI si ya tenemos instalado Tkinter al haber instalado Python.


## Dependencias
Se necesita instalar una libreria de criptografia de Python:
```
pip install pycryptodome
```

## Dependencias opcionales (Windows)
En Windows existe pywin32 y es una librearía para Windows y esta es necesaria si se quiere solucionar el sencillo bug del portapapeles (clipboard) que está presente en tkinter que cuando cerramos el programa nos vacía el portapapeles si hemos copiado un texto en la interfaz gráfica de trabajo.
```
pip install pywin32
```
Al instalar pywin32 el programa usaría win32clipboard como modulo o paquete para intentar solucionar el problema de Tkinter cuando cerramos el programa, usa una función del portapapeles y re-guarda lo que había en el portapapeles, y en una gran mayoría de casos logra resguardar el portapepeles y que este no se borre.


## Uso
Ejecutar **notelocked.py** o también notelocked.pyw (para correr sin la consola)


## Licencia
**Licencia GPLv2 o posterior**

Algunas responsabilidades:  Si se quiere redistribuir el programa es necesario tener en cuenta la licencia, y si también se hace entrega de una librería o dependencia aquellas también tienen su licencia y términos.


# Ejemplos
Algunas imágenes de ejemplo para mostrar el programa:
<div align="center">
<img src="https://user-images.githubusercontent.com/95723749/209721649-18f5a324-6fa2-488b-882f-9c355fa0183d.png">
</div>


## Proteger el contenido:
Se necesita crear una contraseña cuando se guarda el contenido y se guarda cifrado, luego se usará esta contraseña para descifrar y ver o modificar al contenido protegido.

<div align="center">
<img src="https://user-images.githubusercontent.com/95723749/209721930-dc2224ba-0146-4b09-b610-a8644c4886f4.png">
</div>

<div align="center">
<img src="https://user-images.githubusercontent.com/95723749/209724812-5aacb926-1c07-46c3-a342-3746436c20c3.png">
</div>


## Auto bloqueo por inactividad:
Tras descuidar el programa abierto y habiendo creado una contraseña, se cuenta la inactividad, tras cierta inactividad el texto se auto-cifra para que si alguien los quiere ver o modificar necesitará la contraseña actual.

<div align="center">
<img src="https://user-images.githubusercontent.com/95723749/209722045-a4cb6879-5d35-4d96-a8a8-6ae47b20c88f.png">
</div>


## Configurar la visualización
Letras y tamaño estilo de letra, colores, y más. 
Se puede configurar el aspecto y las preferencias de letras, además se puede crear perfiles de colores o elegir otro.

<div align="center">
<img src="https://user-images.githubusercontent.com/95723749/209724562-ad6b0422-7d5f-4189-b4ea-c777512821dd.png">
</div>

<div align="center">
<img src="https://user-images.githubusercontent.com/95723749/209724727-4e093d7b-aaaf-4c90-ad90-636c282cdb2f.png">
</div>


## Sección de Ayuda y datos del programa
El programa también cuenta con documentación: secciones "acerca de", "ayuda", y "licencia".

<div align="center">
<img src="https://user-images.githubusercontent.com/95723749/209725196-9f4299b0-0199-4a49-ba37-669f1b291efc.png">
</div>



## Anegdotas y comentarios
Ha sido mucho trabajo y dedicación, he aprendido mucho, y me ha dolido también en situaciones tener que reparar y corregir cosas o cambiarlas, pero mejoré mi nivel que ya tenía un buen nivel de programación en Python.

Le he dado a este código compatibilidad con muchas versiones de Python3, para programar he usado Python 3 pero en una ocasión me intereso hacer el programa compatible hasta con versiones viejas como Python2 pero resulto muy problemático y cuestionablemente irreparable el modo de codificar y decodificar caracteres raros en Python2, así que he puesto una restricción condicional en el código para que solo corra en versiones Python3x para que así evitar problemas, aunque así le ha quedado al código buenos arreglos para que no se dependa de versiones especificas ya que he probado en muchos casos si una determinada función o método existía en versiones anteriores de Python moderno y he perseguido alternativas para guardar compatibilidad con muchas versiones de Python 3.

No llegaba el día de publicarlo y como grandes proyectos que no he publicado, no he querido que este sea el caso, así que me he tomado el esfuerzo de terminarlo y cumplir con esta publicación. Y aunque este no es el proyecto mas grande o que mas me ha costado, quizás he aprendido mucho y diría que es uno de los proyectos que mas me enseño.
Algunos aspectos visuales en Tkinter, muchos, los he ensamblado con código y mucha lógica porque no existían, y sé que a algún gran experto le puede parecer "solo un programa bonito" porque está hecho en Python, pero he inventado todas las ventanas, y muchos sistemas que no los saque ninguno prediseñado de ningún sitio o trabajo ajeno.

Espero seguir arreglándolo si es necesario arreglar ciertas cosas y mantenerlo evolucionando.

Att: Leonardo

</br></br>

Actualizaciones importantes de versiones:
=================================
Se han introducido algunos cambios técnicos e importantes en las versiones, los cambios importantes son sobre el formato del archivo y por lo tanto los nuevos archivos cambian a nueva versión. Al actualizar la versión y formato he conseguido que el programa logre ser compatible también con las versiones antiguas de archivos gracias a que los archivos guardados tienen un metadato donde indica su versión y de esta forma los archivos antiguos no quedan deprecados. **Para actualizar un archivo a una nueva versión solo es necesario: actualizar el programa, abrir tal archivo y volverlo a guardar**.


</br>

- ## Cambios en versión v0.6
 
 Anteriormente la versión v0.5 calculaba una **integridad del cifrado** usando un hash derivado de (password+cifrado) concatenados.
 Se actualizo ese calculo tomando otros datos que componen el proceso de cifrado: (password+vector+cifrado) concatenados.
 De esta forma se calcula si el cifrado fue modificado por otros desde el archivo y se avisa al usuario con una advertencia. Pero a este cálculo ya no lo llamamos integridad dado que la documentación de cifrado por bloques dice que este cifrado no garantiza integridad, por este motivo este cálculo es una invención pero es más o menos la misma intención.

 </br>

- ## Cambios en versión v0.7


 **Cambios en el cifrado**, anteriormente la versión v0.5 y v0.6 usaba directamente una password de texto plano y con relleno para el cifrado, lo cual si bien es un cifrado seguro al pedir una longitud de 12 hasta 32.

 Ahora a partir de v0.7 usa una clave derivada de esa password plana y lo que se hace es:

 Calcular un hash sha256 de esa password plana, el resultado es 32bytes unicode y a partir de esos 32bytes más el password concatenado genera otro hash de 32bytes unicode y estos bytes se usan en el cifrado:
 
 
```
plainPassword = b"a password secret";
hashPublic = sha256(plainPassword).digest(); #32bytes
keySecretCipher = sha256(plainPassword+hashPublic).digest(); #32bytes
```

Aunque en v0.6 su cifrado es seguro, ahora en v0.7 queda más claro y puede ser más seguro ya que la password de entrada no necesitará límites de longitud o que necesariamente sean de caracteres ASCII. Las contraseñas/passwords creadas podran ahora tener una longitud de 12 a 64 caracteres, pero el programa continuará exigiendo contraseñas en ASCII para evitar cualquier problema de falso tipeo equivocado.
