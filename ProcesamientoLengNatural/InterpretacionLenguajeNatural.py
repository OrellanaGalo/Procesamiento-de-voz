import os
from gtts import gTTS
import speech_recognition as sr
import numpy as np
import wave
import time
import InteraccionUsuario.InteraccionUsuarios as InteraccionUsuario

class InterpretacionLenguajeNatural:
    def __init__(self):
        self.solicitud = None  # Contendrá el audio capturado
        self.tipo_solicitud = None  # Tipo de solicitud ('ingreso', 'egreso')
        self.texto_transcrito = ""  # Texto transcrito del audio
   
    def guardar_audio_temporal(self, filename="temp_audio.wav"):
        """Guarda self.solicitud en un archivo WAV temporal."""
        with wave.open(filename, 'wb') as wf:
            wf.setnchannels(1)  # Mono
            wf.setsampwidth(2)  # Tamaño de muestra de 16 bits (2 bytes)
            wf.setframerate(16000)  # Frecuencia de muestreo de 16 kHz
            wf.writeframes(b''.join(self.solicitud))
        return filename

    def recibir_solicitud(self, solicitud):
        """
        Recibe el audio capturado (solicitud) de InteraccionUsuario y lo almacena.
        """
        self.solicitud = solicitud
        print("Solicitud recibida en InterpretacionLenguajeNatural.")    
            
    def validar_solicitud(self):
        """
        Valida si la solicitud de audio es válida.
        Contiene voz en lugar de solo ruido ambiente.
        """
        # Verificar que self.solicitud no esté vacía
        if not self.solicitud:
            print("No hay datos de audio grabados.")
            return False

        # Convertir self.solicitud en un arreglo numpy para procesarlo
        audio_data = np.frombuffer(b''.join(self.solicitud), dtype=np.int16)

        # Verificar que la energía de la señal sea suficiente
        energy = np.sum(np.abs(audio_data)) / len(audio_data)
        print(f"Energía promedio de la solicitud: {energy}")
        if energy < 2000:
            print("La energía de la solicitud es demasiado baja, es posible que solo haya ruido ambiente.")
            return False

        # Verificar que el tiempo de grabación sea mayor a 1 segundo
        duration = len(self.solicitud) * 2048 / 16000  # Ajustar con CHUNK y RATE del sistema de captura
        print(f"Duración de la solicitud: {duration} segundos")
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

        # Analizar si el texto contiene palabras clave de ingreso o egreso
        if any(palabra in self.texto_transcrito.lower() for palabra in egreso):
            self.tipo_solicitud = "egreso"
            print("Solicitud de egreso detectada.")
        elif any(palabra in self.texto_transcrito.lower() for palabra in ingreso):
            self.tipo_solicitud = "ingreso"
            print("Solicitud de ingreso detectada.")
        else:
            self.tipo_solicitud = "desconocido"
            print("Tipo de solicitud desconocido.")
        return self.tipo_solicitud

    def speech_to_text(self):
        """
        Convierte el audio en texto usando Google Speech-to-Text.
        """
        filename = self.guardar_audio_temporal()  # Guarda el archivo temporal
        recognizer = sr.Recognizer()

        with sr.AudioFile(filename) as source:
            audio = recognizer.record(source)
        try:
            self.texto_transcrito = recognizer.recognize_google(audio, language="es-ES")
            print("Texto transcrito:", self.texto_transcrito)
        except sr.UnknownValueError:
            print("No se pudo entender el audio.")
            self.texto_transcrito = None
        except sr.RequestError as e:
            print(f"Error al conectarse al servicio de reconocimiento de voz: {e}")
            self.texto_transcrito = None
        finally:
            pass
            #os.remove(filename)  # Elimina el archivo temporal después de su uso
        return self.texto_transcrito

    def analisis_intension(self):
        """Realiza el análisis de la intención del usuario y gestiona el flujo."""
        if not self.texto_transcrito:
            self.texto_a_voz("No se pudo entender la solicitud Intente nuevamente.")
            return 1

        tipo_solicitud = self.determinar_tipo_solicitud()
        
        if tipo_solicitud == "ingreso":
            self.solicitud_ingreso()
        elif tipo_solicitud == "egreso":
            self.solicitud_egreso()
        else:
            self.texto_a_voz("No entendí su solicitud. ¿Desea ingresar o retirar el vehículo?")

    def solicitud_ingreso(self):
        """Gestiona el flujo de ingreso: solicita tipo de vehículo, patente y duración."""
        self.texto_a_voz("Por favor, indique el tipo de vehículo y su patente.")

        iu = InteraccionUsuario.InteraccionUsuario
        self.solicitud = iu.capturar_solicitud(self)
        self.speech_to_text()# Captura los datos de tipo y patente
        
        self.validar_datos_vehiculo()
        
        if not self.datos_vehiculo_valido:
            self.texto_a_voz("Datos del vehículo incorrectos. Intente nuevamente.")
            self.solicitud_ingreso()  # Repite si la validación falla

        self.texto_a_voz("Indique la duración del estacionamiento.")
        self.speech_to_text()
        self.validar_duracion()

    def solicitud_egreso(self):
        """Gestiona el flujo de egreso: solicita confirmación y patente."""
        self.texto_a_voz("Confirmo que desea retirar su vehículo. Por favor, indique su patente.")
        self.speech_to_text()
        self.validar_datos_vehiculo()

    def validar_datos_vehiculo(self):
        """Valida el tipo de vehículo y patente extraídos del texto."""
        # Implementa lógica de validación para tipo de vehículo y patente
        self.datos_vehiculo_valido = "ABC123" in self.texto_transcrito  # Ejemplo de validación simplificada
        print(self.datos_vehiculo_valido)
        return self.datos_vehiculo_valido

    def validar_duracion(self):
        """Valida la duración del estacionamiento."""
        # Implementa la lógica de validación para la duración; se debe extraer una cantidad de tiempo
        if "hora" in self.texto_transcrito or "minuto" in self.texto_transcrito:
            self.duracion_valida = True
        else:
            self.duracion_valida = False
        return self.duracion_valida

    def texto_a_voz(self, texto):
        """Convierte texto a voz usando gTTS y reproduce el archivo generado."""
        tts = gTTS(text=texto, lang='es')
        tts.save("respuesta.mp3")
        os.system("mpg123 respuesta.mp3")  # Requiere tener instalado mpg123

