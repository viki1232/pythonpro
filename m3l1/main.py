from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return '<h1>Hello, World!</h1>'
@app.route("/correr")
def correr():
    return '<h1>estas corriendo</h1>'
@app.route("/comer")
def comer():
    return '<h1>estas comiendo</h1>'
@app.route("/musica")
def musica():
    return '<h1>estas escuchando musica</h1>'

def rutas():
    rutas_disponibles = []
    for rule in app.url_map.iter_rules():
        rutas_disponibles.append(f"{rule.endpoint}: {rule.rule}")
    return "<br>".join(rutas_disponibles)
app.run(debug=True)