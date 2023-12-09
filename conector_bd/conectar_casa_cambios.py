from flask import Flask, render_template, request, redirect, url_for
from mysql.connector import connect, Error
from dotenv import load_dotenv
import os

class Conector:
    def __init__(self):
        load_dotenv()
        self._host = os.getenv("VHOST")
        self._port = int(os.getenv("VPORT"))
        self._user = os.getenv("VUSER")
        self._pass = os.getenv("VPASSWORD")
        self._db = os.getenv("VDATABASE")

    def crear_conexion(self):
        try:
            return connect(
                host=self._host,
                port=self._port,
                user=self._user,
                password=self._pass,
                database=self._db
            )
        except Error as e:
            print(f"Error al conectar a MySQL: {e}")
            return None

class Transaccion:
    def __init__(self):
        self.conector = Conector()

    def obtener_transacciones(self, tabla):
        conn = self.conector.crear_conexion()
        if conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute(f"SELECT * FROM {tabla}")
                    return cursor.fetchall()
            finally:
                conn.close()

    def insertar_transaccion(self, tabla, direccion_transaccion, tipo_cambio, cantidad_original, cantidad_cambiada, fecha):
        conn = self.conector.crear_conexion()
        if conn:
            try:
                with conn.cursor() as cursor:
                    consulta = f"INSERT INTO {tabla} (Direccion_Transaccion, Tipo_Cambio, Cantidad_Original, Cantidad_Cambiada, Fecha) VALUES (%s, %s, %s, %s, %s)"
                    cursor.execute(consulta, (direccion_transaccion, tipo_cambio, cantidad_original, cantidad_cambiada, fecha))
                    conn.commit()
            finally:
                conn.close()

    def eliminar_transaccion(self, tabla, id_transaccion):
        conn = self.conector.crear_conexion()
        if conn:
            try:
                with conn.cursor() as cursor:
                    consulta = f"DELETE FROM {tabla} WHERE ID_Transaccion = %s"
                    cursor.execute(consulta, (id_transaccion,))
                    conn.commit()
            finally:
                conn.close()

    def obtener_sumas_por_dia(self, tabla):
        conn = self.conector.crear_conexion()
        if conn:
            try:
                with conn.cursor() as cursor:
                    consulta = f"""
                           SELECT Fecha, Direccion_Transaccion, SUM(Cantidad_Cambiada) as Total
                           FROM {tabla}
                           GROUP BY Fecha, Direccion_Transaccion
                           ORDER BY Fecha;
                       """
                    cursor.execute(consulta)
                    return cursor.fetchall()
            finally:
                conn.close()