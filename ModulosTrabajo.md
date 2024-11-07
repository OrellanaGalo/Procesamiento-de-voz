# Modulos de Trabajo
-
```mermaid
graph TD
    subgraph Grupo1 [Grupo 1: Interacción con Usuario]
        A1[Ingreso de Solicitud]
        A2[Confirmación de Salida]
    end

    subgraph Grupo2 [Grupo 2: Procesamiento de Lenguaje Natural]
        B1[Análisis de Intención]
        B2[Extracción de Parámetros]
    end

    subgraph Grupo3 [Grupo 3: Base de Datos y Consultas]
        C1[Validación de Datos]
        C2[Operaciones en BD]
    end

    subgraph Grupo4 [Grupo 4: Generación de Respuestas y TTS]
        D1[Generación de Respuesta]
        D2[Text-to-Speech]
    end

    subgraph Grupo5 [Grupo 5: Logging y Métricas]
        E1[Registro de Interacciones]
        E2[Análisis y Optimización]
    end

    %% Interconexiones entre módulos y grupos
    A1 --> B1
    B1 --> B2
    B2 --> C1
    C1 -->|Datos Válidos| C2
    C1 -->|Datos Inválidos| A1
    C2 --> D1
    D1 --> D2
    D2 --> A2
    A2 --> E1
    E1 --> E2
