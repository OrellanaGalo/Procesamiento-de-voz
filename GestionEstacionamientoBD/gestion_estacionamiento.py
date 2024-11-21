import psycopg2
from psycopg2 import sql
from datetime import datetime
from .credenciales import DBNAME, USER, PASSWORD, HOST, PORT

class GestionEstacionamiento:
    def __init__(self, db_name=DBNAME, user=USER, password=PASSWORD, host=HOST, port=PORT):
        try:
            self.conn = psycopg2.connect(
                dbname = db_name,
                user=user,
                password=password,
                host=host,
                port=port
            )
            self.cursor = self.conn.cursor()
            print("Conexion con la base de datos establecida.")
        except psycopg2.Error as e:
            print(f"Error al conectar a la base de datos: {e}")
            raise

    def ejecutarConsulta(self, consulta, parametros=(), commit=False):
        """Funcion generica para ejecutar consultas SQL."""
        try:
            self.cursor.execute(consulta, parametros)
            if commit:
                self.conn.commit()
            return self.cursor
        except psycopg2.Error as e:
            print(f"Error al realizar consulta: {e}")
            return None
        
    def registrarIngreso(self, patente, fecha_ingreso):
        """Registra un nuevo ingreso en la tabla de ESTACIONAMIENTO"""
        if self.consultaEstacionamientoActivo(patente):
            print("El vehiculo ya esta registrado en un estacionamiento activo.")
            return False
        
        consulta = """
            INSERT INTO ESTACIONAMIENTO (patente_vehiculo, fecha_ingreso, estado)
            VALUES (%s, %s, 'activo');
        """
        resultado = self.ejecutarConsulta(consulta, (patente, fecha_ingreso), commit=True)
        if resultado:
            print("Ingreso registrado correctamente.")
            return True
        return False

    def registrarEgreso(self, patente, fecha_egreso):
        """Registra el egreso actualizando el estado del estacionamiento."""
        consulta = """
            UPDATE ESTACIONAMIENTO
            SET fecha_egreso = %s, estado = 'finalizado'
            WHERE patente_vehiculo = %s AND estado = 'activo';
        """
        resultado = self.ejecutarConsulta(consulta, (fecha_egreso, patente), commit=True)
        if resultado and self.cursor.rowcount > 0:
            print("Retiro registrado correctamente.")
            return True
        else:
            print("No se encontro un estacionamiento activo para este vehiculo.")
            return False
    
    def consultaEstacionamientoActivo(self, patente):
        """Consulta si el vehiculo esta estacionado actualmente."""
        consulta = """
            SELECT id_estacionamiento, fecha_ingreso FROM ESTACIONAMIENTO
            WHERE patente_vehiculo = %s AND estado = 'activo';
        """
        resultado = self.ejecutarConsulta(consulta, (patente,))
        return resultado.fetchone() if resultado else None
    
    def obtenerFechaIngreso(self, patente):
        """Recupera la fecha de ingreso de un vehiculo basado en su patente."""
        consulta = """
        SELECT fecha_ingreso FROM estacionamiento WHERE patente = %s AND fecha_egreso IS NULL;
        """

        resultado = self.ejecutarConsulta(consulta, (patente,))
        return resultado.fetchone() if resultado else None
    
    def cerrarConexion(self):
        """Cierra la conexion con la base de datos."""
        self.cursor.close()
        self.conn.close
        print("Conexion a la base de datos cerrada.")