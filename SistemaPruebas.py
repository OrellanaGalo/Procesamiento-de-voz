from InteraccionUsuario.InteraccionUsuarios import InteraccionUsuario
from ProcesamientoLengNatural.InterpretacionLenguajeNatural import InterpretacionLenguajeNatural

def main():
    interaccion = InteraccionUsuario()
    pln = InterpretacionLenguajeNatural()
    i = True
    while i:
        #print("\t\t\t\t\tCapturando solicitud...\n")
        
        solicitud = interaccion.capturar_solicitud()
        #print("\t\t\t\t\tsolicitud realizada")
        if solicitud:
            pln.recibir_solicitud(solicitud)
            #print(f"\t\t\t\t\t Validar solicitud:{pln.validar_solicitud()}")
            if pln.validar_solicitud():
                
                pln.speech_to_text()
                tipo_solicitud = pln.determinar_tipo_solicitud()
                #print(f"\t\t\t\tTipo de solicitud: {tipo_solicitud}")
                if tipo_solicitud == "ingreso":
                    #print(f"Resultado solicitud:{pln.solicitud_ingreso()}")
                    solicitud = pln.solicitud_ingreso()
                    if solicitud == 1:
                        print("Reiniciando flujo de ingreso")
                        pass  # Reinicia el flujo si hay datos inválidos
                    else:
                        i = False
                        print(solicitud) # Consulta con BD
                elif tipo_solicitud == "egreso":
                    solicitud = pln.solicitud_egreso()
                    if solicitud == 1:
                        print("Reiniciando flujo de egreso")
                        pass
                    else:
                        i = False
                        print(solicitud) #Consulta con BD

                else:
                    print("No se entendió la solicitud.")
                    
            else:
                print("Solicitud inválida, regresando a captura.")
        else:
            print("No se detectó voz, reiniciando.")

if __name__ == "__main__":
    main()