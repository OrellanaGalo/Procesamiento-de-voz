# main.py
from InteraccionUsuario.InteraccionUsuarios import InteraccionUsuario
from ProcesamientoLengNatural.InterpretacionLenguajeNatural import InterpretacionLenguajeNatural

def main():
    # Instancia las clases
    interaccion = InteraccionUsuario()
    pln = InterpretacionLenguajeNatural()
    
    # Captura la solicitud de audio y pásala al módulo de PLN
    solicitud = interaccion.capturar_solicitud()
    if solicitud:
        pln.recibir_solicitud(solicitud)
        # A partir de aquí puedes procesar la solicitud en InterpretacionLenguajeNatural
        if pln.validar_solicitud():
            pln.speech_to_text()
            if pln.determinar_tipo_solicitud() == "egreso":
                pln.solicitud_egreso()
            elif pln.determinar_tipo_solicitud() == "ingreso":
                pln.solicitud_ingreso()
                pln.validar_datos_vehiculo
            else:
                return 1 # volver a interaccion usuario
        else:
            return 1 # Volver a inetraccion usuario
    else:
        return 1 #No se detecto interaccion

        

if __name__ == "__main__":
    main()


    """
    validar intencion -> invalida, return 1, vuelve grupo 1
        |
       valida
        |
    determinar Tipo de solicitud? -> desconocido, return 1, vuelve grupo 1
        |                   |
    Ingreso                 |------------------------------------------------------------_>egreso
        |                                                                                     |
Pedir datos Vehiculo      <-|                                                           Pedir datos vehiculo?      <-|
        |                   |                                                                 |                      |
    validos? -> invalido, vuelve e pedir datos                                              Validos? -> invalido, vuelve a pedir datos
        |                                                                                     |
    valido                                                                                  valido
        |                                                                                     |
    Pedir duracion        <-|                                                                 |      
        |                   |                                                                 |                              
    validos? -> invalido, vuelve e pedir datos                                                |              
        |                                                                                     |      
    valido                                                                                    |      
        |                                                                                     |
        |-> Confirmar Datos <-----------------------------------------------------------------|
                |
            Return a pricipal
"""


        

