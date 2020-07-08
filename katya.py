#!/usr/bin/python3

#  _  __   _ _______   ___      ___ _____   _____ _____ 
# | |/ /  /_\_   _\ \ / /_\    / __| _ \ \ / / _ \_   _|
# | ' <  / _ \| |  \ V / _ \  | (__|   /\ V /|  _/ | |  
# |_|\_\/_/ \_\_|   |_/_/ \_\  \___|_|_\ |_| |_|   |_|
#
#                 Created by Kirari

import random
import collections

from math import gcd as coprime
from sympy.core.numbers import igcdex as inverse


# Excepciones personalizadas

class KatyaException(Exception):
	pass

class ABCException(KatyaException):
	pass

class ShiftException(KatyaException):
	pass

class SeedException(KatyaException):
	pass

class SubkeysError(KatyaException):
	pass


SPECIAL_NUMBER = 91	


# Formula de cifrado Katya: [ ( [(L+Lk+Lki) ^ (Lk*Lki))] % 91 ) * sk1 + sk2 ] % 91 

# L: letra en crudo
# Lk: letra de la contraseña
# Lki: letra de la contraseña (invertida)
# sk1: subclave 1
# sk2: subclave 2

# Ejemplo de contraseña invertida: password -> yek



# Formula de descifrado Katya: [ [(91*Coc + (a^-1) * (Lc-sk2))%91] ^ [Lk*Lki] ] - Lk - Lki

# Coc: cociente calculado 
# a^-1: inversa del modulo calculado
# Lc: letra cifrada
# Lk: letra de la contraseña
# Lki: letra de la contraseña (invertida)
# sk2: subclave 2


class Katya:

	def __init__ (self):

		self.ABC = None
		self.seed_ = 0
		self.subkey1,self.subkey2 = (1,1)
		self.iv = None


	# METODOS OCULTOS

	def __clear_string(self,string):

		""" 

		Devuelve una tupla de los cocientes de cada letra del mensaje cifrado 
		y la cadena cifrada modificada.
		
		Parametros -> string: string (ejemplo) ¿bbf¡+¿bbf¡q¿bcb¡;¿bde¡V¿bde¡a¿bdf¡l¿bde¡R¿bcb¡+¿bbf¡L¿bbf¡q

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


	def __password_complete(self,raw_string,password):

		"""

		Devuelve la password con la longitud de la cadena a cifrar.

		Parametros -> raw_string: string (ejemplo) Hola Mundo
		              password: string (ejemplo)   key

		Salida: keykeykeyk

		"""

		new_password = ""

		if (len(password)<=len(raw_string)):

			while (len(new_password)<len(raw_string)):
				new_password += password
			
			if (len(new_password)>len(raw_string)):
				new_password = new_password[:len(raw_string)]

		else:

			new_password = password[:len(raw_string)]

		return new_password


	def __check_password(self,raw_string,raw_passwd):

		""" 
	
		Devuelve password con longitud igual o menor a cadena a encriptar.

		Parametros -> raw_string: string (ejemplo) Hola
		              raw_passwd: string (ejemplo) katya_pass

		salida: katy

		"""

		if (len(raw_passwd)>len(raw_string)):
			raw_passwd = raw_passwd[:-(len(raw_passwd)-len(raw_string))]

		return raw_passwd


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


	def __generate_iv(self,long_password):

		""" Generador de Vector de Inicializacion con longitud contraseña"""

		return ''.join([chr(random.randint(33,126)) for i in range(long_password)])


	# FUNCIONES PARA MANIPULACION DE SUBCLAVES

	def subkeys(self,a=1,b=1):

		"""

		Devuelve una tupla con las dos subclaves para cifrar el mensaje. Tales
		son un numero coprimo y el otro un desplazamiento.

		Parametros -> a: integer coprime (ejemplo) 1
		              b: integer (ejemplo) 1

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

		Parametros -> abc: integer or list (por defecto 0)

		Se puede establecer un abecedario personalizado, solo debe cumplir las
		siguientes reestricciones:

		- abc tiene que ser una lista
		- abc debe ser de longitud 91
		- abc no deber tener caracteres repetidos

		"""

		if (isinstance(abc,list)) and (len(abc)==SPECIAL_NUMBER) and (abc!=0) and (len(abc)==len(set(abc))):

			self.ABC = abc

		elif (abc==0):

			self.ABC = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z",
			            "A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z",
			            "0","1","2","3","4","5","6","7","8","9","!","#","$","%","&","(",")","*","+","´","-",".","/",
			            ":",";","<","=",">","@","[","]","^","_","`","{","|","}","~","?"]


		else:
			
			raise ABCException("ABC Invalid")

		return self.ABC


	def random_ABC(self):

		"""

		Devuelve un entero que indica el orden en el que se encuentra el ABC, luego
		de haber sido alterado aleatoriamente.

		Se utiliza un numero aleatorio y a traves del modulo random altera el ABC. 
		Hay que considerar que si pierde el numero de orden o semilla entonces no 
		podra recuperar la informacion al momento de querer descifrarla.

		"""

		if (self.ABC!=None):

			self.set_ABC(0)

			num = random.randint(0,SPECIAL_NUMBER-1)

			random.Random(num).shuffle(self.ABC)

			self.seed_ = num

		else:

			raise ABCException("ABC not established")

		return self.seed_


	def set_seed(self,integer=0):

		"""

		Devuelve un entero que indica el orden en el que se encuentra el ABC, luego
		de haber sido alterado manualmente.

		Parametros -> integer: entero que servira para alterar el orden del ABC.
		                       Por defecto se encuentra en 0.

		Al igual que el metodo random_ABC(), hay que considerar que si pierde el numero
		de orden o semilla entonces no podra recuperar la informacion al momento de
		querer descifrarla.

		"""

		try:

			if (isinstance(integer,int)) and (integer!=0):

				self.set_ABC(0)

				#self.ABC = self.__shifts(self.ABC,integer)

				random.Random(integer).shuffle(self.ABC)

				self.seed_ = integer

		except SeedException:

			print ("An error occurred while setting seed")

		return self.seed_


	# FUNCIONES PARA MODIFICAR MENSAJE

	def __build_blocks(self,raw_string,len_password):

		"""

		Devuelve una lista con trozos de mensaje con longitud contraseña.

		Parametros -> raw_string: string (ejemplo) Hola Mundo
		              len_password: integer (ejemplo) 4

		Salida: ["Hola"," Mun","do\0\0"]

		Nota: si el ultimo elemento no tiene la misma longitud que la contraseña, 
		      entonces se le agregaran caracteres nulos.

		"""

		matrix = [raw_string[i:i+len_password] for i in range(0,len(raw_string),len_password)]

		if (len(matrix[-1:][0])<len_password):

			matrix[len(matrix)-1] = matrix[-1:][0] + '\0'*(len_password - len(matrix[-1:][0]))

		return matrix


	def __modify_msg(self,raw_string,rotate):

		"""

		Devuelve la cadena alterada. 

		A traves del método __shifts() utiliza desplazamientos 
		para alterar la cadena original.

		Parametros -> raw_string: cadena en crudo
		              rotate: desplazamiento

		"""

		shift,rotate = abs(rotate),rotate

		if (shift!=0) and (shift<=len(raw_string)):
			return ''.join(self.__shifts(list(raw_string),rotate))

		elif (shift!=0) and (shift>len(raw_string)):
			raise ShiftException("Displacement does not meet desired length")

		else:
			return 0


	# FUNCIONES PARA CIFRADO Y DESCIFRADO

	def encrypt(self,raw_string,password,string_shift=0,iv=None):

		"""

		Devuelve cadena cifrada.

		Parametros -> raw_string: string (ejemplo) Hola Mundo
		              password: string (ejemplo) password
		              string_shift: integer (alteracion de cadena) (ejemplo) 3

		Salida: ¿bcb¡T¿bcg¡e¿bce¡w¿bcc¡X¿bcf¡r¿bcf¡F¿bcc¡7¿bce¡B¿bcf¡q¿bcc¡6

		"""
		
		# Modificar cadena
		if (string_shift!=0):
			raw_string = self.__modify_msg(raw_string,string_shift)


		# password en crudo y completado con logitud cadena
		raw_password = self.__check_password(raw_string,password)
		password = self.__password_complete(raw_string,raw_password)

		# Asignar subclaves
		sk1,sk2 = self.subkey1,self.subkey2

		text = [] 

		if (self.ABC!=None):

			# Dividir cadena en crudo en trozos de longitud de clave
			raw_blocks = self.__build_blocks(raw_string,len(raw_password))
			
			# Generar Vector de Inicializacion (IV)
			if (iv==None):
				self.iv = self.__generate_iv(len(raw_password))
			else:
				self.iv = iv

			iv = self.iv

			for raw_block in raw_blocks:

				# Aplicar operador XOR con el bloque en crudo y el IV
				block = ''.join([chr(ord(a) ^ ord(b)) for a,b in zip(raw_block,iv)])

				# Para cada caracter del bloque
				for i in range(len(block)):

					# Se le aplica la regla de cifrado

					calc = ( (ord(block[i]) + ord(raw_password[i]) + ord(raw_password[::-1][i])) ^ (ord(raw_password[i])*ord(raw_password[::-1][i])) )

					quotient = ''.join([self.ABC[int(i)] for i in str(calc//SPECIAL_NUMBER)])

					chr_n = ( (calc%SPECIAL_NUMBER) * sk1 + sk2 ) % SPECIAL_NUMBER

					text.append("¿"+quotient+"¡"+self.ABC[chr_n])

				# El resultado de cifrado de tal bloque, ahora es el IV	
				iv = block

		else:

			raise ABCException("ABC not established")

		return ''.join(text)


	def decrypt(self,raw_string,password,iv,seed=0,string_shift=0,subkey1=1,subkey2=1):

		"""

		Devuelve cadena descifrada.

		Parametros -> raw_string: string (ejemplo) ¿bcb¡T¿bcg¡e¿bce¡w¿bcc¡X¿bcf¡r¿bcf¡F¿bcc¡7¿bce¡B¿bcf¡q¿bcc¡6
		              password: string (ejemplo) password
		              iv: string
		              seed: integer (por defecto 0)
		              string_shift: integer (por defecto 0)
		              subkey1: integer coprime (por defecto 1)
		              subkey2: integer (por defecto 1)

		Salida: 

		"""

		# Ordenar ABC
		self.set_seed(seed)

		# Obtener cadena modificada y cocientes
		quotients,string = self.__clear_string(raw_string)

		raw_password = self.__check_password(raw_string,password)
		password = self.__password_complete(string,raw_password)

		raw_decrypt = [] 

		if (self.ABC!=None):

			for i in range(len(string)):

				# Obtener entero de la letra cifrada
				n_letter = self.ABC.index(string[i])

				# Calculo de descifrado
				calc = ((SPECIAL_NUMBER*quotients[i] +((inverse(subkey1,SPECIAL_NUMBER)[0]*(n_letter-subkey2))%SPECIAL_NUMBER)) ^ (ord(password[i])*ord(password[::-1][i]))) - ord(password[i]) - ord(password[::-1][i])

				try:
					raw_decrypt.append(chr(calc))
				except ValueError:
					# Si hay caracteres inexistentes, seleccionarlos al azar
					raw_decrypt.append(chr(random.randint(33,126)))

		else:

			raise ABCException("ABC not established")

		# Cadena en texto plano en formato lista
		decrypt = []

		raw_blocks = self.__build_blocks(''.join(raw_decrypt),len(raw_password))

		for raw_block in raw_blocks:

			block = []

			if (iv!=None):

				for a,b in zip(raw_block,iv):

					ordinal_chr = ord(a) ^ ord(b)

					# Si entero supero tal numero, significa que es un caracter invalido,
					# por lo que se cambia por un caracter valido.
					if (ordinal_chr<=55291): 
						block.append(chr(ordinal_chr))
					else:
						block.append(chr(random.randint(33,255)))

				# Cada bloque de descifrado se agrega a la lista
				decrypt.append(''.join(block))

				# IV toma el valor del trozo de cadena actual
				iv = raw_block

			else:

				raise KatyaException("The IV is not valid for use")

		#if (string_shift!=0):
		#	decrypt = self.__modify_msg(''.join(raw_decrypt),string_shift)

		#else:
		#	decrypt = ''.join(raw_decrypt)

		return ''.join(decrypt)