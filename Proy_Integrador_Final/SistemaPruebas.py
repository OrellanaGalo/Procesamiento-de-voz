from InteraccionUsuario.InteraccionUsuarios import InteraccionUsuario
from ProcesamientoLengNatural.InterpretacionLenguajeNatural import InterpretacionLenguajeNatural
from GestionEstacionamientoBD.gestion_estacionamiento import GestionEstacionamiento
from datetime import datetime

DBNAME = "postgres"
USER = "postgres"
PASSWORD = "postgres"
HOST = "localhost"  # O la dirección IP de tu servidor PostgreSQL
PORT = "5432"       # Puerto predeterminado de PostgreSQL

def calcularTiempoEstancia(fecha_ingreso, fecha_egreso):
    """
    Calcula el tiempo transcurrido entre la fecha de ingreso y la fecha de egreso en horas y minutos.
    """

    # Convierte las fechas en objetos datetime.
    ingreso = datetime.strptime(fecha_ingreso, "%Y-%m-%d %H:%M:%S")
    egreso = datetime.strptime(fecha_egreso, "%Y-%m-%d %H:%M:%S")

    diferencia = egreso - ingreso

    horas = diferencia.seconds // 3600
    minutos = (diferencia.seconds % 3600) // 60
    return horas, minutos

def main():
    interaccion = InteraccionUsuario()
    pln = InterpretacionLenguajeNatural()

    # Instancia para interactuar con la base de datos.
    gestion_bd = GestionEstacionamiento(
        db_name=DBNAME,
        user=USER,
        password=PASSWORD,
        host=HOST,
        port=PORT
    )

    try:
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
                            pln.text_to_speech("Por favor ingrese su solicitud")
                            pass  # Reinicia el flujo si hay datos inválidos
                        else:
                            # Registrar ingreso en la base de datos.
                            patente = datos_ingreso[0]
                            fecha_ingreso = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            if gestion_bd.registrarIngreso(patente, fecha_ingreso):
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
                        pln.text_to_speech("Por favor ingrese su solicitud")

                else:
                    print("Solicitud inválida, regresando a captura.")
            else:
                print("No se detectó voz, reiniciando.")
    finally:
        gestion_bd.cerrarConexion()

if __name__ == "__main__":
    main()
