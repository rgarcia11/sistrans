--ADMINISTRADORES
--1. unicidad de tuplas
--PK nueva
insert into administradores(nombre, identificacion, idadministrador)
values ("pepito", "123", "1230000");
--PK conocida
insert into administradores(nombre, identificacion, idadministrador)
values ("pepito", "1", "1");
--Misma PK
insert into administradores(nombre, identificacion, idadministrador)
values ("pepito", "123", "1230000");
--3. Chequeo
insert into administradores(nombre, identificacion, idadministrador)
values (null, null, "1230000");

--AEROLINEAS
--1. unicidad de tuplas
--PK nueva
insert into aerolineas(iatacod, nombre, pais) values ('abs', 'rrr', 'Colombia');
--PK conocida
insert into aerolineas(iatacod, nombre, pais) values ('AAA', 'dasda', 'Colombia');
--Misma PK
insert into aerolineas(iatacod, nombre, pais) values ('abs', 'rrr', 'Colombia');
--3. Chequeo
insert into aerolineas(iatacod, nombre, pais) values (null, null, 'Colombia');

--AEROPUERTOS
--1. unicidad de tuplas
--PK nueva
insert into aeropuertos(ciudad, capacidadaviones, iatacod, nombre) values ('Cali', 500, 'abc', 'dasda');
--PK conocida
insert into aeropuertos(ciudad, capacidadaviones, iatacod, nombre) values ('Cali', 500, 'AAA', 'dasda');
--Misma PK
insert into aeropuertos(ciudad, capacidadaviones, iatacod, nombre) values ('Cali', 500, 'abc', 'dasda');
--3. Chequeo
insert into aeropuertos(ciudad, capacidadaviones, iatacod, nombre) values (null, -500, null, null);

--AEROPUERTOSTIPOSVUELOS
--1. unicidad de tuplas
--PK nueva
insert into aeropuertostiposvuelos(idtipo, codaeropuerto) values (1, 'abc');
--PK conocida
insert into aeropuertostiposvuelos(idtipo, codaeropuerto) values (1, 'AAA');
--Misma PK
insert into aeropuertostiposvuelos(idtipo, codaeropuerto) values (1, 'abc');
--2. FK
--FK existente
insert into aeropuertostiposvuelos(idtipo, codaeropuerto) values (1, 'ABB');
--FK no existente
insert into aeropuertostiposvuelos(idtipo, codaeropuerto) values (5, 'zzz');

--AVIONES
--1. unicidad de tuplas
--PK nueva
insert into aviones(marca, modelo, numserie, idavion, anofabricacion, idaerolinea) values ('Boeing', '500A', 650, 50000, to_date(2014-06-15), 'AB');
--PK conocida
insert into aviones(marca, modelo, numserie, idavion, anofabricacion, idaerolinea) values ('Boeing', '500A', 1, 50000, to_date(2014-06-15), 'AB');
--Misma PK
insert into aviones(marca, modelo, numserie, idavion, anofabricacion, idaerolinea) values ('Boeing', '500A', 650, 50000, to_date(2014-06-15), 'AB');
--2. FK
--FK existente
insert into aviones(marca, modelo, numserie, idavion, anofabricacion, idaerolinea) values ('Boeing', '500A', 700, 5000000, to_date(2014-06-15), 'AB');
--FK no existente
insert into aviones(marca, modelo, numserie, idavion, anofabricacion, idaerolinea) values ('Boeing', '500A', 650, 50000, to_date(2014-06-15), 'zz');
--3. Chequeo
insert into aviones(marca, modelo, numserie, idavion, anofabricacion, idaerolinea) values ('ygasjdk', null, -650, 50000, null, null);

--AVIONESCARGA
--1. unicidad de tuplas
--PK nueva
insert into avionescarga(idavion, capacidad) values (50000, 40);
--PK conocida
insert into avionescarga(idavion, capacidad) values (1, 40);
--Misma PK
insert into avionescarga(idavion, capacidad) values (50000, 40);
--2. FK
--FK existente
insert into avionescarga(idavion, capacidad) values (5, 40);
--FK no existente
insert into avionescarga(idavion, capacidad) values (700000000, 40);
--3. Chequeo
insert into avionescarga(idavion, capacidad) values (null, -40);

--AVIONESPASAJEROS
--1. unicidad de tuplas
--PK nueva
insert into avionespasajeros(idavion, sillaseconomicas, sillasejecutivas) values (50000, 40, 2);
--PK conocida
insert into avionespasajeros(idavion, sillaseconomicas, sillasejecutivas) values (2, 40, 2);
--Misma PK
insert into avionespasajeros(idavion, sillaseconomicas, sillasejecutivas) values (50000, 40, 2);
--2. FK
--FK existente
insert into avionespasajeros(idavion, sillaseconomicas, sillasejecutivas) values (3, 40, 2);
--FK no existente
insert into avionespasajeros(idavion, sillaseconomicas, sillasejecutivas) values (500005555, 40, 2);
--3. Chequeo
insert into avionespasajeros(idavion, sillaseconomicas, sillasejecutivas) values (null, -40, -2);

--ENVIOS
--1. unicidad de tuplas
--PK nueva
insert into avionespasajeros(idavion, sillaseconomicas, sillasejecutivas) values (50000, 40, 2);
--PK conocida
insert into avionespasajeros(idavion, sillaseconomicas, sillasejecutivas) values (2, 40, 2);
--Misma PK
insert into avionespasajeros(idavion, sillaseconomicas, sillasejecutivas) values (50000, 40, 2);
--2. FK
--FK existente
insert into avionespasajeros(idavion, sillaseconomicas, sillasejecutivas) values (3, 40, 2);
--FK no existente
insert into avionespasajeros(idavion, sillaseconomicas, sillasejecutivas) values (500005555, 40, 2);
--3. Chequeo
insert into avionespasajeros(idavion, sillaseconomicas, sillasejecutivas) values (null, -40, -2);

--ENVIOS
--1. unicidad de tuplas
--PK nueva
insert into envios(idremitente, idvuelo, idenvio, volumen, peso, contenido) values (5, 40, 500000, 5, 2, 'fragil');
--PK conocida
insert into envios(idremitente, idvuelo, idenvio, volumen, peso, contenido) values (5, 40, 1, 5, 2, 'fragil');
--Misma PK
insert into envios(idremitente, idvuelo, idenvio, volumen, peso, contenido) values (5, 40, 500000, 5, 2, 'fragil');
--2. FK
--FK existente
insert into envios(idremitente, idvuelo, idenvio, volumen, peso, contenido) values (5, 40, 500000, 5, 2, 'fragil');
--FK no existente
insert into envios(idremitente, idvuelo, idenvio, volumen, peso, contenido) values (50000000, 40000000, 500000, 5, 2, 'fragil');
--3. Chequeo
insert into envios(idremitente, idvuelo, idenvio, volumen, peso, contenido) values (null, null, 4, -5, -2, null);

--NACIONALIDADES
--1. unicidad de tuplas
--PK nueva
insert into nacionalidades(idnacionalidad, nacionalidad) values (300, 'Holo');
--PK conocida
insert into nacionalidades(idnacionalidad, nacionalidad) values (1, 'Colombia');
--Misma PK
insert into nacionalidades(idnacionalidad, nacionalidad) values (300, 'Holo');
--3. Chequeo
insert into nacionalidades(idnacionalidad, nacionalidad) values (null, null);

--NACIONALIDADESREMITENTES
--1. unicidad de tuplas
--PK nueva
insert into nacionalidadesremitentes(idremitente, nacionalidad) values (5000000, 'holo');
--PK conocida
insert into nacionalidadesremitentes(idremitente, nacionalidad) values (2, 'holo');
--Misma PK
insert into nacionalidadesremitentes(idremitente, nacionalidad) values (5000000, 'holo');
--2. FK
--FK existente
insert into nacionalidadesremitentes(idremitente, nacionalidad) values (2, 'holo');
--FK no existente
insert into nacionalidadesremitentes(idremitente, nacionalidad) values (500330000, 'holo');
--3. Chequeo
insert into nacionalidadesremitentes(idremitente, nacionalidad) values (null, null);

--NACIONALIDADESVIAJEROS
--1. unicidad de tuplas
--PK nueva
insert into nacionalidadesviajeros(idviajero, nacionalidad) values (5000000, 'holo');
--PK conocida
insert into nacionalidadesviajeros(idviajero, nacionalidad) values (2, 'holo');
--Misma PK
insert into nacionalidadesviajeros(idviajero, nacionalidad) values (5000000, 'holo');
--2. FK
--FK existente
insert into nacionalidadesviajeros(idviajero, nacionalidad) values (5, 'holo');
--FK no existente
insert into nacionalidadesviajeros(idviajero, nacionalidad) values (5000056700, 'holo');
--3. Chequeo
insert into nacionalidadesviajeros(idviajero, nacionalidad) values (null, null);

--REMITENTES
--1. unicidad de tuplas
--PK nueva
insert into remitentes(nombre, identificacion, idremitente) values ('dasd', 5000000, 50000000);
--PK conocida
insert into remitentes(nombre, identificacion, idremitente) values ('dasd', 3, 3);
--Misma PK
insert into remitentes(nombre, identificacion, idremitente) values ('dasd', 5000000, 50000000);
--2. FK
--FK existente
insert into remitentes(nombre, identificacion, idremitente) values ('dasd', 5000000, 2);
--FK no existente
insert into remitentes(nombre, identificacion, idremitente) values ('dasd', 5000000, 5000456780000);
--3. Chequeo
insert into remitentes(nombre, identificacion, idremitente) values (null, -5000000, -50000000);

--RESERVAS

--TIPOSVUELOS

--TIPOUSUARIO

--USUARIOS

--VIAJEROS

--VIAJESREALIZADOS

--VUELOS

--VUELOSCARGA

--VUELOSPASAJEROS