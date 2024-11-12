from InteraccionUsuario.InteraccionUsuarios import InteraccionUsuario
from ProcesamientoLengNatural.InterpretacionLenguajeNatural import InterpretacionLenguajeNatural
from GestionEstacionamientoBD import gestionEstacionamientoBD
from datetime import datetime

def main():
    interaccion = InteraccionUsuario()
    pln = InterpretacionLenguajeNatural()

    # Instancia para interactuar con la base de datos.
    gestion_bd = gestionEstacionamientoBD()
    i = True

    while i:
        solicitud = interaccion.capturar_solicitud()
        if solicitud:
            pln.recibir_solicitud(solicitud)
            if pln.validar_solicitud():
                pln.speech_to_text()
                tipo_solicitud = pln.determinar_tipo_solicitud()

                if tipo_solicitud == "ingreso":
                    datos_ingreso = pln.solicitud_ingreso()
                    if datos_ingreso == 1:
                        print("Reiniciando flujo de ingreso")
                        pass  # Reinicia el flujo si hay datos inválidos
                    else:
                        # Registrar ingreso en la base de datos.
                        patente = datos_ingreso[0]
                        id_usuario = 1 # Aca se debe definir el ID de usuario correspondiente.
                        fecha_ingreso = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        if gestion_bd.registrarIngreso(patente, id_usuario, fecha_ingreso):
                            print("Ingreso registrado en la base de datos.")
                        i = False

                elif tipo_solicitud == "egreso":
                    patente_egreso = pln.solicitud_egreso()
                    if patente_egreso == 1:
                        print("Reiniciando flujo de egreso")
                        pass
                    else:
                        # Registrar egreso en la base de datos.
                        fecha_egreso = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        if gestion_bd.registrarEgreso(patente_egreso, fecha_egreso):
                            print("Retiro registrado en la base de datos.")
                        i = False
                else:
                    print("No se entendió la solicitud.")
                    
            else:
                print("Solicitud inválida, regresando a captura.")
        else:
            print("No se detectó voz, reiniciando.")

if __name__ == "__main__":
    main()