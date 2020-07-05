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
