import itertools
import numpy as np
import cx_Oracle
import socket
import random
import datetime

#codigos iata posibles de aerolineas
a= range(65,91)
b=a
f= lambda x: chr(x)
d= map(f,a)
e= map(f,b)
c= list(itertools.product(d,e))

g= lambda y: ''.join(str(i) for i in y)
cod= map(g,c)

#Nombres posibles de las aerolineas
v= range(1,len(cod)+1)
j= lambda z: 'aerolinea'+str(z)
nom= map(j,v)

#Paises
file= open('Paises.txt', 'r')
p= file.readlines()
file.close()
g= lambda x: x[:-1]
pays= map(g,p)
#arreglar mismo #
pays= pays+pays+pays+pays
p= pays[0:len(cod)]

tot= zip(cod,nom,p)

#ip=socket.gethostbyname(socket.gethostname())
ip= 'fn3.oracle.virtual.uniandes.edu.co'
puerto= 1521
sid= 'prod'
usuario= 'ISIS2304B121620'
password= 'hvlnNayNipo2'
dsn= cx_Oracle.makedsn(ip,puerto,sid)
connection= cx_Oracle.connect(usuario, password, dsn)
#cursor= cx_Oracle.cursor(connection)
cursor= connection.cursor()
cursor.executemany('insert into aerolineas(iatacod, nombre, pais) values (:1, :2, :3)',tot)
connection.commit()

#AEROPUERTOS
#codigos iata 
a= range(65,91)
b=a
h=b
f= lambda x: chr(x)
d= map(f,a)
e= map(f,b)
i= map(f,h)
c= list(itertools.product(d,e,i))
g= lambda y: ''.join(str(z) for z in y)
cod= map(g,c)

#nom aeropuertos
v= range(1,len(cod)+1)
j= lambda z: 'aeropuerto'+str(z)
nom= map(j,v)

#capacidad
av= range(50,125)
act=av
for i in range(1,(len(nom)/len(av))+1):
	act=act+av

cap= act[0:len(nom)]

#ciudades
file= open('Ciudades.txt', 'r')
v=[]
for line in file:
    z=line.split(' ')[0]
    v.append(z)

file.close()
city= v
for i in range(1,(len(nom)/len(v))+1):
	city=city+v

city= city[0:len(nom)]

tot= zip(city, cap, cod, nom)

ip= 'fn3.oracle.virtual.uniandes.edu.co'
puerto= 1521
sid= 'prod'
usuario= 'ISIS2304B121620'
password= 'hvlnNayNipo2'
dsn= cx_Oracle.makedsn(ip,puerto,sid)
connection= cx_Oracle.connect(usuario, password, dsn)
#cursor= cx_Oracle.cursor(connection)
cursor= connection.cursor()
cursor.executemany('insert into aeropuertos(ciudad, capacidadaviones, iatacod, nombre) values (:1, :2, :3, :4)',tot)
connection.commit()

#VUELOS

#idvuelo
idV= range(1,37913)

#idAerolinea
a= range(65,91)
b=a
f= lambda x: chr(x)
d= map(f,a)
e= map(f,b)
c= list(itertools.product(d,e))

g= lambda y: ''.join(str(i) for i in y)
codL= map(g,c)

aeroL= []
for i in idV:
	aeroL.append(random.choice(codL))

#aeropuertos codigos
a= range(65,91)
b=a
h=b
f= lambda x: chr(x)
d= map(f,a)
e= map(f,b)
i= map(f,h)
c= list(itertools.product(d,e,i))
g= lambda y: ''.join(str(z) for z in y)
codP= map(g,c)

#aeropuertos
llegada= []
salida=[]
for i in idV:
	#aeropuerto llegada
	llegada.append(random.choice(codP))
	#aeropuerto salida
	salida.append(random.choice(codP))

#frecuencia
frec= np.ones(len(idV))

#fechas de solo 1 semana
f= []
#fecha
base= "2017-02-"
for i in range(13,19):
	f.append(base+str(i))

#hora salida
horaS= []
#hora llegada
horaLl=[]
#distancia, duración, tipo vuelo
date=[]
dist= []
time=[]
tipoV= []
pos= range(130,20000)
for i in idV:
	j= len(idV)-i
	dist.append(random.choice(pos))
	time.append((dist[-1]*60)/800)
	ran= random.choice(f)
	horaS.append(datetime.datetime.strptime(ran+ " "+ str(i%23) + ":" +str(i%59) + ":" +str(i%59), "%Y-%m-%d %H:%M:%S"))
	horaLl.append(datetime.datetime.strptime(random.choice(f)+ " "+ str(j%23) + ":" +str(j%59) + ":" +str(j%59), "%Y-%m-%d %H:%M:%S"))
	date.append(datetime.datetime.strptime(ran,"%Y-%m-%d"))
	if(dist[-1] < 500):
		tipoV.append(3)
	elif(dist[-1]>=500 and dist[-1]<1000):
		tipoV.append(2)
	else: tipoV.append(1)

#idAvion
ids= range(1,1573)
idA= ids
for i in range(1,(len(idV)/len(ids))+1):
	idA=idA+ids

idA=idA[0:len(idV)]

#idnumvuelo
numV= range(1,1200)
idN= numV
for i in range(1,(len(idV)/len(numV))+1):
	idN=idN+numV

idN=idN[0:len(idV)]

tot= zip(idV, aeroL, idN, salida, llegada, horaS, horaLl, date, frec, dist, time, tipoV, idA)

ip= 'fn3.oracle.virtual.uniandes.edu.co'
puerto= 1521
sid= 'prod'
usuario= 'ISIS2304B121620'
password= 'hvlnNayNipo2'
dsn= cx_Oracle.makedsn(ip,puerto,sid)
connection= cx_Oracle.connect(usuario, password, dsn)
#cursor= cx_Oracle.cursor(connection)
cursor= connection.cursor()
cursor.executemany('insert into vuelos(idvuelo, idaerolinea, idnumvuelo, aeropuertosalida, aeropuertollegada, horasalida, horallegada, fecha, frecuencia, distancia, duracion, tipovuelo, idavion) values (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11, :12, :13)',tot)
connection.commit()


#AEROPUERTOSTIPOSVUELOS
#codigos iata 
a= range(65,91)
b=a
h=b
f= lambda x: chr(x)
d= map(f,a)
e= map(f,b)
i= map(f,h)
c= list(itertools.product(d,e,i))
g= lambda y: ''.join(str(z) for z in y)
cod= map(g,c)

#idtipo
#1 es internacional
#2 es nacional y local
j= [1, 2, 3]
act=j
for i in range(1,(len(nom)/len(j))+1):
	act=act+j

idt= act[0:len(cod)]

tot= zip(idt, cod)

ip= 'fn3.oracle.virtual.uniandes.edu.co'
puerto= 1521
sid= 'prod'
usuario= 'ISIS2304B121620'
password= 'hvlnNayNipo2'
dsn= cx_Oracle.makedsn(ip,puerto,sid)
connection= cx_Oracle.connect(usuario, password, dsn)
#cursor= cx_Oracle.cursor(connection)
cursor= connection.cursor()
cursor.executemany('insert into aeropuertosTiposVuelos(idtipo, codaeropuerto) values (:1, :2)',tot)
connection.commit()

#NACIONALIDADESREMITENTES

# id remitente
idR= range(1,1172)

#nacionalidad
nac= range(1,204)
act=nac+nac+nac+nac+nac+nac
n= act[0:len(idR)]

tot=zip(idR,n)

ip= 'fn3.oracle.virtual.uniandes.edu.co'
puerto= 1521
sid= 'prod'
usuario= 'ISIS2304B121620'
password= 'hvlnNayNipo2'
dsn= cx_Oracle.makedsn(ip,puerto,sid)
connection= cx_Oracle.connect(usuario, password, dsn)
#cursor= cx_Oracle.cursor(connection)
cursor= connection.cursor()
cursor.executemany('insert into nacionalidadesremitentes(idremitente, nacionalidad) values (:1, :2)',tot)
connection.commit()

#VIAJEROS
#idViajero
v= range(1,100001)

#identificacion
ide= range(1020819000,1020919000)

#nombres
w= range(1,len(v)+1)
j= lambda z: 'viajero'+str(z)
nom= map(j,w)

tot=zip(nom,ide,v)

ip= 'fn3.oracle.virtual.uniandes.edu.co'
puerto= 1521
sid= 'prod'
usuario= 'ISIS2304B121620'
password= 'hvlnNayNipo2'
dsn= cx_Oracle.makedsn(ip,puerto,sid)
connection= cx_Oracle.connect(usuario, password, dsn)
#cursor= cx_Oracle.cursor(connection)
cursor= connection.cursor()
cursor.executemany('insert into viajeros(nombre, identificacion, idviajero) values (:1, :2, :3)',tot)
connection.commit()

#NACIONALIDADESVIAJEROS
# idviajero
idV= range(1,100001)

#nacionalidad
nac= range(1,204)
div= len(idV)/len(nac)
n= nac
for i in range(1,div+1):
	n=n+nac

n= n[0:len(idV)]

tot=zip(idV,n)

ip= 'fn3.oracle.virtual.uniandes.edu.co'
puerto= 1521
sid= 'prod'
usuario= 'ISIS2304B121620'
password= 'hvlnNayNipo2'
dsn= cx_Oracle.makedsn(ip,puerto,sid)
connection= cx_Oracle.connect(usuario, password, dsn)
#cursor= cx_Oracle.cursor(connection)
cursor= connection.cursor()
cursor.executemany('insert into nacionalidadesviajeros(idviajero, nacionalidad) values (:1, :2)',tot)
connection.commit()

#VUELOSCARGA
#idvuelo
idV= range(1,37913)

#costodensidad
cost=[]
for i in idV:
	cost.append(random.choice(range(50,5000)))

tot=zip(idV,cost)

ip= 'fn3.oracle.virtual.uniandes.edu.co'
puerto= 1521
sid= 'prod'
usuario= 'ISIS2304B121620'
password= 'hvlnNayNipo2'
dsn= cx_Oracle.makedsn(ip,puerto,sid)
connection= cx_Oracle.connect(usuario, password, dsn)
cursor= connection.cursor()
cursor.executemany('insert into vueloscarga(idvuelo, costodensidad) values (:1, :2)',tot)
connection.commit()

#VUELOSPASAJEROS
#idvuelo
idV= range(1,37913)

#costoeconomico y costoejecutivo
econ=[]
ejec=[]
for i in idV:
	econ.append(random.choice(range(50,3000)))
	ejec.append(random.choice(range(150,6000)))

tot=zip(idV,econ, ejec)

ip= 'fn3.oracle.virtual.uniandes.edu.co'
puerto= 1521
sid= 'prod'
usuario= 'ISIS2304B121620'
password= 'hvlnNayNipo2'
dsn= cx_Oracle.makedsn(ip,puerto,sid)
connection= cx_Oracle.connect(usuario, password, dsn)
cursor= connection.cursor()
cursor.executemany('insert into vuelospasajeros(idvuelo, costoeconomico, costoejecutivo) values (:1, :2, :3)',tot)
connection.commit()

#VIAJESREALIZADOS
#idvuelo
idV=range(1,50)
#for i in range(1, 1001):
#	idvuel.append(random.choice(range(1,37913)))

#idavion
ids= range(1,1573)
idA= ids
for i in range(1,(len(idvuel)/len(ids))+1):
	idA=idA+ids

idA=idA[0:len(idvuel)]

#fechas de solo 1 semana
f= []
#fecha
base= "2017-02-"
for i in range(13,19):
	f.append(base+str(i))

#hora salida
horaS= []
#hora llegada
horaLl=[]
#distancia, duración, tipo vuelo
date=[]
dist= []
time=[]
tipoV= []
pos= range(130,20000)
for i in idV:
	j= len(idV)-i
	ran= random.choice(f)
	horaS.append(datetime.datetime.strptime(ran+ " "+ str(i%23) + ":" +str(i%59) + ":" +str(i%59), "%Y-%m-%d %H:%M:%S"))
	horaLl.append(datetime.datetime.strptime(random.choice(f)+ " "+ str(j%23) + ":" +str(j%59) + ":" +str(j%59), "%Y-%m-%d %H:%M:%S"))
	date.append(datetime.datetime.strptime(ran,"%Y-%m-%d"))

a= range(65,91)
b=a
f= lambda x: chr(x)
d= map(f,a)
e= map(f,b)
c= list(itertools.product(d,e))

g= lambda y: ''.join(str(i) for i in y)
cod= map(g,c)

idVR= range(1,50)

tot=zip(idA,idV, idVR, cod,horaS,horaLl)

ip= 'fn3.oracle.virtual.uniandes.edu.co'
puerto= 1521
sid= 'prod'
usuario= 'ISIS2304B121620'
password= 'hvlnNayNipo2'
dsn= cx_Oracle.makedsn(ip,puerto,sid)
connection= cx_Oracle.connect(usuario, password, dsn)
cursor= connection.cursor()
cursor.executemany('insert into viajesrealizados(idavion, idvuelo, idrealizado, idaerolinea, fechasalida, fechallegada ) values (:1, :2, :3, :4, :5, :6)',tot)
connection.commit()

#RESERVAS
#idReserva
idR= range(3,37913)

#idViajero
idViaj= range(1,37913)

#idVuelo
idVuelo= range(1,37913)
v= idVuelo
nejec=[]
necon=[]

for i in range(1, len(idR)/len(idVuelo)+1):
	v= v+idVuelo

for i in idR:
	nejec.append(random.choice(range(1,5)))
	necon.append(random.choice(range(1,7)))

v=v[0:len(idR)]

tot=zip(idViaj,v, idR, nejec, necon)

ip= 'fn3.oracle.virtual.uniandes.edu.co'
puerto= 1521
sid= 'prod'
usuario= 'ISIS2304B121620'
password= 'hvlnNayNipo2'
dsn= cx_Oracle.makedsn(ip,puerto,sid)
connection= cx_Oracle.connect(usuario, password, dsn)
cursor= connection.cursor()
cursor.executemany('insert into reservas(idviajero, idvuelo, idreserva, numejec, numecon) values (:1, :2, :3, :4, :5)',tot)
connection.commit()

#TipoUsuario

#ntipo
ntipo=['administrador', 'viajero', 'remitente']

#tipo
t= [1,2,3]

tot= zip(ntipo,t)
ip= 'fn3.oracle.virtual.uniandes.edu.co'
puerto= 1521
sid= 'prod'
usuario= 'ISIS2304B121620'
password= 'hvlnNayNipo2'
dsn= cx_Oracle.makedsn(ip,puerto,sid)
connection= cx_Oracle.connect(usuario, password, dsn)
cursor= connection.cursor()
cursor.executemany('insert into tipousuario(ntipo,tipo) values (:1, :2)',tot)
connection.commit()

#USUARIOS
#id
v= range(1, 501)
#nombre 
w= range(1,len(v)+1)
j= lambda z: 'viajero'+str(z)
nom= map(j,w)

#email
w= range(1,len(v)+1)
j= lambda z: 'viajero'+str(z) + '@gmail.com'
email= map(j,w)

#tipo
tip=[]
for i in v:
	tip.append(random.choice(t))

tot= zip(nom, v, email, tip)

ip= 'fn3.oracle.virtual.uniandes.edu.co'
puerto= 1521
sid= 'prod'
usuario= 'ISIS2304B121620'
password= 'hvlnNayNipo2'
dsn= cx_Oracle.makedsn(ip,puerto,sid)
connection= cx_Oracle.connect(usuario, password, dsn)
cursor= connection.cursor()
cursor.executemany('insert into usuarios(nombre, identificacion, e_mail, tipo) values (:1, :2, :3, :4)',tot)
connection.commit()

#ADMINISTRADORES
#nombre
w= range(1,len(v)+1)
j= lambda z: 'administrador'+str(z)
nom= map(j,w)

#identificacion
v= range(1, 501)

#idadmin
z= range(1, 501)

tot= zip(nom, v, z)

ip= 'fn3.oracle.virtual.uniandes.edu.co'
puerto= 1521
sid= 'prod'
usuario= 'ISIS2304B121620'
password= 'hvlnNayNipo2'
dsn= cx_Oracle.makedsn(ip,puerto,sid)
connection= cx_Oracle.connect(usuario, password, dsn)
cursor= connection.cursor()
cursor.executemany('insert into administradores(nombre, identificacion, idadministrador) values (:1, :2, :3)',tot)
connection.commit()