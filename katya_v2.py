#!/usr/bin/python3

import string 
import random
import collections

from math import gcd as coprime
from sympy.core.numbers import igcdex as inverse


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

class CipherException(Exception):
	pass



# Algoritmo de Katya: f(L,Kn,Ki,n) = [[(L+Kn+Ki) mod 96]^(Kn)] mod n;

class Cipher:

	def __init__ (self):

		self.ABC = None
		self.seed_ = 0
		self.subkey1,self.subkey2 = (5,1)

	def key_complete(self,string,key):

		new_key = ""

		if (len(key)<=len(string)):

			while (len(new_key)<len(string)):
				new_key += key
			
			if (len(new_key)>len(string)):
				new_key = new_key[:len(string)]

		else:

			new_key = key[:len(string)]


		return new_key

	def subkeys(self,a=1,b=1):

		if (isinstance(a,int) and isinstance(b,int)) and ((a>0 and a<=96) and (b>0 and b<=96)) and (coprime(a,96)==1):
			self.subkey1,self.subkey2 = (a,b)

		else:
			raise SubkeysError('Failed to set subkeys')

		return (self.subkey1,self.subkey2)

	def show_possible_subkeys(self):

		subkeys_ = []

		a,b = (1,96)

		for i in range(a,b+1):
			if (coprime(i,b)==1):
				subkeys_.append(i)

		return subkeys_


	def shifts(self,generic_list,num):

		generic = collections.deque(generic_list)
		generic.rotate(num)

		generic_list = list(generic)

		return generic_list

	''' Funciones para lenguaje '''

	def set_ABC(self,abc=0):

		if (isinstance(abc,list)) and (len(abc)==96) and (abc!=0):

			self.ABC = abc

		elif (abc==0):

			self.ABC = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","ñ","o","p","q","r","s","t","u","v","w","x","y","z",
			            "A","B","C","D","E","F","G","H","I","J","K","L","M","N","Ñ","O","P","Q","R","S","T","U","V","W","X","Y","Z",
			            "0","1","2","3","4","5","6","7","8","9","!","\"","#","$","%","&","'","(",")","*","+","´","-",".","/",
			            ":",";","<","=",">","@","[","\\","]","^","_","`","{","|","}","~","?"]

			#random.shuffle(self.ABC)

		else:
			
			raise ABCInvalid("ABC Invalid")

		return self.ABC


	def random_ABC(self):

		if (self.ABC!=None):

			self.set_ABC(0)

			num = random.randint(0,95)

			self.ABC = self.shifts(self.ABC,num)

			self.seed_ = num

		else:

			raise ABCNotEstablished("ABC not established")

		return self.seed_

	def set_seed(self,integer=0):

		if (isinstance(integer,int)) and (integer<=95 and integer>0):

			self.set_ABC(0)

			self.ABC = self.shifts(self.ABC,integer)

			self.seed_ = integer

		elif (isinstance(integer,int)) and (integer>95 or integer<0):

			raise ShiftInvalid("Seed is not in the range (0-95)")

		return self.seed_


	''' Funcion para orden de mensaje '''

	def build_matrix(self,string,long_key):

		matrix = [string[i:i+long_key] for i in range(0,len(string),long_key)]

		return matrix

	def modify_msg(self,string,key,shift):

		if (shift!=0) and (shift<=len(key) and shift>0):
			matrix = self.build_matrix(string,len(key))
			return ''.join(self.shifts(matrix,shift))

		elif (shift!=0) and (shift>len(key) or shift<0):
			raise ShiftException("Displacement does not meet desired length")

		else:
			return 0

	''' Funciones de cifrado y descifrado '''

	def encrypt(self,string,key,string_shift=0):
		
		if (string_shift!=0):
			string = self.modify_msg(string,key,string_shift)

		key = self.key_complete(string,key)
		sk1,sk2 = self.subkey1,self.subkey2

		text = [] 

		if (self.ABC!=None):

			for i in range(len(string)):

				suma = ord(string[i]) + ord(key[i]) + ord(key[::-1][i])
				opbit = suma ^ (ord(key[i])*ord(key[::-1][i])) 
				calc = (opbit * sk1) + sk2
				mod = calc % 96

				#index = ( ( (ord(string[i]) + ord(key[i]) + ord(key[::-1][i])) ^ (ord(key[i])*ord(key[::-1][i])) ) * sk1 + sk2 ) % 96 

				print(calc, end=" ")

				index = mod

				text.append(self.ABC[index])

			print('')

		else:

			raise ABCNotEstablished("ABC not established")

		return ''.join(text)


	def decrypt(self,string,key,mod=96,order=0,p=1,f=1):

		self.ABC = self.set_ABC(order)

		key = self.key_complete(string,key)

		decrypt = [] 

		if (self.ABC!=None):

			for i in range(len(string)):

				a = self.ABC.index(string[i])

				index = ((inverse(5,96)[0]*(a-f))%96) 

				print(index,end=" ")

		else:

			raise ABCNotEstablished("ABC not established")

		return ''.join(decrypt)

		return


m = Cipher()

m.set_ABC()
#m.random_ABC()
s = m.set_seed(0)
#print(m.show_possible_subkeys())
#m.subkeys()
print (m.encrypt("Marco Martel","password"), ' -> Desplazamiento: ',s)
print (m.decrypt("b9koT-GbzN>6","password",p=5,f=1))
#print(m.modify_msg("Cifrado __ sera aprobado? O es solo una porquería?","password",0))