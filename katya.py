#!/usr/bin/python3

#  _  __   _ _______   ___      ___ _____   _____ _____ 
# | |/ /  /_\_   _\ \ / /_\    / __| _ \ \ / / _ \_   _|
# | ' <  / _ \| |  \ V / _ \  | (__|   /\ V /|  _/ | |  
# |_|\_\/_/ \_\_|   |_/_/ \_\  \___|_|_\ |_| |_|   |_|
#
#                 Created by Kirari

import random
import collections

from os import remove
from os.path import isfile
from math import gcd as coprime
from base64 import b64encode, b64decode
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

BLOCK_SIZE = 20

IV_SIZE = 20


# Formula de cifrado Katya: [ ( [(L+Lk+Lki) ^ (Lk*Lki))] % 91 ) * sk1 + sk2 ] % 91 

# L: letra en crudo
# Lk: letra de la contraseña
# Lki: letra de la contraseña (invertida)
# sk1: subclave 1
# sk2: subclave 2

# Ejemplo de contraseña invertida: password -> yek



# Formula de descifrado Katya: [ [(91*Coc + (a^-1) * (Lc-sk2))%91] ^ [Lk*Lki] ] - Lk - Lki

# C: cociente calculado 
# a^-1: inverso multiplicativo (aritmetica modular)
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


	# METODO EN DESUSO (POR AHORA)
	def __shifts(self,generic_list,num):

		"""

		Devuelve una lista con los trozos de mensaje desplazado.

		Parametros -> generic_list: lista a trozos de mensaje (ejemplo) ["Hola","Mundo!","Es","la","hora."]
		              num: desplazamientos de los elementos de la lista (ejemplo) 3

		Salida: ["Es","la","hora.","Hola","Mundo!"]

		"""

		generic = collections.deque(generic_list)
		generic.rotate(num)

		generic_list = list(generic)

		return generic_list


	def __generate_iv(self):

		""" Generador de Vector de Inicializacion con longitud contraseña"""

		return ''.join([chr(random.randint(33,126)) for i in range(IV_SIZE)])


	# FUNCIONES PARA MANIPULACION DE SUBCLAVES

	def subkeys(self,a=1,b=1):

		"""

		Devuelve una tupla con las dos subclaves para cifrar el mensaje. Tales
		son un numero coprimo y el otro un desplazamiento.

		Parametros -> a: integer coprime (ejemplo) 1
		              b: integer (ejemplo) 1

		Salida: (1,1)

		"""

		try:

			if (isinstance(a,int) and isinstance(b,int)) and ((a>0 and a<=SPECIAL_NUMBER) and (b>0 and b<=SPECIAL_NUMBER)) and (coprime(a,SPECIAL_NUMBER)==1):
				self.subkey1,self.subkey2 = (a,b)

				return (self.subkey1,self.subkey2)
			
			else:
				raise SubkeysError('Failed to set subkeys')

		except SubkeysError as e:

			print (e)

		return False


	def show_possible_subkeys(self):

		"""

		Devuelve las posibles subclaves (numeros coprimos) que se podran utilizar.

		"""

		a,b = (1,SPECIAL_NUMBER)

		return [i for i in range(a,b+1) if coprime(i,b)==1]


	# FUNCIONES PARA EL LENGUAJE

	def set_ABC(self,abc=0):

		"""

		Devuelve el abecedario que se utilizara para cifrar el mensaje.

		Parametros -> abc: integer or list (por defecto 0)

		Se puede establecer un abecedario personalizado, solo debe cumplir las
		siguientes reestricciones:

		- abc tiene que ser una lista
		- abc debe ser de longitud 91
		- abc no deber tener caracteres repetidos

		"""

		try:

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

		except ABCException as e:

			print (e)

		return False

	def random_ABC(self):

		"""

		Devuelve un entero que indica el orden en el que se encuentra el ABC, luego
		de haber sido alterado aleatoriamente.

		Se utiliza un numero aleatorio y a traves del modulo random altera el ABC. 
		Hay que considerar que si pierde el numero de orden o semilla entonces no 
		podra recuperar la informacion al momento de querer descifrarla.

		"""
		try:

			if (self.ABC!=None):

				self.set_ABC(0)

				num = random.randint(0,SPECIAL_NUMBER-1)

				random.Random(num).shuffle(self.ABC)

				self.seed_ = num

				return self.seed_

			else:

				raise ABCException("ABC not established")

		except ABCException as e:

			print (e)

		return False


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

				return self.seed_

			else:

				raise SeedException("An error occurred while setting seed")

		except SeedException as s:

			print (s)

		return False


	# FUNCIONES PARA MODIFICAR MENSAJE

	def __build_blocks(self,raw_string):

		"""

		Devuelve una lista con trozos de mensaje con longitud BLOCK_SIZE.

		Parametros -> raw_string: string (ejemplo) Hola Mundo | Si BLOCK_SIZE = 4

		Salida: ["Hola"," Mun","do\0\0"]

		Nota: si el ultimo elemento no tiene la misma longitud que el BLOCK_SIZE, 
		      entonces se le agregaran caracteres nulos.

		"""

		matrix = [raw_string[i:i+BLOCK_SIZE] for i in range(0,len(raw_string),BLOCK_SIZE)]

		if (len(matrix[-1:][0])<BLOCK_SIZE):

			matrix[len(matrix)-1] = matrix[-1:][0] + '\0'*(BLOCK_SIZE - len(matrix[-1:][0]))

		return matrix


	def __blocks_quotients(self,quotients,long_quotiens,long_blocks):

		"""

		Devuelve lista de bloques. Cada bloque contiene los cocientes de un trozo de cadena longitud IV

		Salida ejemplo: [[1,4,6,1],[2,3,4,5],[5,5,1,2],[4,0,1,3]]

		"""

		long_ = long_quotiens//long_blocks

		return [quotients[i:i+long_] for i in range(0, len(quotients), long_)]


	# METODO EN DESUSO (POR AHORA)
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
	
	def __KatyaEncypter(self,s_block,p_block):

		"""

		Devuelve bloque de cadena cifrado y proximo IV.

		"""

		# Asignar subclaves
		sk1,sk2 = self.subkey1,self.subkey2

		iv,enc_string = ("","")

		for i in range(len(s_block)):

			# Se le aplica la regla de cifrado
			calc = ( (ord(s_block[i]) + ord(p_block[i]) + ord(p_block[::-1][i])) ^ (ord(p_block[i])*ord(p_block[::-1][i])) )

			quotient = ''.join([self.ABC[int(i)] for i in str(calc//SPECIAL_NUMBER)])

			chr_n = ( (calc%SPECIAL_NUMBER) * sk1 + sk2 ) % SPECIAL_NUMBER

			enc_string += "¿"+quotient+"¡"+self.ABC[chr_n]
			iv += self.ABC[chr_n]

		return (enc_string,iv)


	def __CBC_Encypt(self,raw_string,raw_password,iv):

		"""

		Devuelve resultado del cifrado CBC.

		"""

		cbc_result = ""

		s_blocks = self.__build_blocks(raw_string)
		password = self.__password_complete(''.join(s_blocks),raw_password)	
		p_blocks = self.__build_blocks(password)

		for i in range(len(s_blocks)):

			# Aplicar operador XOR con el bloque y el IV
			block_xor = ''.join([chr(ord(a) ^ ord(b)) for a,b in zip(s_blocks[i],iv)])

			# Aplicar cifrado Katya
			block_cipher,iv = self.__KatyaEncypter(block_xor,p_blocks[i])

			cbc_result += block_cipher

		return cbc_result



	def __KatyaDecypter(self,s_block,p_block,subkey1,subkey2,quotients):

		"""

		Devuelve bloque de cadena descifrado. 

		"""

		raw_decrypt = ""
		
		for i in range(len(s_block)):

			# Obtener entero de la letra cifrada
			n_letter = self.ABC.index(s_block[i])

			# Calculo de descifrado
			calc = ((SPECIAL_NUMBER*quotients[i] +((inverse(subkey1,SPECIAL_NUMBER)[0]*(n_letter-subkey2))%SPECIAL_NUMBER)) ^ (ord(p_block[i])*ord(p_block[::-1][i]))) - ord(p_block[i]) - ord(p_block[::-1][i])

			try:
				raw_decrypt += chr(calc)
			except ValueError:
				# Si hay caracteres inexistentes, seleccionarlos al azar
				raw_decrypt += chr(random.randint(33,126))


		return raw_decrypt

	def __CBC_Decrypt(self,raw_string,raw_password,password,sk1,sk2,quotients,iv):

		"""

		Devuelve resultado del descifrado CBC.

		"""

		s_blocks = self.__build_blocks(raw_string)
		p_blocks = self.__build_blocks(password)
		q_blocks = self.__blocks_quotients(quotients,len(quotients),len(s_blocks))

		cbc_result = ""

		for i in range(len(s_blocks)):

			block = ""
			
			block_decipher = self.__KatyaDecypter(s_blocks[i],p_blocks[i],sk1,sk2,q_blocks[i])

			for a,b in zip(block_decipher,iv):
				ordinal_chr = ord(a) ^ ord(b)
				# Si entero supero tal numero, significa que es un caracter invalido,
				# por lo que se cambia por un caracter valido.
				if (ordinal_chr<=55291): 
					block += chr(ordinal_chr)
				else:
					block += chr(random.randint(33,255))

			cbc_result += block

			iv = s_blocks[i]

		return cbc_result


	def encrypt(self,raw_string,password,string_shift=0,iv=None):

		"""

		Devuelve cadena cifrada.

		Parametros -> raw_string: string (ejemplo) Hola Mundo
		              password: string (ejemplo) password
		              string_shift: integer (alteracion de cadena) (ejemplo) 3  --> en desuso temporalmente
		              iv: string de longitud fija

		Salida: ¿bcb¡T¿bcg¡e¿bce¡w¿bcc¡X¿bcf¡r¿bcf¡F¿bcc¡7¿bce¡B¿bcf¡q¿bcc¡6

		"""
		
		
		#if (string_shift!=0):
		#	raw_string = self.__modify_msg(raw_string,string_shift)


		try:

			# password en crudo y completado con logitud cadena
			raw_password = self.__check_password(raw_string,password)

			if (self.ABC!=None):

				# Generar Vector de Inicializacion (IV)
				self.iv = self.__generate_iv() if iv==None else iv
				iv = self.iv

				# Generar cifrado
				result = self.__CBC_Encypt(raw_string,raw_password,iv)

				return result
			
			else:

				raise ABCException("ABC not established")

		except Exception as exception:

			print (exception)

		return False


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

		try:

				# Ordenar ABC
				self.set_seed(seed)

				# Obtener cadena modificada y cocientes
				quotients,string = self.__clear_string(raw_string)

				raw_password = self.__check_password(raw_string,password)
				password = self.__password_complete(string,raw_password)

				
				if (self.ABC!=None):

					# Obtener resultado del cifrado
					result = self.__CBC_Decrypt(string,raw_password,password,subkey1,subkey2,quotients,iv)

					return result
				
				else:

					raise ABCException("ABC not established")


		except Exception as exception:

			print(exception)

		return False


	# Todo relacionado a archivos

	def __read_file(self,file_name):

		with open(file_name,"rb") as f:

			content = f.read()

		return content

	def __write_file(self,file_name,data):

		with open(file_name,"wb") as f:

			f.write(data) 

		return True


	def file_encrypt(self,file_name,password):

		try:

			if (isfile(file_name)):

				content = b64encode(self.__read_file(file_name))
				
				# Encriptar contenido 
				data_enc = self.encrypt(content.decode(),password)

				data_dump = data_enc.encode()+self.iv.encode()

				self.__write_file(file_name+".katya",data_dump)
				self.__write_file("katya.key",password.encode())

				remove(file_name)

			else:
				print ("File does not exists")

		except Exception as exception:

			print ("An error occurred while encrypting the file: ",exception)


	def file_decrypt(self,file_name,file_pass,seed=0,subkey1=1,subkey2=1):

		try:

			if (isfile(file_name) and file_name.endswith(".katya") and isfile(file_pass) and file_pass.endswith(".key")):

				original_name = file_name[:len(file_name)-6]

				data_enc = self.__read_file(file_name).decode()
				data_enc_ = data_enc[:len(data_enc)-IV_SIZE]
				iv = data_enc[-20:]
				password = (self.__read_file(file_pass).decode()).strip()

				data_dec = b64decode(self.decrypt(data_enc_,password,iv,seed,subkey1,subkey2))

				self.__write_file(original_name,data_dec)

				remove(file_name)
				remove(file_pass)

			else:

				print ("File does not exists or the file does not have the extension (.katya,.key)")

		except ValueError:

			print ("The file could not be decrypted")

		except (Exception,ValueError) as exception:

			print ("An error occurred while decrypting the file: ",exception)

		return


	# Metodos de formato

	def elegant(self,result=None):

		'''

		Devuelve cadena con formato elegante.

		'''

		try:

			if (result!=None):

				result_elegant = "---- BEGIN KATYA TEXT ENCRYPT ----\n\n"

				cont = 0

				for block in result:
					if (cont<=60):
						result_elegant += block
						cont+=1
					else:
						result_elegant += '\n'
						cont = 0

				result_elegant += "\n\n---- END KATYA TEXT ENCRYPT ----\n"

				return result_elegant

			else:

				raise KatyaException("There is no message to decorate")

		except KatyaException as e:

			print (e)

		return False