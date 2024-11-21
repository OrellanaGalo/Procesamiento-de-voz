-- Crear esquema público (si no existe)
CREATE SCHEMA IF NOT EXISTS public;

-- Tabla: USUARIO
CREATE TABLE public.usuario (
    id_usuario SERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    direccion VARCHAR(255),
    telefono VARCHAR(15),
    correo_electronico VARCHAR(255) UNIQUE NOT NULL
);

-- Tabla: VEHICULO
CREATE TABLE public.vehiculo (
    patente VARCHAR(15) PRIMARY KEY,
    id_usuario INT REFERENCES public.usuario (id_usuario) ON DELETE CASCADE,
    color VARCHAR(30),
    ancho FLOAT,
    alto FLOAT
);

-- Tabla: ESTACIONAMIENTO
CREATE TABLE public.estacionamiento (
    id_estacionamiento SERIAL PRIMARY KEY,
    patente_vehiculo VARCHAR(15) REFERENCES public.vehiculo (patente) ON DELETE CASCADE,
    fecha_ingreso TIMESTAMP NOT NULL,
    fecha_egreso TIMESTAMP,
    estado VARCHAR(20) NOT NULL
);

-- Tabla: COBRANZA
CREATE TABLE public.cobranza (
    id_cobranza SERIAL PRIMARY KEY,
    id_estacionamiento INT REFERENCES public.estacionamiento (id_estacionamiento) ON DELETE CASCADE,
    monto FLOAT NOT NULL,
    moneda VARCHAR(10),
    fecha_hora TIMESTAMP NOT NULL
);

-- Tabla: MEMBRESIA
CREATE TABLE public.membresia (
    id_membresia SERIAL PRIMARY KEY,
    id_usuario INT REFERENCES public.usuario (id_usuario) ON DELETE CASCADE,
    tipo_membresia VARCHAR(50),
    fecha_vencimiento DATE NOT NULL
);

-- Crear restricciones adicionales para relaciones del diagrama ER
ALTER TABLE public.usuario ADD CONSTRAINT usuario_correo_unico UNIQUE (correo_electronico);
