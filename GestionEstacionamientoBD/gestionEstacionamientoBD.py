import sqlite3
from datetime import datetime

class GestionEstacionamientoBD:
    def __init__(self, db_path="estacionamiento.db"):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def registrarIngreso(self, patente, id_usuario, fecha_ingreso):
        """Registra un nuevo ingreso en la tabla de ESTACIONAMIENTO"""
        try:
            # Verifica si el vehiculo ya esta estacionado.
            self.cursor.execute("""
                SELECT estado FROM ESTACIONAMIENTO WHERE patente_vehiculo = ? AND estado = 'activo';
            """, (patente,))
            if self.cursor.fetchone():
                print("El vehiculo ya esta registrado en un estacionamiento activo.")
                return False
            
            # Inserta el nuevo registro de estacionamiento.
            self.cursor.execute("""
                INSERT INTO ESTACIONAMIENTO (patente_vehiculo, fecha_ingreso, estado)
                VALUES (?, ?, 'activo');
            """, (patente, fecha_ingreso))
            self.conn.commit()
            print("Ingreso registrado correctamente.")
            return True
        except sqlite3.Error as e:
            print(f"Error al registrar ingreso: {e}")
            return False

    def registrarEgreso(self, patente, fecha_egreso):
        """Registra el egreso actualizando el estado del estacionamiento."""
        try:
            # Actualiza el estado del vehiculo
            self.cursor.execute("""
                UPDATE ESTACIONAMIENTO
                SET fecha_egreso = ?, estado = 'finalizado'
                WHERE patente_vehiculo = ? AND estado = 'activo'; 
            """, (fecha_egreso, patente))
            self.conn.commit()
            print("Retiro registrado correctamente.")
            return True
        except sqlite3.Error as e:
            print(f"Error al registrar retiro: {e}")
            return False
    
    def consultaEstacionamientoActivo(self, patente):
        """Consulta si el vehiculo esta estacionado actualmente."""
        self.cursor.execute("""
            SELECT id_estacionamiento, fecha_ingreso FROM ESTACIONAMIENTO
            WHERE patente_vehiculo = ? AND estado = 'activo';
        """, (patente,))
        return self.cursor.fetchone()