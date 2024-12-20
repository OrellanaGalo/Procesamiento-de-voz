import pyaudio
import numpy as np
import wave
import time
#import ProcesamientoLengNatural.InterpretacionLenguajeNatural as PNL
#import speech_recognition as sr Grupo ILN


class InteraccionUsuario:
    def __init__(self):
        self.solicitud = []  # Aquí almacenaremos la solicitud actual
        self.tipo_solicitud = ""
        # Configuración de parámetros de audio
        self.FORMAT = pyaudio.paInt16  # Formato de 16-bit PCM
        self.CHANNELS = 1  # Mono
        self.RATE = 16000  # Frecuencia de muestreo
        self.CHUNK = 2048  # Tamaño del bloque
        self.SILENCE_THRESHOLD = 6000  # Umbral de energía para detectar voz (ajustable)
        self.RECORD_SECONDS = 2  # Duración máxima de la grabación
        self.OUTPUT_FILENAME = "audio_output.wav"
        # Inicialización de PyAudio
        self.p = pyaudio.PyAudio()

    def capturar_solicitud(self):
        """
        Captura la entrada de voz del usuario. Si el nivel de energia es mayor al umbra,
        se graba durante 5 segundos.
        """
        try:
            # Abre el stream de entrada de PyAudio
            stream = self.p.open(format=self.FORMAT,
                                channels=self.CHANNELS,
                                rate=self.RATE,
                                input=True,
                                frames_per_buffer=self.CHUNK)
            
            print("Esperando voz...")
            
            self.solicitud = []  # Inicializar self.solicitud para almacenar los frames de audio
            recording = False  # Estado de grabación
            start_time = None  # Tiempo de inicio de la grabación
            max_wait_time = 10 # Tiempo maximo para detectar voz.
            global_start = time.time() # Marca el tiempo de inicio global para el metodo.

            while True:
                # Lee un bloque de datos de audio desde el micrófono
                data = stream.read(self.CHUNK, exception_on_overflow=False)
                
                # Convierte los datos de audio a una matriz numpy
                audio_data = np.frombuffer(data, dtype=np.int16)
                
                # Calcula la energía de la señal
                energy = np.sum(np.abs(audio_data)) / len(audio_data)
                
                # Inicia la grabación si se detecta energía por encima del umbral
                if energy > self.SILENCE_THRESHOLD and not recording:
                    print("Voz detectada, comenzando grabación...")
                    recording = True
                    self.solicitud = []  # Reinicia self.solicitud para almacenar solo la grabación actual
                    start_time = time.time()  # Marca el tiempo de inicio de la grabación

                # Almacena los datos de audio si está en modo grabación
                if recording:
                    self.solicitud.append(data)  # Almacena el bloque de audio en self.solicitud

                    # Termina la grabación si se alcanza la duración máxima
                    if time.time() - start_time > self.RECORD_SECONDS:
                        print("Tiempo de grabación alcanzado. Terminando grabación.")
                        break
                
                # Detiene la espera si excede el tiempo maximo global.
                if time.time() - global_start > max_wait_time:
                    print("Tiempo maximo de espera alcanzado. No se detecto voz.")
                    break

            # Finaliza el stream y cierra el recurso de audio
            stream.stop_stream()
            stream.close()

            if self.solicitud:
                print("Grabación almacenada en self.solicitud.")
                self.guardar_audio()
                return self.solicitud
            else:
                print("No se detectó voz válida.")
                return None
        except Exception as e:
            print(f"Error al capturar voz: {e}")
            return None
        
    def guardar_audio(self, filename="audio_output.wav"):
        """
        Guarda el contenido de self.solicitud en un archivo de audio .wav.
        """
        if not self.solicitud:
            print("No hay audio en self.solicitud para guardar.")
            return
            
        # Configura el archivo de salida .wav
        with wave.open(filename, 'wb') as wf:
            wf.setnchannels(self.CHANNELS)
            wf.setsampwidth(self.p.get_sample_size(self.FORMAT))
            wf.setframerate(self.RATE)
            wf.writeframes(b''.join(self.solicitud))
            
        print(f"Archivo de audio guardado como: {filename}")


    