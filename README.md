# Katya-Crypt

Katya es un algoritmo de cifrado simétrico simple desarrollado en Python.

## Funcionamiento general

El funcionamiento de dicho algoritmo se puede explicar de una manera sencilla:

1) Se establece un abecedario o como quieran llamarlo. Este deberá contar con una longitud de 96 carácteres distintos (por defecto ya tiene un orden):

```
 "a","b","c","d","e","f","g","h","i","j","k","l","m","n","ñ","o","p","q","r","s","t","u","v","w","x","y","z",
 "A","B","C","D","E","F","G","H","I","J","K","L","M","N","Ñ","O","P","Q","R","S","T","U","V","W","X","Y","Z",
 "0","1","2","3","4","5","6","7","8","9","!","\"","#","$","%","&","'","(",")","*","+","´","-",".","/",":",";",
 "<","=",">","@","[","\\","]","^","_","`","{","|","}","~","?"
```

2) Se recorre la cadena.

3) Por cada letra de la cadena se le aplica la siguiente regla: [ ( [(L+Lk+Lki) ^ (Lk*Lki))] % 96 ) * sk1 + sk2 ] % 96.
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
   
   Bueno, básicamente:
   
   a. Se suman los valores enteros de cada carácter de la cadena, contraseña y contraseña invertida.
   b. Se realiza el producto del carácter de la contraseña con el de la invertida.
   c. Luego que se tiene la suma y el producto de los pasos anteriores, se le aplica el <a href="https://en.wikipedia.org/wiki/Exclusive_or">operador XOR</a>
