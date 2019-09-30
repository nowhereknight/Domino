import os
import sys
import random
from time import sleep
domino = [(6,6),(6,5),(6,4),(6,3),(6,2),(6,1),(6,0),(5,5),(5,4),(5,3),(5,2),(5,1),(5,0),
		(4,4),(4,3),(4,2),(4,1),(4,0),(3,3),(3,2),(3,1),(3,0),(2,2),(2,1),(2,0),(1,1),(1,0),(0,0)]
mesa = [(6,6),(6,5),(6,4),(6,3),(6,2),(6,1),(6,0),(5,5),(5,4),(5,3),(5,2),(5,1),(5,0),
		(4,4),(4,3),(4,2),(4,1),(4,0),(3,3),(3,2),(3,1),(3,0),(2,2),(2,1),(2,0),(1,1),(1,0),(0,0)]
tablero = []
sumaTablero = 0
for i in tablero:
	sumaTablero += sum(i)

class Admin:
	def __init__ (self):
		pass
	def CrearJugador (self):
		"""Método para crear jugadores registrado como Administrador"""
		clearScreen()
		file = open("texto.txt","a")
		jugador = input("Ingresa el nombre del jugador:\n")
		password = input("Ingresa la contraseña del usuario:\n")
		password_again = input("Ingresa la contraseña del usuario nuevamente:\n")
		if password==password_again:
			file.write(jugador+"::"+Caesar(password)+"\n")
			print("Jugador creado correctamente.")
		else:
			print("Las contraseñas no coinciden")
			self.CrearJugador()
		file.close()
		sleep(2)
		clearScreen()
class Partida:
	def __init__(self):
		global mesa
		global tablero
		self.empate = 0	
		self.players = []
	def Jugar(self,primero):
		"""Método principal que contiene la estructura del juego"""
		index = primero+1
		while True:
			clearScreen()
			if index == len(self.players):
				index = 0
			if index == 0:
				print("El tablero es:".center(40," "))
				print(str(tablero).center(40," "))
				if self.menuJugador(self.players[index]) == 4:
					self.players[0].puntuacion -= sumaTablero//4
					return
			else:
				if self.players[index].MachineTurn(self):
					print(self.players[index].name+' tiró una ficha')
					print("El tablero es:".center(40," "))
					print(str(tablero).center(40," "))
					self.empate = 0
				else:
					if self.players[index].comerFicha(self):
						print(self.players[index].name+' robó una ficha')
						print(self.players[index].name+' tiró una ficha')
						print("El tablero es:".center(40," "))
						self.empate = 0
					else:
						print(self.players[index].name+' pasa')
						print("El tablero es:".center(40," "))
						print(str(tablero).center(40," "))
						self.empate += 1
			if len(self.players[index].fichas)==0:
				print(self.players[index].name+' ha ganado.')
				if self.players[index] == self.players[0]:
					print("Felicidades. Disfruta este momento mientras dure")
					self.players[0].puntuacion += sumaTablero//4
					self.players[0].victorias +=1
				else:
					print("Has fracasado.")
					self.players[0].puntuacion -= sumaTablero//4
				sleep(3)
				return
			if self.empate == len(self.players)*2:
				print('Todos los jugadores han pasado.')
				print('El juego se declara como empate.')
				return
			index += 1
		sleep(2)
	def menuJugador(self, jugador):
		"""Menú que se despliega cuando es el turno del usuario"""
		while True:
			print(jugador.nombre+' tu mano es:')
			print(jugador.fichas)
			try:
				op = int(input("\n¿Qué deseas hacer?\n1) Tirar una ficha.\n2) Comer una ficha.\n3) Pasar de turno.\n4) Rendirse. "))
			except ValueError as vE:
				print('Opción inválida.\nVuelve a intentar!')
				sleep(2)
			else:
				if op == 1:
					num=1
					print("¿Qué ficha deseas tirar?\n")
					for aux in range(0,len(jugador.fichas)):
						print(num,") ",jugador.fichas[aux])
						num+=1
					try:
						ficha = int(input())
					except ValueError as vE:
						print('Opción inválida')
					else:
						if jugador.UserTurn(self, ficha-1):
							print(jugador.nombre+' tiró una ficha')
							self.empate = 0
							return
				elif op == 2:
					if jugador.comerFicha(self):
						print('Robaste una ficha')
						self.empate = 0
						return
					else:
						print("Ya no quedan fichas. Debes de pasar de turno.")
				elif op == 3:
					if mesa:
						print("Todavía hay fichas para comer chavo")
					else:
						return False	
				elif op == 4:
					print("Te has rendido. Descepcionante. Más no inesperado. Vuelve a la próxima.")
					sleep(3)
					sys.exit()

				else:
					print('Opción inválida.\nVuelve a intentar!')
					sleep(1)	
class Jugador:
	def __init__(self):
		global primero
		global raw_usuario
		self.name = raw_usuario
		self.password = raw_psw
		self.victorias = 0
		self.derrotas = 0
		self.puntuacion = 0
		self.empates = 0
		self.fichas = []
	def Jugar(self):
		"""Estructura principal del juego"""
		try:
			p = int(input("¿Contra cuántos jugadores quieres jugar?\n1) 1 Jugador.\n2) 2 Jugadores.\n3) 3 Jugadores.\n4) Regresar al menú anterior.\n"))
		except ValueError as vE:
			print("Selecciona una opción valida.")
			self.Jugar()
		else:
			if p == 1:
				partida = Partida()
				partida.players.append(self)
				Oponent1 = Jugador()
				partida.players.append(Oponent1)
				for x in range (1,8):
					a = mesa[random.randrange(0,len(mesa))]
					partida.players[0].fichas.append(a)
					mesa.remove(a)
					b = mesa[random.randrange(0,len(mesa))]
					partida.players[1].fichas.append(b)
					mesa.remove(b)
				for aux in range(6,0,-1):
					if (aux,aux) in partida.players[1].fichas:
						tablero.append((aux,aux))
						#clearScreen()
						print("El oponente tiene la mula ("+str(aux)+" : "+str(aux)+").")
						sleep(1)
						primero = 1
						"""MenuJugador(self.fichas,Jugador1.fichas)"""
						break
					elif (aux,aux) in partida.players[0].fichas:
						tablero.append((aux,aux))
						sleep(2)
						print("Tú tienes la mula más grande")
						primero = 0
						#MachinePlay(Jugador1.fichas,self.fichas)
						break
					else:
						print("Nadie tiene la mula más grande por lo que tú comienzas.")
						sleep(2)
						primero=0
				partida.Jugar(primero)
				file = open('usuarios.txt', 'w')
				for i in users:
					if users[i]==Caesar(ADMIN):
						file.write(self.name+'::'+self.password+'\n')
					elif user[i] in Historial:
						file.write(self.name+'::'+Caesar(self.password)+'::'+str(self.victorias)+'::'+str(self.derrotas)+'::'+str(self.empates)+'::'+str(self.puntuacion)+'\n')
				file.close()
				del partida
				sleep(5)
				return
			elif p == 2:
				partida = Partida()
				partida.players.append(self)
				Oponent1 = Jugador()
				partida.players.append(Oponent1)
				Oponent2 = Jugador()
				partida.players.append(Oponent2)

				for x in range (1,8):
					a = mesa[random.randrange(0,len(mesa))]
					partida.players[0].fichas.append(a)
					mesa.remove(a)
					b = mesa[random.randrange(0,len(mesa))]
					partida.players[1].fichas.append(b)
					mesa.remove(b)
					c = mesa[random.randrange(0,len(mesa))]
					partida.players[2].fichas.append(c)
					mesa.remove(c)
				for aux in range(6,0,-1):
					if (aux,aux) in partida.players[2].fichas:
						tablero.append((aux,aux))
						#clearScreen()
						print("El oponente 2 tiene la mula ("+str(aux)+" : "+str(aux)+").")
						sleep(1)
						primero = 2
						break
					if (aux,aux) in partida.players[1].fichas:
						tablero.append((aux,aux))
						#clearScreen()
						print("El oponente 1 tiene la mula ("+str(aux)+" : "+str(aux)+").")
						sleep(1)
						primero = 1
						break
					elif (aux,aux) in partida.players[0].fichas:
						tablero.append((aux,aux))
						sleep(2)
						print("Tú tienes la mula más grande")
						primero = 0
						#MachinePlay(Jugador1.fichas,self.fichas)
						break
					else:
						print("Nadie tiene la mula más grande por lo que tú comienzas.")
						primero=0
				partida.Jugar(primero)
				file = open('usuarios.txt', 'w')
				for i in users:
					if users[i]==Caesar(ADMIN):
						file.write(self.name+'::'+self.password+'\n')
					else:
						file.write(self.name+'::'+Caesar(self.password)+'::'+str(self.victorias)+'::'+str(self.derrotas)+'::'+str(self.empates)+'::'+str(self.puntuacion)+'\n')
				file.close()
				del partida
				sleep(5)
				return
			elif p == 3:
				partida = Partida()
				partida.players.append(self)
				Oponent1 = Jugador()
				partida.players.append(Oponent1)
				Oponent2 = Jugador()
				partida.players.append(Oponent2)
				Oponent3 = Jugador()
				partida.players.append(Oponent3)

				for x in range (1,8):
					a = mesa[random.randrange(0,len(mesa))]
					partida.players[0].fichas.append(a)
					mesa.remove(a)
					b = mesa[random.randrange(0,len(mesa))]
					partida.players[1].fichas.append(b)
					mesa.remove(b)
					c = mesa[random.randrange(0,len(mesa))]
					partida.players[2].fichas.append(c)
					mesa.remove(c)
					d = mesa[random.randrange(0,len(mesa))]
					partida.players[3].fichas.append(d)
					mesa.remove(d)
				for aux in range(6,0,-1):
					if (aux,aux) in partida.players[3].fichas:
						tablero.append((aux,aux))
						#clearScreen()
						print("El oponente 3 tiene la mula ("+str(aux)+" : "+str(aux)+").")
						sleep(1)
						primero = 3
						break
					if (aux,aux) in partida.players[2].fichas:
						tablero.append((aux,aux))
						#clearScreen()
						print("El oponente 2 tiene la mula ("+str(aux)+" : "+str(aux)+").")
						sleep(1)
						primero = 2
						break
					if (aux,aux) in partida.players[1].fichas:
						tablero.append((aux,aux))
						#clearScreen()
						print("El oponente 1 tiene la mula ("+str(aux)+" : "+str(aux)+").")
						sleep(1)
						primero = 1
						break
					elif (aux,aux) in partida.players[0].fichas:
						tablero.append((aux,aux))
						sleep(2)
						print("Tú tienes la mula más grande")
						primero = 0
						#MachinePlay(Jugador1.fichas,self.fichas)
						break
					else:
						print("Nadie tiene la mula más grande por lo que tú comienzas.")
						primero=0
				partida.Jugar(primero)
				file = open('usuarios.txt', 'w')
				for i in users:
					if users[i]==Caesar(ADMIN):
						file.write(self.name+'::'+self.password+'\n')
					else:
						file.write(self.name+'::'+Caesar(self.password)+'::'+str(self.victorias)+'::'+str(self.derrotas)+'::'+str(self.empates)+'::'+str(self.puntuacion)+'\n')
				file.close()
				del partida
				sleep(5)
				return
			elif p == 4:
				Type()

	def MachineTurn(self, domino):
		"""Actúa por los oponentes ficticios"""
		for i in self.fichas:
			if i[0] == tablero[0][0]:
				tablero.insert(0, self.fichas.pop(self.fichas.index(i))[::-1])
				return True
			elif i[1] == tablero[0][0]:
				tablero.insert(0, self.fichas.pop(self.fichas.index(i)))
				return True
			elif i[0] == tablero[-1][1]:
				tablero.append(self.fichas.pop(self.fichas.index(i)))
				return True
			elif i[1] == tablero[-1][1]:
				tablero.append(self.fichas.pop(self.fichas.index(i))[::-1])
				return True
		return False
	def UserTurn(self, domino, x):
		"""Evalúa si la ficha que se trata de tirar coincide"""
		if x in range(len(self.fichas)):
			if self.fichas[x][0] == tablero[0][0]:
				tablero.insert(0, self.fichas.pop(x)[::-1])
				return True
			elif self.fichas[x][1] == tablero[0][0]:
				tablero.insert(0, self.fichas.pop(x))
				return True
			elif self.fichas[x][0] == tablero[-1][1]:
				tablero.append(self.fichas.pop(x))
				return True
			elif self.fichas[x][1] == tablero[-1][1]:
				tablero.append(self.fichas.pop(x)[::-1])
				return True
			print('La ficha que estás tratando de tirar no coindide')
			return False
		else:
			print('La ficha no es válida')
			return False

	def comerFicha(self, domino):
		"""Método para comer fichas"""
		if len(mesa) > 0:
			r = random.randint(0, len(mesa)-1)
			self.fichas.append(mesa.pop(r))
			return True
		return False

	def __repr__(self):
		return self.nombre
def clearScreen():
	"""Limpia la pantalla dependiendo del sistema operativo del que se trate"""
	if os.name == 'posix':
		os.system('clear')
	elif os.name == 'nt':
		os.system('cls')
def Caesar(a):
	"""Cifra una canción en cifrado Caesar"""
	nuevo = ""
	for symbol in a:
		if symbol.isalpha():
			num = ord(symbol)
			num+=3
			if symbol.isupper():
				if num > ord('Z'):
					num-= 26
				elif num < ord('A'):
					num += 26
			elif symbol.islower():
				if num > ord('z'):
					num-=26
				elif num < ord('a'):
					num += 26
			nuevo += chr(num)
		else:
			nuevo += symbol
	return(nuevo)
def invCaesar(a):
	"""Decifra un valor en cifrado Caesar"""
	nuevo = ""
	for symbol in a:
		if symbol.isalpha():
			num = ord(symbol)
			num+=-3
			if symbol.isupper():
				if num > ord('Z'):
					num-= 26
				elif num < ord('A'):
					num += 26
			elif symbol.islower():
				if num > ord('z'):
					num-=26
				elif num < ord('a'):
					num += 26
			nuevo += chr(num)
		else:
			nuevo += symbol
	return(nuevo)
def InputData():
	"""Solicita el usuario y contraseña al usuario"""
	global raw_usuario, raw_psw
	raw_usuario = input("Ingresa la información.\nUsuario:\n")
	raw_psw = input("Contraseña:\n")

element = []
def ScanFile():
	"""Almacena las lineas del archivo en una lista"""
	global element
	with open('texto.txt') as file:
		element = file.read().splitlines()
	file.close()
users = {}
def ListaJugadores():
	"""Asigna los elementos de una lista en un diccionario con el usuario siendo la llave y el código siendo la contraseña"""
	global users
	for x in range (0,len(element)):
		a = element[x]
		b = a.split("::")
		users[b[0]]=invCaesar(b[1])
def MenuAdmin():
	"""Esta función almacena lo que """
	asw = int(input("Seleccione la opción deseada:\n1) Crear un nuevo Jugador.\n2) Cerrar sesión.\n"))
	try:
		if asw==1:
			administrador = Admin()
			administrador.CrearJugador()
			Type()
		if asw==2:
			clearScreen()
			Main()
			Type()
	except ValueError as vE:
		print("Selecciona una opción valida")
		sleep(2)
		MenuAdmin()
def Type():	
	"""Función que vincula los usuarios dependiendo de si son usuarios comunes o administradores"""
	if raw_usuario in users:
		if users[raw_usuario]==raw_psw:
			if raw_usuario=="Admin":
				clearScreen()
				print("*******************Bienvenido Administrador********************\n\n")
				MenuAdmin()
			else:
				clearScreen()
				print("********************Bienvenido "+raw_usuario+"************************\n")
				jugador = Jugador()
				jugador.nombre = raw_usuario
				asw = int(input("Selecciona la opción deseada:\n1) Jugar domino\n2) Actualizar mi contraseña\n3) Dar de baja esta cuenta\n4) Cerrar sesión\n\n"))
				try:
					if asw==1:
						clearScreen()
						jugador.Jugar()
						Type()
					if asw==2:
						clearScreen()
						aux2 = {}
						answer=input("Ingresa la antigua contraseña\n")
						if answer==raw_psw:
							new_psw=input("Ingresa la nueva contraseña\n")
							new_psw2=input("Ingresa la nueva contraseña nuevamente\n")
							if new_psw2==new_psw:
								with open('texto.txt') as file:
									aux = file.read().splitlines()
								file.close()
								file = open("texto.txt","w")
								for line in aux:
									if line in aux:
										if raw_usuario in line:
											file.write(raw_usuario+"::"+Caesar(new_psw)+"\n")
										else:
											file.write(line+"\n")
								file.close()
						else:
							print("Ingresaste una contraseña errónea. Trátalo nuevamente.")
							sleep(5)
							Type()
					if asw==3:
						file = open("texto.txt","r")
						lines = file.readlines()
						file.close
						file = open("texto.txt","w")
						for line in lines:
							if line in lines:
								if raw_usuario in line:
									pass
								else:
									file.write(line)
						file.close
						print("La cuenta ha sido eliminada con éxito")
						Main()
					if asw==4:
						clearScreen()
						Main()
						Type()
				except ValueError as vE:
					print("Selecciona una opción valida")
					sleep(2)

def Main():
	"""Función que encapsula tres funciones que sirven para dar acceso al juego"""
	InputData()
	ScanFile()
	ListaJugadores()
"""***************************************Main Program***************************************"""
a="-------------------Proyecto Final-----------------" 
print (a.center(100," "))
b="|                                                  |" 
print (b.center(100," "))
c="|    UNICA           Curso: Python                 |" 
print (c.center(100," "))
d="|    Semestre:           2017-2                    |" 
print (d.center(100," "))
e="|    Generación            73                      |" 
print (e.center(100," "))
f="|    Prebecario:  Rodríguez Agiss Zuriel Uzai      |" 
print (f.center(100," "))
g="|                                                  |" 
print (g.center(100," "))
h="--------------------------------------------------" 
print (h.center(100," "))

Main()
Type()