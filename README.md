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

3) Por cada letra de la cadena le aplica la siguiente regla: [ ( [(L+Lk+Lki) ^ (Lk*Lki))] % 96 ) * sk1 + sk2 ] % 96.
   Hagamos una pausa acá. Sé que parece bastante confusa, pero les explicaré, no es nada complicado.
