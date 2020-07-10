
# Katya-Crypt

Katya es un algoritmo de cifrado simétrico simple desarrollado en Python.

## Funcionamiento general

El funcionamiento de dicho algoritmo se puede explicar de una manera sencilla:

### Cifrado 

En el transcurso de todo este proceso, utilizaremos la cadena y contraseña: 

    Hola Mundo         # Cadena
    katya              # Contraseña

Esto con el fin de que se entienda mejor la explicación. Sin más que añadir, comencemos con el primer paso.

#### Establecer abecedario (o como quieran llamarlo)

Este deberá contar con una longitud de 91 caracteres distintos (por defecto ya tiene un orden):

```
'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 
'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 
'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '!', '#', '$', '%', '&', '(', ')', '*', '+', '´', '-', '.', '/', ':', ';', '<', 
'=', '>', '@', '[', ']', '^', '_', '`', '{', '|', '}', '~', '?'
```

#### Autocompletar la contraseña con longitud de cadena

```
Hola Mundo
katyakatya
```

#### Aplicar modo de operación CBC

![enter image description here](https://upload.wikimedia.org/wikipedia/commons/d/d3/Cbc_encryption.png)

Si no sabe que es el modo CBC, [haga click aquí](https://es.wikipedia.org/wiki/Modos_de_operaci%C3%B3n_de_una_unidad_de_cifrado_por_bloques).

**Nota1:** la versión que se implementó en este cifrado es más simplificada y simple. <br>
 **Nota2:** el IV y los bloques deben ser de longitud contraseña.<br>
 **Nota3:** el IV por defecto es generado automáticamente, pero también lo puede establecer usted. Guardelo de manera segura, lo usará en el proceso de descifrado. 

#### Proceso *Block Cipher Encryption*

Cada carácter (ya con XOR aplicado con el IV) de ese bloque, será transformado a su respectivo entero.

Por cada letra de la cadena se le aplica la siguiente regla:

![](https://i.imgur.com/RhSHT2q.png)

Hagamos una pausa. Sé que parece bastante confusa, pero les explicaré, no es nada complicado.
   
Los variables y sus descripciones son:
```
   L: letra en crudo
   Lk: letra de la contraseña
   Lki: letra de la contraseña (invertida)
   sk1: subclave 1
   sk2: subclave 2
```
   
Bien. ¿Pero que quiere decir esta regla? 
   
Bueno, con el fin de hacer sencillas las cosas, usaremos una variable llamada *resultado* y enteros de los caracteres "H", "k" y "a", que corresponden a la cadena, contraseña y contraseña invertida:

>     Hola Mundo         # Cadena
>     katya              # Contraseña

**Nota:** la contraseña invertida seria así -> aytak (de ahí viene el carácter "a" seleccionado)  <br>
**Advertencia:** a pesar de que este ejemplo está hecho con el carácter de la cadena original, en el proceso BCE (Block Cipher Encryption), se usa el carácter transformado por la operación XOR con el IV y la cadena. Pero para no confundir mucho, directamente se mostrará el ejemplo con el entero del carácter original.  

<br>

Los valores de las mismos son *(L=72,Lk=107,Lki=97,sk1=1,sk2=1)*. Entonces básicamente:

**a)** Se suman los valores enteros de cada carácter de la cadena, contraseña y contraseña invertida:

![enter image description here](https://i.imgur.com/lqdOc61.png)

**b)** Se realiza el producto del carácter de la contraseña con el de la invertida, para luego aplicar el [operador XOR](https://en.wikipedia.org/wiki/Exclusive_or) con el resultado obtenido anteriormente:

![enter image description here](https://i.imgur.com/njNjrvj.png)

**c)** Al terminar el proceso, se realiza el módulo entre el resultado y 91 (cantidad de elementos del ABC):

![enter image description here](https://i.imgur.com/e4UUt3X.png)

**d)** Después a este *resultado* se le multiplica la subclave 1 (sk1: número coprimo con 91):

![enter image description here](https://i.imgur.com/I95eG21.png)

**e)** Luego, al mismo se le suma la subclave 2 (sk2: desplazamiento de cadena):

![enter image description here](https://i.imgur.com/fPJC6X2.png)

**f)** Como paso final, al *resultado* obtenido se le calcula, nuevamente, el módulo de 91 (en este caso el resto es el mismo):

![enter image description here](https://i.imgur.com/UKIKMbR.png)

Y listo, ya tendríamos el primer carácter ya cifrado. Vieron que es bastante simple? :D

#### Convertir enteros a caracteres

Una vez que finaliza el proceso de *Block Cipher Encryption*, directamente cada entero se asocia con un elemento del abecedario. Ejemplo:

```
14 10 58 88 62 71 88 41 89 57
```

Se transforma a:

```
ok6}!´}P~5
```

Claro, además de esos caracteres, se añadirán extras, que son los cocientes calculados de cada carácter del **paso c de Block Cipher Encryption**. Estos nos sirven para luego poder descifrarlos. Entonces, agregando estos a la cadena, quedan así:

```
¿bbh¡o¿bcg¡k¿bfa¡6¿bcf¡}¿bbd¡!¿bbd¡´¿bcf¡}¿bfb¡P¿bcg¡~¿bbh¡5
```

### Descifrado

#### Establecer abecedario

Se establece el abecedario con el que que se cifraron los mensajes.  

#### Limpieza de cadena cifrada

Se toma la cadena cifrada en crudo: 

> ¿bbh¡o¿bcg¡k¿bfa¡6¿bcf¡}¿bbd¡!¿bbd¡´¿bcf¡}¿bfb¡P¿bcg¡~¿bbh¡5

Se divide el respectivo string. La primera parte con los cocientes de cada carácter y la segunda con la cadena cifrada original sin extras.
```
(["bbh","bcg","bfa","bcf","bbd","bbd","bcf","bfb","bcg","bbh"], ok6}!´}P~5) -> Forma genérica
([117, 126, 150, 125, 113, 113, 125, 151, 126, 117], ok6}!´}P~5)
```

#### Autocomplementar el key con longitud de cadena

```
ok6}!´}P~5
katyakatya
```

#### Se recorre la cadena cifrada

Cada carácter se transformará a su respectivo entero perteneciente al ABC.

```
ok6}!´}P~5
14 10 58 88 62 71 88 41 89 57
```

#### Proceso *Block Cipher Encryption* inverso

Por cada entero la cadena se le aplica la siguiente regla:

![enter image description here](https://i.imgur.com/DXLpF7c.png)

Los variables y sus descripciones son:

```
   C: cociente calculado 
   a⁻¹: inverso multiplicativo (aritmética modular)
   Lc: letra cifrada
   Lk: letra de la contraseña
   Lki: letra de la contraseña (invertida)
   sk2: subclave 2
   
```

En esta etapa descifraremos el carácter que mostramos en el proceso de cifrado. En principio:

**a)** Debemos calcular el  número que nos dio en el **paso c** del cifrado:

![enter image description here](https://i.imgur.com/yPcowKA.png)

 **b)** Luego al resultado se le sumará el producto entre el cociente calculado (**paso c de cifrado** -> resultado / 91) y el 91:

![enter image description here](https://i.imgur.com/7OAYIoo.png)

**c)** Se realiza la operación XOR entre el resultado y el producto entre el entero del carácter de la contraseña y la invertida:

![enter image description here](https://i.imgur.com/VcwU0JV.png)

**d)** Por último, se le resta al resultado el número del carácter de la contraseña y luego la de la invertida:

![enter image description here](https://i.imgur.com/lRgLn9q.png)

Al transformarlo a carácter, vemos que es la "H".

**Nota:** aclaro de nuevo que acá utilizamos el mismo ejemplo que en la etapa de cifrado, con la diferencia que lo vamos a desencriptar. Esto es para mostrar el funcionamiento interno del mismo. 

#### Aplicando nuevamente el CBC pero de manera inversa

![enter image description here](https://upload.wikimedia.org/wikipedia/commons/6/66/Ecb_decryption.png)

En caso que no entiendan esta parte, ya les he dejado un enlace el cual explica el proceso ;) 

#### Muestra final

Una vez que todos los caracteres se hayan descifrado, se mostrará el mensaje:

    Hola Mundo

## Cómo descargar e instalar dependencias?

Para instalar las dependencias, tipeamos lo siguiente:

```
pip install sympy 
```

Como siempre, clonamos el repositorio:

```
git clone https://github.com/Kirari-Senpai/Katya-Crypt.git
cd Katya-Crypt/
```

## Cómo se usa Katya?

Antes que nada importamos el módulo:

```
>>> import katya
```

Creamos el objeto katya:

```
>>> katya = katya.Katya()
```

Establecemos el abecedario:

```
>>> katya.set_ABC()
```

**Nota:** por defecto el valor del método está en 0, por lo que si desea crear un ABC personalizado, entonces deberá pasarle una lista con una longitud de 91 elementos y los mismos no deben estar repetidos.

Ahora que tenemos todo preparado, empezaremos con el proceso de cifrado.

### Cifrado

Para encriptar un mensaje, usaremos el método encrypt:

```
>>> msg = katya.encrypt("Hola Mundo","katya")
```

Salida:

```
¿bbh¡o¿bcg¡k¿bfa¡6¿bcf¡}¿bbd¡!¿bbd¡´¿bcf¡}¿bfb¡P¿bcg¡~¿bbh¡5
```

Al momento de cifrar el mensaje, se generará el IV. Para poder verlo, solo escriba:

```
>>> katya.iv
```


### Descifrado

Para desencriptar el mensaje, usaremos el método decrypt:

```
>>> msg = katya.decrypt("¿bbh¡o¿bcg¡k¿bfa¡6¿bcf¡}¿bbd¡!¿bbd¡´¿bcf¡}¿bfb¡P¿bcg¡~¿bbh¡5","katya",katya.iv)
```

Salida:

```
Hola Mundo
```

## Necesito más seguridad, es posible?

Por supuesto! Hay varios métodos:

### Método random_ABC() y set_seed()

Con el método random_ABC() alterarás el orden original del alfabeto, por lo que darás más dificultad al atacante para saber cuál es el orden correcto. De modo que al individuo que intenta desencriptar el mensaje, no le servirá de nada obtener la contraseña si no sabe el orden de los elementos.

La salida del mismo es la semilla, es decir, el número en el cual estará ordenado tu ABC.

Salida:
```
>>> katya.random_ABC()
68 
>>> katya.ABC
['@', 'N', 'D', 'q', 'u', 'e', 'z', '`', 'k', 'g', 't', 'd', 'T', '2', '|', 'P', 'r', '(', 'c', '_', 'G', '{', '6', '>', 'Z', ';', 'V', ':', '^', 'x', '?', '´', 'A', 'X', '0', ']', 'm', '.', 's', 'M', '5', 'E', '#', ')', 'W', '&', 'K', 'Y', 'j', 'O', 'L', 'b', 'J', '-', 'S', 'i', '!', '~', 'I', 'C', 'B', '1', '[', 'a', '%', 'y', 'w', 'l', 'h', 'R', 'n', '9', '*', 'f', 'p', '=', 'v', 'U', '+', '4', 'Q', 'H', '8', '3', 'F', '/', '<', 'o', '$', '}', '7']
>>> 
```

Lo mismo podemos hacer con el método set_seed(). A diferencia del anterior, este es personalizado:

```
>>> katya.set_seed(10)
10
>>> katya.ABC
['q', '{', ')', '%', '=', '8', 'z', 'g', '-', '_', '<', '5', '4', '/', 's', 'd', 'Z', 'l', '*', '0', '#', '+', 'Y', 'v', 'S', ':', ';', 'M', '`', 'h', 'n', 'o', 'k', 'G', 'O', '>', 'E', 'B', '(', '[', '@', 'V', '^', 'I', '|', 'm', '$', '}', 'a', 'L', 'c', 'y', 'N', 'C', 'p', '3', 'X', 'D', 'i', 'x', 'Q', 't', 'R', 'w', '6', 'H', 'K', '´', 'W', 'T', 'r', '1', 'f', 'U', 'F', 'j', 'P', ']', '&', '~', 'u', 'J', '!', '7', 'A', 'b', '?', '9', '2', 'e', '.']
>>>
```

#### Ejemplo sencillo

```
>>> import katya
>>> 
>>> katya = katya.Katya()
>>> 
>>> katya.set_ABC()
['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'ñ', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'Ñ', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', '´', '-', '.', '/', ':', ';', '<', '=', '>', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~', '?']
>>> 
>>> katya.random_ABC()
64
>>> 
>>> msg = katya.encrypt("Hola Mundo","katya")
>>> 
>>> msg
'¿TT%¡#¿Ty!¡Q¿T9L¡G¿TyY¡3¿TTY¡m¿TTY¡Q¿Ty!¡t¿T9T¡e¿Ty9¡.¿TT%¡s'
>>>
```
Y en efecto, se puede apreciar que la cadena de cifrado no es la misma que mostramos en el ejemplo anterior. Ahora, a descifrar, le pasamos como argumento seed, el valor entero obtenido:

```
>>> msg_decrypt = katya.decrypt(msg,"katya",katya.iv,seed=64)
>>> 
>>> msg_decrypt
'Hola Mundo'
>>>
```
El mismo ejemplo se puede aplicar también para el método set_seed().

**Advertencia:** hay que considerar que si pierde el numero de orden o semilla, entonces, no podrá recuperar la información al momento de querer descifrarla.

### Método subkeys()

Con este método se puede establecer las dos subclaves de las que estábamos hablando antes. Bueno, con la primer subclave estableceremos un número coprimo con 91 y con la segunda un número de desplazamiento para la cadena misma. Veamos un ejemplo sencillo:

```
>>> import katya
>>> 
>>> katya = katya.Katya()
>>> 
>>> katya.set_ABC()
['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'ñ', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'Ñ', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', '´', '-', '.', '/', ':', ';', '<', '=', '>', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~', '?']
>>> 
>>> katya.subkeys(80,10)
(80,10)
>>> 
>>> msg = katya.encrypt("Hola Mundo","katya")
>>> 
>>> msg
'¿bbh¡X¿bcg¡c¿bfa¡u¿bcf¡2¿bbd¡(¿bbd¡7¿bcf¡2¿bfb¡z¿bcg¡R¿bbh¡F'
>>>
```

Vemos que el resultado de cifrado no es el mismo que este:

> ¿bbh¡o¿bcg¡k¿bfa¡6¿bcf¡}¿bbd¡!¿bbd¡´¿bcf¡}¿bfb¡P¿bcg¡~¿bbh¡5

Si no tiene idea que número coprimo utilizar, no se preocupe, no tiene que calcular nada, puede utilizar el método show_possible_subkeys():

```
>>> katya.show_possible_subkeys()
[1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 15, 16, 17, 18, 19, 20, 22, 23, 24, 25, 27, 29, 30, 31, 32, 33, 34, 36, 37, 38, 40, 41, 43, 44, 45, 46, 47, 48, 50, 51, 53, 54, 55, 57, 58, 59, 60, 61, 62, 64, 66, 67, 68, 69, 71, 72, 73, 74, 75, 76, 79, 80, 81, 82, 83, 85, 86, 87, 88, 89, 90]
>>> 
```

Los valores de la subclave 2 debe ser de 1 a 91.

Si bien este último método no es muy seguro, se puede combinar con los métodos anteriores y así mejorar la seguridad. Eso suena bien eh? :o

## :heavy_exclamation_mark: Requerimientos

Python 3.5 o superior

## :octocat: Contribuciones

Todas las contribuciones son bienvenidas! Código, documentación, tutoriales, etc., son bienvenidos. Lo que tenga que ofrecer, ¡lo agradecería! 

## Advertencia 

El mismo está en pleno desarrollo, por lo tanto, puede presentar errores durante su ejecución.
