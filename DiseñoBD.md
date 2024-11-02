erDiagram
    USUARIO {
        int id_usuario PK
        string nombre
        string direccion
        string telefono
        string correo_electronico
    }

    VEHICULO {
        string patente PK
        int id_usuario FK
        string color
        float ancho
        float alto
    }

    ESTACIONAMIENTO {
        int id_estacionamiento PK
        string patente_vehiculo FK
        datetime fecha_ingreso
        datetime fecha_egreso
        string estado
    }

    COBRANZA {
        int id_cobranza PK
        int id_estacionamiento FK
        float monto
        string moneda
        datetime fecha_hora
    }

    %%PRECIO {
        %%int id_precio PK
        %%int tiempo_en_horas
        %%float monto
        %%string moneda
    %%}

    MEMBRESIA {
        int id_membresia PK
        int id_usuario PK
        string tipo_membresia
        date fecha_vencimiento
    }

    USUARIO ||--o{ VEHICULO : "1 : N | registra | "
    VEHICULO ||--o{ ESTACIONAMIENTO : "1 : N | estaciona en | "
    ESTACIONAMIENTO ||--|| COBRANZA : "1 : 1 | genera | "
    USUARIO ||--o{ MEMBRESIA : "1 : 1 | tiene | "
