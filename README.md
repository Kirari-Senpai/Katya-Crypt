# Katya-Crypt

Katya es un algoritmo de cifrado simétrico simple desarrollado en Python.

## Funcionamiento general

El funcionamiento de dicho algoritmo se puede explicar de una manera sencilla:

### Cifrado 

#### Establecer abecederio (o como quieran llamarlo)

Este deberá contar con una longitud de 96 carácteres distintos (por defecto ya tiene un orden):

```
 "a","b","c","d","e","f","g","h","i","j","k","l","m","n","ñ","o","p","q","r","s","t","u","v","w","x","y","z",
 "A","B","C","D","E","F","G","H","I","J","K","L","M","N","Ñ","O","P","Q","R","S","T","U","V","W","X","Y","Z",
 "0","1","2","3","4","5","6","7","8","9","!","\"","#","$","%","&","'","(",")","*","+","´","-",".","/",":",";",
 "<","=",">","@","[","\\","]","^","_","`","{","|","}","~","?"
```

#### Se recorre la cadena

Cada letra será transformada a su respectivo entero en Ascii.

#### Aplicar regla a cada entero

Por cada letra de la cadena se le aplica la siguiente regla: [ ( [(L+Lk+Lki) ^ (Lk*Lki))] % 96 ) * sk1 + sk2 ] % 96.
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
   
Bueno, con el fin de hacer sencillas las cosas, usaremos una variable llamada *resultado* como muestra. Básicamente:
   
a) Se suman los valores enteros de cada carácter de la cadena, contraseña y contraseña invertida. (Se almacena en *resultado*)<br>
b) Se realiza el producto del carácter de la contraseña con el de la invertida, creemos una variable temp. (temp = Lk * Lki)<br>
c) Luego, al *resultado* se le aplica el <a href="https://en.wikipedia.org/wiki/Exclusive_or">operador XOR</a>. (Se almacena en *resultado* = *resultado* ^ temp)<br>
d) Al terminar el proceso, se realiza el módulo entre el resultado y 96. (Se almacena en *resultado* = *resultado* mod 96)<br>
e) Después a este *resultado* se le multiplica la subclave (sk1: coprimo con 96). (*resultado* = *resultado* * sk1)<br>
f) Luego, al mismo se le suma la subclave 2 (sk2: desplazamiento de cadena). (*resultado* = *resultado* + sk2)<br>
g) Como paso final, al *resultado* se le aplica módulo de 96 nuevamente. (*resultado* = *resultado* mod 96)

Vieron que es bastante simple? :D

#### Convertir enteros a letras

Una vez que finaliza el paso anterior, directamente cada entero se asocia con un elemento del abecedario. Ejemplo:

```
94 29 24 2 35 20 13 27 72 12 87 72 79 50 20 21 7 26 3 41 54 13 75 14 94 83 84 2 6 79 74

```

Se transforma a:

```
~ C x c I t n A ) m ] ) : W t u h z d Ñ 0 n ´ ñ ~ > @ c g : +
```

Claro, además de esos carácteres, se añadirán extras, que son los cocientes calculados de cada letra del paso *d*. Estos nos sirven para luego poder descifrarlos. Entonces, agregando estos a la cadena, quedan así:

```
¡bcd¿~¡bdc¿C¡bbg¿x¡bdg¿c¡jg¿I¡bdh¿t¡bbh¿n¡bdc¿A¡bcc¿)¡bcc¿m¡bcb¿]¡bcc¿)¡bdc¿:¡bbg¿W¡bdg¿t¡bab¿u¡bdg¿h¡bbg¿z¡bdc¿d¡bcd¿Ñ¡bcb¿0¡bcc¿n¡bcc¿´¡bdc¿ñ¡bbc¿~¡bdg¿>¡baa¿@¡bdg¿c¡bbh¿g¡bdc¿:¡bcd¿+
```

### Descifrado

#### Establecer abecederio

Se setea el abecedario con el que que se cifraron los mensajes. 

#### Limpieza de cadena cifrada

Se toma la cadena cifrada en crudo y se divide el respectivo string. La primera parte con los divisores y la segunda con la cadena completa.

```
([115, 115, 121, 134, 134, 135, 134, 121, 115, 115], +q;ValR+Lq)
```

#### Autocomplementar el key con longitud de cadena

```
+q;ValR+Lq
passwordpa
```

#### Se recorre la cadena cifrada

Cada letra se transformará a su respectivo entero perteneciente al ABC.

```
+q;ValR+Lq
74 17 80 49 0 11 45 74 38 17
```

#### Aplicar regla a cada entero

Por cada entero la cadena se le aplica la siguiente regla: [ [(96*coc + (a^-1) * (Lc-sk2))%96] ^ [Lk*Lki] ] - Lk - Lki

Los variables y sus descripciones son:

```
   Coc: cociente calculado 
   a^-1: inversa del modulo calculado
   Lc: letra cifrada
   Lk: letra de la contraseña
   Lki: letra de la contraseña (invertida)
   sk2: subclave 2
   
```

En esta etapa también usaremos la misma variable llamada *resultado* como muestra. En principio:

a) Debemos calcular el inverso modular a partir del coprimo y desplazamiento seleccionado en la etapa de cifrado. (*resultado* = ).

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
import katya
```

Creamos el objeto katya:

```
katya = katya.Katya()
```

Establecemos el abecedario:

```
katya.set_ABC()
```

<b>Nota: </b>por defecto el valor del método está en 0, por lo que si desea crear un ABC personalizado, entonces deberá pasarle una lista con una longitud de 96 elementos.

Ahora que tenemos todo preparado, empezaremos con el proceso de cifrado.

### Cifrado

Para encriptar un mensaje, usaremos el método encrypt:

```
msg = katya.encrypt("Hola Mundo","katya_pass")
```

Salida:

```
¿bda¡.¿bbd¡|¿bbf¡m¿bed¡u¿jd¡A¿jc¡*¿bed¡]¿bbf¡o¿bbf¡+¿bda¡K
```

### Descifrado

Para desencriptar el mensaje, usaremos el método decrypt:

```
msg = katya.decrypt("¿bda¡.¿bbd¡|¿bbf¡m¿bed¡u¿jd¡A¿jc¡*¿bed¡]¿bbf¡o¿bbf¡+¿bda¡K","katya_pass",katya.iv)
```

Salida:

```
Hola Mundo
```

## Necesito más seguridad, es posible?

Por supuesto! Con el método random_ABC() alterarás el orden original del alfabeto, por lo que darás más dificultad al atacante para saber cuál es el orden correcto. De modo que al individuo que intenta desencriptar el mensaje, no le servirá de nada obtener la contraseña si no sabe el orden de los elementos.

La salida del mismo es la semilla, es decir, el número en el cual estará ordenado tu ABC.

Salida:
```
>>> katya.random_ABC()
57
>>> katya.ABC
['h', ')', 'p', '4', 'k', '9', 'm', 'A', '*', 'j', 'L', 'P', 'g', '\\', '$', 'Q', 'X', '2', 'Y', ']', 'e', '?', '^', '3', 'Z', 'i', 'E', '5', 't', 'D', 'l', '!', 'H', 'V', ';', 'R', 'I', '/', '=', '6', 'S', '@', 'M', 'd', 'x', 'b', '-', 'C', 'N', 'a', '`', 'z', '}', 'O', 'y', '%', '_', 'o', 'ñ', '(', 'G', 'J', 'w', '[', 'v', '0', 's', ':', "'", 'r', 'q', 'F', '&', '8', '+', 'n', 'W', '>', '~', '|', '#', 'u', '{', 'U', '<', '1', 'K', '7', 'Ñ', '"', 'B', 'c', '.', '´', 'T', 'f']
```

## Requerimientos

Python 3.5 o superior
