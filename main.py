from flask import Flask, render_template, request, redirect, url_for
from conector_bd.conectar_casa_cambios import Conector, Transaccion
from datetime import date

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/dolares', methods=['GET', 'POST'])
def dolares():
    transaccion = Transaccion()
    if request.method == 'POST':
        if 'direccion_transaccion' in request.form:  # Lógica para agregar una transacción en dólares
            direccion_transaccion = request.form['direccion_transaccion']
            tipo_cambio = float(request.form['tipo_cambio'])
            cantidad_original = float(request.form['cantidad_original'])
            cantidad_cambiada = float(request.form['cantidad_cambiada'])
            fecha = date.today()
            transaccion.insertar_transaccion('Transacciones_Dolares', direccion_transaccion, tipo_cambio, cantidad_original, cantidad_cambiada, fecha)

    transacciones_dolares = transaccion.obtener_transacciones('Transacciones_Dolares')
    sumas_por_dia = transaccion.obtener_sumas_por_dia('Transacciones_Dolares')
    return render_template('dolares.html', transacciones=transacciones_dolares, sumas_por_dia=sumas_por_dia)

@app.route('/eliminar_dolares', methods=['POST'])
def eliminar_dolares():
    id_transaccion = request.form['id_transaccion']
    transaccion = Transaccion()
    transaccion.eliminar_transaccion('Transacciones_Dolares', id_transaccion)
    return redirect(url_for('dolares'))
@app.route('/euros', methods=['GET', 'POST'])
def euros():
    transaccion = Transaccion()
    if request.method == 'POST':
        if 'direccion_transaccion' in request.form:  # Lógica para agregar una transacción en euros
            direccion_transaccion = request.form['direccion_transaccion']
            tipo_cambio = float(request.form['tipo_cambio'])
            cantidad_original = float(request.form['cantidad_original'])
            cantidad_cambiada = float(request.form['cantidad_cambiada'])
            fecha = date.today()
            transaccion.insertar_transaccion('Transacciones_Euros', direccion_transaccion, tipo_cambio, cantidad_original, cantidad_cambiada, fecha)

    transacciones_euros = transaccion.obtener_transacciones('Transacciones_Euros')
    sumas_por_dia = transaccion.obtener_sumas_por_dia('Transacciones_Euros')
    return render_template('euros.html', transacciones=transacciones_euros, sumas_por_dia=sumas_por_dia)


@app.route('/eliminar_euros', methods=['POST'])
def eliminar_euros():
    id_transaccion = request.form['id_transaccion']
    transaccion = Transaccion()
    transaccion.eliminar_transaccion('Transacciones_Euros', id_transaccion)
    return redirect(url_for('euros'))

if __name__ == '__main__':
    app.run(debug=True)