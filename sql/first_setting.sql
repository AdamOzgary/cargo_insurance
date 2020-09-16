CREATE DATABASE cargo;

CREATE TABLE history 
(
    cargoId SERIAL PRIMARY KEY, 
    cargoName varchar(30),
    cargoType varchar(30), 
    cargoDate date, 
    decCost real, 
    insCost real
);

CREATE USER cargouser WITH PASSWORD 'qwerty';
GRANT All PRIVILEGES ON DATABASE cargo TO cargouser;