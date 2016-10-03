CREATE TABLE aerolineas
(iataCod varchar(2),
nombre varchar(50) NOT NULL,
pais varchar(50) NOT NULL,
PRIMARY KEY(iataCod)
);

CREATE TABLE aviones
(marca varchar(50) NOT NULL,
modelo varchar(50) NOT NULL,
numSerie int,
idAvion int,
anoFabricacion DATE NOT NULL,
idAerolinea varchar(2),
PRIMARY KEY(idAvion),
CONSTRAINT ck_marca CHECK(marca IN ('Airbus','Boeing')),
CHECK(numSerie>0),
FOREIGN KEY(idAerolinea) REFERENCES aerolineas(iataCod)
);

CREATE TABLE avionesCarga
(idAvion int,
capacidad int NOT NULL,
FOREIGN KEY(idAvion) REFERENCES aviones(idAvion),
PRIMARY KEY(idAvion),
CHECK(capacidad>0)
);

CREATE TABLE avionesPasajeros
(idAvion int,
sillasEconomicas int NOT NULL,
sillasEjecutivas int NOT NULL,
FOREIGN KEY(idAvion) REFERENCES aviones(idAvion),
PRIMARY KEY(idAvion),
CHECK(sillasEconomicas>0),
CHECK(sillasEjecutivas>0)
);

CREATE TABLE aeropuertos
(ciudad varchar(50) NOT NULL,
capacidadAviones int NOT NULL,
iataCod varchar(3),
nombre varchar(50) NOT NULL,
PRIMARY KEY(iataCod),
CHECK(capacidadAviones>0)
);

CREATE TABLE tiposVuelos
(idTipo int,
nombre varchar(20) NOT NULL,
PRIMARY KEY(idTipo)
);

CREATE TABLE vuelos
(idVuelo int,
idAerolinea varchar(2) NOT NULL,
idNumVuelo int NOT NULL ,
aeropuertoSalida varchar(3) NOT NULL,
aeropuertoLlegada varchar(3) NOT NULL,
horaSalida DATE NOT NULL,
horaLlegada DATE NOT NULL,
fecha DATE NOT NULL,
frecuencia int NOT NULL,
distancia NUMBER(10,2) NOT NULL,
duracion NUMBER(10,2) NOT NULL,
tipoVuelo int NOT NULL,
idAvion int NOT NULL,
FOREIGN KEY(aeropuertoSalida) REFERENCES aeropuertos(iataCod),
FOREIGN KEY(aeropuertoLlegada) REFERENCES aeropuertos(iataCod),
FOREIGN KEY(idAerolinea) REFERENCES aerolineas(iataCod),
FOREIGN KEY(tipoVuelo) REFERENCES tiposVuelos(idTipo),
FOREIGN KEY(idAvion) REFERENCES aviones(idAvion),
CHECK (frecuencia>0),
CHECK (distancia>0),
CHECK (duracion>0),
PRIMARY KEY(idVuelo)
);

CREATE TABLE vuelosCarga
(idVuelo int,
costoDensidad NUMBER(10,2) NOT NULL,
FOREIGN KEY(idVuelo) REFERENCES vuelos(idVuelo),
PRIMARY KEY(idVuelo),
CHECK(costoDensidad>0)
);

CREATE TABLE vuelosPasajeros
(idVuelo int,
costoEconomico NUMBER(10,2) NOT NULL,
costoEjecutivo NUMBER(10,2) NOT NULL,
FOREIGN KEY(idVuelo) REFERENCES vuelos(idVuelo),
PRIMARY KEY(idVuelo),
CHECK(costoEconomico>0),
CHECK(costoEjecutivo>0)
);

CREATE TABLE aeropuertosTiposVuelos
(idTipo int,
codAeropuerto varchar(3),
FOREIGN KEY(idTipo) REFERENCES tiposVuelos(idTipo),
FOREIGN KEY(codAeropuerto) REFERENCES aeropuertos(iataCod),
CONSTRAINT pk_aeropuertosTiposVuelos PRIMARY KEY(idTipo,codAeropuerto)
);

CREATE TABLE viajesRealizados
(fecha DATE NOT NULL,
hora DATE NOT NULL,
idAvion int NOT NULL,
idVuelo int,
FOREIGN KEY(idVuelo) REFERENCES vuelos(idVuelo),
PRIMARY KEY(idVuelo),
FOREIGN KEY(idAvion) REFERENCES aviones(idAvion)
);

CREATE TABLE viajeros
(nombre varchar(50) NOT NULL,
identificacion varchar(50) NOT NULL,
idViajero int,
PRIMARY KEY(idViajero)
);

CREATE TABLE nacionalidades
(idNacionalidad int,
nacionalidad varchar(50) NOT NULL,
PRIMARY KEY(idNacionalidad)
);

CREATE TABLE nacionalidadesViajeros
(idViajero int NOT NULL,
nacionalidad int NOT NULL,
CONSTRAINT pk_nacionalidadesViajeros PRIMARY KEY(idViajero,nacionalidad),
FOREIGN KEY(idViajero) REFERENCES viajeros(idViajero),
FOREIGN KEY(nacionalidad) REFERENCES nacionalidades(idNacionalidad)
);

CREATE TABLE remitentes
(nombre varchar(50) NOT NULL,
identificacion varchar(50) NOT NULL,
idRemitente int,
PRIMARY KEY(idRemitente)
);

CREATE TABLE nacionalidadesRemitentes
(idRemitente int NOT NULL,
nacionalidad int NOT NULL,
CONSTRAINT pk_nacionalidadesRemitentes PRIMARY KEY(idRemitente,nacionalidad),
FOREIGN KEY(idRemitente) REFERENCES remitentes(idRemitente),
FOREIGN KEY(nacionalidad) REFERENCES nacionalidades(idNacionalidad)
);

CREATE TABLE reservas
(idViajero int NOT NULL,
idVuelo int NOT NULL,
idReserva int,
PRIMARY KEY(idReserva),
FOREIGN KEY(idViajero) REFERENCES viajeros(idViajero),
FOREIGN KEY(idVuelo) REFERENCES vuelos(idVuelo)
);

CREATE TABLE envios
(idRemitente int NOT NULL,
idVuelo int NOT NULL,
idEnvio int,
volumen NUMBER(10,2) NOT NULL,
peso NUMBER(10,2) NOT NULL,
contenido NUMBER(10,2) NOT NULL,
PRIMARY KEY(idEnvio),
FOREIGN KEY(idRemitente) REFERENCES remitentes(idRemitente),
FOREIGN KEY(idVuelo) REFERENCES vuelos(idVuelo)
);


