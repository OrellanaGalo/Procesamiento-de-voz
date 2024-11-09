import os
from gtts import gTTS
import speech_recognition as sr
import numpy as np
import wave
import time
import InteraccionUsuario.InteraccionUsuarios as InteraccionUsuario
import re

class InterpretacionLenguajeNatural:
    def __init__(self):
        self.solicitud = None  # Contendrá el audio capturado
        self.tipo_solicitud = None  # Tipo de solicitud ('ingreso', 'egreso')
        self.texto_transcrito = ""  # Texto transcrito del audio
        self.consulta = [] #Contendra la consulta que se le hace a la BD
        self.duracion_valida = False
        self.datos_vehiculo_valido = False

    def reset(self):
        self.solicitud = None  # Contendrá el audio capturado
        self.tipo_solicitud = None  # Tipo de solicitud ('ingreso', 'egreso')
        self.texto_transcrito = ""  # Texto transcrito del audio
        self.consulta = [] #Contendra la consulta que se le hace a la BD
        self.duracion_valida = False
        self.datos_vehiculo_valido = False

    def recibir_solicitud(self, solicitud):
        """Recibe el audio capturado de InteraccionUsuario y lo almacena."""
        self.solicitud = solicitud
        print("\t\t\tSolicitud recibida en InterpretacionLenguajeNatural.")

    def guardar_audio_temporal(self, filename="temp_audio.wav"):
        """Guarda self.solicitud en un archivo WAV temporal."""
        with wave.open(filename, 'wb') as wf:
            wf.setnchannels(1)  # Mono
            wf.setsampwidth(2)  # Tamaño de muestra de 16 bits (2 bytes)
            wf.setframerate(16000)  # Frecuencia de muestreo de 16 kHz
            wf.writeframes(b''.join(self.solicitud))
        return filename
            
    def validar_solicitud(self):
        """Valida si la solicitud de audio es válida (no es ruido ambiente)."""
        if not self.solicitud:
            print("No hay datos de audio grabados.")
            return False
        audio_data = np.frombuffer(b''.join(self.solicitud), dtype=np.int16)
        energy = np.sum(np.abs(audio_data)) / len(audio_data)
        if energy < 2000:
            print("La energía de la solicitud es demasiado baja, es posible que solo haya ruido ambiente.")
            return False
        duration = len(self.solicitud) * 2048 / 16000
        if duration < 1:
            print("La duración de la solicitud es demasiado corta.")
            return False
        return True

    def determinar_tipo_solicitud(self):
        """Determina si la solicitud es para Ingreso o Egreso."""
        egreso = ["salir", "egreso", "retirar"]
        ingreso = ["ingresar", "estacionar", "entrada"]
        if not self.texto_transcrito:
            print("No hay texto para analizar.")
            return None
        if any(palabra in self.texto_transcrito.lower() for palabra in egreso):
            self.tipo_solicitud = "egreso"
        elif any(palabra in self.texto_transcrito.lower() for palabra in ingreso):
            self.tipo_solicitud = "ingreso"
        else:
            self.tipo_solicitud = "desconocido"
        return self.tipo_solicitud

    def speech_to_text(self):
        """Convierte el audio en texto usando Google Speech-to-Text."""
        filename = self.guardar_audio_temporal()
        recognizer = sr.Recognizer()
        with sr.AudioFile(filename) as source:
            audio = recognizer.record(source)
        try:
            self.texto_transcrito = recognizer.recognize_google(audio, language="es-ES")
        except sr.UnknownValueError:
            print("No se pudo entender el audio.")
            self.texto_transcrito = None
        except sr.RequestError as e:
            print(f"Error al conectarse al servicio de reconocimiento de voz: {e}")
            self.texto_transcrito = None
        finally:
            os.remove(filename)
        return self.texto_transcrito
    
    def speech_to_text2(self):
        """Convierte el audio en texto usando Google Speech-to-Text."""
        
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Hablar ahora")
            audio = recognizer.listen(source)


        try:
            self.texto_transcrito = recognizer.recognize_google(audio, language="es-ES")
        except sr.UnknownValueError:
            print("No se pudo entender el audio.")
            self.texto_transcrito = None
        except sr.RequestError as e:
            print(f"Error al conectarse al servicio de reconocimiento de voz: {e}")
            self.texto_transcrito = None
        
        return self.texto_transcrito

    def analisis_intension(self):
        """Realiza el análisis de la intención del usuario y gestiona el flujo."""
        if not self.texto_transcrito:
            self.text_to_speech("No se pudo entender la solicitud Intente nuevamente.")
            return 1

        tipo_solicitud = self.determinar_tipo_solicitud()
        
        if tipo_solicitud == "ingreso":
            self.solicitud_ingreso()
        elif tipo_solicitud == "egreso":
            self.solicitud_egreso()
        else:
            self.text_to_speech("No entendí su solicitud. ¿Desea ingresar o retirar el vehículo?")

    def solicitud_ingreso(self):
        """Gestiona el flujo de ingreso: solicita tipo de vehículo, patente y duración."""
        self.text_to_speech("Por favor, indique su patente.")
        print("texto: ",self.speech_to_text2())
        datos_vehiculo = self.validar_datos_vehiculo()

        if not self.datos_vehiculo_valido:
            print(f"\t\t\t\t\t\t\t\t\t\n\n Datos vehiculo incorrectos\n\n")
            self.text_to_speech("Datos del vehículo incorrectos. Intente nuevamente.")
            return 1  # Retornar control al flujo principal en caso de datos incorrectos

        self.consulta.append(datos_vehiculo)

        self.text_to_speech("Indique la duración del estacionamiento.")
        print("texto: ",self.speech_to_text2())

        self.consulta.append(self.validar_duracion())

        self.text_to_speech("Todo correcto")

        #enviar solicitud con los datos a la BD
        return self.consulta

    def solicitud_egreso(self):
        """Gestiona el flujo de egreso: solicita confirmación y patente."""
        self.text_to_speech("Confirmo que desea retirar su vehículo. Por favor, indique su patente.")
        print(f"texto: {self.speech_to_text2()}")
        datos_vehiculo = self.validar_datos_vehiculo()
        return datos_vehiculo

    def validar_datos_vehiculo(self): #Se puede agregar que verifique el tipo de vehiculo
        """Valida la patente extraída del texto, permitiendo diferentes formatos."""
        print(f"Texto transcrito: {self.texto_transcrito}")
        
        # Expresión regular para encontrar la patente en diferentes formatos
        patron = r'\b([a-zA-Z]\s*[a-zA-Z]?\s*[a-zA-Z]?\s*\d\s*\d\s*\d)\b'
        coincidencia = re.search(patron, self.texto_transcrito, re.IGNORECASE)
        
        if coincidencia:
            # Eliminar espacios y convertir a minúsculas
            patente = coincidencia.group(1).replace(" ", "").lower()
            self.datos_vehiculo_valido = True
            return patente
        else:
            self.datos_vehiculo_valido = False
            return None

    def validar_duracion(self):
        """Valida la duración del estacionamiento y extrae la hora en formato hh:mm:ss."""
        print(f"\t\t\t\t\t\n\n Texto de tiempo: {self.texto_transcrito}")
        
        # Expresión regular para encontrar horas y minutos
        patron = r'(\d+)\s*(hora|horas|h)?\s*(\d+)?\s*(minuto|minutos|m)?'
        coincidencia = re.search(patron, self.texto_transcrito, re.IGNORECASE)
        
        if coincidencia:
            horas = int(coincidencia.group(1)) if coincidencia.group(1) else 0
            minutos = int(coincidencia.group(3)) if coincidencia.group(3) else 0
            segundos = 0  # Puedes ajustar esto si necesitas manejar segundos también
            
            self.duracion_valida = True
            return f"{horas:02}:{minutos:02}:{segundos:02}"
        else:
            self.duracion_valida = False
            return None

    def text_to_speech(self, texto):
        """Convierte texto a voz usando gTTS y reproduce el archivo generado."""
        tts = gTTS(text=texto, lang='es')
        tts.save("respuesta.mp3")
        os.system("mpg123 respuesta.mp3")  # Requiere tener instalado mpg123


