# Procesamiento Lenguaje Natural
-
``` mermaid
graph TD
    W:::method2
    W[Conexion Con Interaccion Usuario]--> A[a]
    A:::method
    A[Iniciar Interacción] --> B{Validacion de intencion}
    B-->|Valida|Z[Speech to text]
    Z --> C{¿Ingreso o Egreso?}

    B --> |Invalida|W
    D:::method
    C -->P[text to speech]
    P-->|Ingreso|D[Solicitar tipo de vehículo y patente]
    I:::method
    P -->|Egreso|I[Solicitar datos del vehiculo]
    I --> V{Validar datos del vehiculo}
    
    
    D --> E{Validar datos del vehículo}
    F:::method
    E --> |Valido|F[Solicitar duración del estacionamiento]
    E --> |Invalido|D
    F --> G{Validar duración del estacionamiento}
    H:::method
    G --> |Valido|H[Confirmar datos]
    G --> |Invalido|F

    X:::method2
    H --> |Consulta|X[Base de Datos]
    X --> |Respuesta|H

    Z:::method
    V --> |Valido|H
    
        

    
    Y:::method2
    H --> Y[Generacion de Respuesta]
   
    P -->|Desconocido|L[No entender solicitud, solicitar de nuevo]
    L --> W

 classDef method fill:#f9f,stroke:#333,stroke-width:2px;
 classDef method2 fill:#aaa,stroke:#444,stroke-width:2px;
```
