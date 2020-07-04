#!/usr/bin/python3

import random
import collections

from math import gcd as coprime
from sympy.core.numbers import igcdex as inverse


# Excepciones personalizadas

class ABCException(Exception):
	pass

class ABCNotEstablished(ABCException):
	pass

class ABCInvalid(ABCException):
	pass

class ShiftException(Exception):
	pass

class ShiftInvalid(ShiftException):
	pass

class SubkeysError(Exception):
	pass


SPECIAL_NUMBER = 96	


# Formula de cifrado Katya: [ ( [(L+Lk+Lki) ^ (Lk*Lki))] % 96 ) * sk1 + sk2 ] % 96 
# Formula de descifrado Katya: [ [(96*Coc + (a^-1) * (Lc-sk2))%96] ^ [Lk*Lki] ] - Lk - Lki


class Cipher:

	def __init__ (self):

		self.ABC = None
		self.seed_ = 0
		self.subkey1,self.subkey2 = (1,1)


	# FUNCIONES OCULTAS

	def __clear_string(self,string):

		""" 

		Devuelve una tupla de los cocientes de cada letra del mensaje cifrado 
		y la cadena cifrada modificada.
		
		Parametros -> string: cadena cifrada (ejemplo) ¿bbf¡+¿bbf¡q¿bcb¡;¿bde¡V¿bde¡a¿bdf¡l¿bde¡R¿bcb¡+¿bbf¡L¿bbf¡q

		Salida: ([115,115,121,134,134,135,134,121,115,115],"+q;ValR+Lq;") 

		"""

		quotients = []
		new_string = ""

		blocks = [tuple(i.split('¡')) for i in string.split("¿") if len(i)!=0]

		for block in blocks:
				
			quotient = ""

			for chunk in block[0]:

				quotient += str(self.ABC.index(chunk))

			quotients.append(int(quotient))	
			new_string += block[1]

		return (quotients,new_string)


	def __key_complete(self,raw_string,key):

		"""

		Devuelve la key con la longitud de la cadena a cifrar.

		Parametros -> raw_string: cadena no cifrada (ejemplo) Hola Mundo
		              key: llave para cifrar (ejemplo) key

		Salida: keykeykeyk

		"""

		new_key = ""

		if (len(key)<=len(raw_string)):

			while (len(new_key)<len(raw_string)):
				new_key += key
			
			if (len(new_key)>len(raw_string)):
				new_key = new_key[:len(raw_string)]

		else:

			new_key = key[:len(raw_string)]

		return new_key



	def __shifts(self,generic_list,num):

		"""

		Devuelve una lista con los trozos de mensaje alterados.

		Parametros -> generic_list: lista a trozos de mensaje (ejemplo) ["Hola","Mundo!","Es","la","hora."]
		              num: desplazamientos de los elementos de la lista (ejemplo) 3

		Salida: ["Es","la","hora.","Hola","Mundo!"]

		"""

		generic = collections.deque(generic_list)
		generic.rotate(num)

		generic_list = list(generic)

		return generic_list



	# FUNCIONES PARA MANIPULACION DE SUBCLAVES

	def subkeys(self,a=1,b=1):

		"""

		Devuelve una tupla con las dos subclaves para cifrar el mensaje. Tales
		son un numero coprimo y el otro un desplazamiento.

		Parametros -> a: numero coprimo (ejemplo) 1
		              b: numero de desplazamiento (ejemplo) 1

		Salida: (1,1)

		"""

		if (isinstance(a,int) and isinstance(b,int)) and ((a>0 and a<=SPECIAL_NUMBER) and (b>0 and b<=SPECIAL_NUMBER)) and (coprime(a,SPECIAL_NUMBER)==1):
			self.subkey1,self.subkey2 = (a,b)

		else:
			raise SubkeysError('Failed to set subkeys')

		return (self.subkey1,self.subkey2)


	def show_possible_subkeys(self):

		"""

		Devuelve las posibles subclaves (numeros coprimos) que se podran utilizar.

		"""

		subkeys_ = []

		a,b = (1,SPECIAL_NUMBER)

		for i in range(a,b+1):
			if (coprime(i,b)==1):
				subkeys_.append(i)

		return subkeys_


	# FUNCIONES PARA EL LENGUAJE

	def set_ABC(self,abc=0):

		"""

		Devuleve el abecedario que se utilizara para cifrar el mensaje.

		Parametros -> abc: establecer abecedario (por defecto 0)

		Se puede establecer un abecedario personalizado, solo debe cumplir las
		siguientes reestricciones:

		- abc tiene que ser una lista
		- abc debe ser de longitud 96

		"""

		if (isinstance(abc,list)) and (len(abc)==SPECIAL_NUMBER) and (abc!=0):

			self.ABC = abc

		elif (abc==0):

			self.ABC = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","ñ","o","p","q","r","s","t","u","v","w","x","y","z",
			            "A","B","C","D","E","F","G","H","I","J","K","L","M","N","Ñ","O","P","Q","R","S","T","U","V","W","X","Y","Z",
			            "0","1","2","3","4","5","6","7","8","9","!","\"","#","$","%","&","'","(",")","*","+","´","-",".","/",
			            ":",";","<","=",">","@","[","\\","]","^","_","`","{","|","}","~","?"]


		else:
			
			raise ABCInvalid("ABC Invalid")

		return self.ABC


	def random_ABC(self):

		"""

		Devuelve un entero que indica el orden en el que se encuentra el ABC, luego
		de haber sido alterado aleatoriamente.

		Se utiliza un numero aleatorio y a traves del metodo __shifts() se realiza 
		el desplazamiento con tal numero. Hay que considerar que si pierde el numero
		de orden o semilla entonces no podra recuperar la informacion al momento de
		querer descifrarla.

		"""

		if (self.ABC!=None):

			self.set_ABC(0)

			num = random.randint(0,SPECIAL_NUMBER-1)

			self.ABC = self.__shifts(self.ABC,num)

			self.seed_ = num

		else:

			raise ABCNotEstablished("ABC not established")

		return self.seed_


	def set_seed(self,integer=0):

		"""

		Devuelve un entero que indica el orden en el que se encuentra el ABC, luego
		de haber sido alterado manualmente.

		Parametros -> integer: entero que sera el desplazamiento para alterar el orden del ABC.
		                       Por defecto se encuentra en 0.

		Al igual que el metodo random_ABC(), hay que considerar que si pierde el numero
		de orden o semilla entonces no podra recuperar la informacion al momento de
		querer descifrarla.

		"""

		if (isinstance(integer,int)) and (integer<=SPECIAL_NUMBER-1 and integer>0):

			self.set_ABC(0)

			self.ABC = self.__shifts(self.ABC,integer)

			self.seed_ = integer

		elif (isinstance(integer,int)) and (integer>SPECIAL_NUMBER-1 or integer<0):

			raise ShiftInvalid("Seed is not in the range (0-95)")

		return self.seed_


	# FUNCIONES PARA MODIFICAR MENSAJE

	def __build_matrix(self,raw_string,long_key):

		"""

		Devuelve una lista con trozos de mensaje con longitud contraseña.

		Parametros -> raw_string: (ejemplo) Hola Mundo
		              long_key: entero (ejemplo) 3

		Salida: ["Hol","a M","und","o"]

		"""

		matrix = [raw_string[i:i+long_key] for i in range(0,len(raw_string),long_key)]

		return matrix

	def __modify_msg(self,raw_string,key,shift):

		"""

		Devuelve la cadena alterada. 

		A traves de los metodos de __build_matrix() y __shifts() para dividir la cadena en crudo
		en trozos y luego utilizar desplazamientos para alterar la cadena original.

		Parametros -> raw_string: cadena en crudo
		              key: contraseña
		              shift: desplazamiento

		"""

		if (shift!=0) and (shift<=len(key) and shift>0):
			matrix = self.__build_matrix(raw_string,len(key))
			return ''.join(self.__shifts(matrix,shift))

		elif (shift!=0) and (shift>len(key) or shift<0):
			raise ShiftException("Displacement does not meet desired length")

		else:
			return 0


	# FUNCIONES PARA CIFRADO Y DESCIFRADO

	def encrypt(self,raw_string,key,string_shift=0):

		"""

		Devuelve cadena cifrada.

		Parametros -> raw_string: cadena en crudo (ejemplo) Hola Mundo
		              key: contraseña para cifrar (ejemplo) key
		              string_shift: entero para desplazamientos (alteracion de cadena) (ejemplo) 3

		Salida: ¿bcb¡T¿bcg¡e¿bce¡w¿bcc¡X¿bcf¡r¿bcf¡F¿bcc¡7¿bce¡B¿bcf¡q¿bcc¡6

		"""
		
		# Modificar cadena
		if (string_shift!=0):
			raw_string = self.__modify_msg(raw_string,key,string_shift)

		# Completar key
		key = self.__key_complete(raw_string,key)

		# Asignar subclaves
		sk1,sk2 = self.subkey1,self.subkey2

		text = [] 

		if (self.ABC!=None):

			for i in range(len(raw_string)):

				# Calculo de cifrado 1
				calc = ( (ord(raw_string[i]) + ord(key[i]) + ord(key[::-1][i])) ^ (ord(key[i])*ord(key[::-1][i])) )

				# Obetener cociente y convertirlo en un caracter del ABC
				quotient = ''.join([self.ABC[int(i)] for i in str(calc//SPECIAL_NUMBER)])

				# Calculo de cifrado 2
				chr_n = ( (calc%SPECIAL_NUMBER) * sk1 + sk2 ) % SPECIAL_NUMBER 


				text.append("¿"+quotient+"¡"+self.ABC[chr_n])

		else:

			raise ABCNotEstablished("ABC not established")

		return ''.join(text)


	def decrypt(self,raw_string,key,order=0,string_shift=0,subkey1=1,subkey2=1):

		"""

		Devuelve cadena descifrada.

		Parametros -> raw_string: cadena a descifrar (ejemplo) ¿bcb¡T¿bcg¡e¿bce¡w¿bcc¡X¿bcf¡r¿bcf¡F¿bcc¡7¿bce¡B¿bcf¡q¿bcc¡6
		              key: contraseña para descifrar (ejemplo) key
		              order: numero de orden del ABC (por defecto 0)
		              subkey1: numero coprimo utilizado (por defecto 1)
		              subkey2: numero desplazamiento en ABC (por defecto 1)

		Salida: 

		"""

		# Ordenar ABC
		self.ABC = self.set_ABC(order)

		# Obtener cadena modificada y cocientes
		quotients,string = self.__clear_string(raw_string)

		key = self.__key_complete(string,key)

		decrypt = [] 

		if (self.ABC!=None):

			for i in range(len(string)):

				# Obtener entero de la letra cifrada
				n_letter = self.ABC.index(string[i])

				# Calculo de descifrado
				calc = ((SPECIAL_NUMBER*quotients[i] +((inverse(subkey1,SPECIAL_NUMBER)[0]*(n_letter-subkey2))%SPECIAL_NUMBER)) ^ (ord(key[i])*ord(key[::-1][i]))) - ord(key[i]) - ord(key[::-1][i])

				try:
					decrypt.append(chr(calc))
				except ValueError:
					# Si hay caracteres inexistentes, seleccionarlos al azar
					decrypt.append(chr(random.randint(33,126)))

		else:

			raise ABCNotEstablished("ABC not established")

		# Reacomodar la cadena
		decrypt = self.__shifts(decrypt,string_shift)

		return ''.join(decrypt)