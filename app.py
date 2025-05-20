##
from flask import Flask, render_template, request, redirect

app = Flask(__name__)


##
@app.route("/")
def index():
    return redirect("acceso")
    return render_template("index.html")


##
@app.route("/acceso", methods=["GET", "POST"])
def acceso():
    if request.method == "POST":
        nombre_completo = request.form["nombre-completo"]
        email = request.form["email"]
        contraseña = request.form["contraseña"]

        if "registrarse" in request.form:
            print("Registro")


        elif "iniciar-sesion" in request.form:
            print("Inicio de sesion")

        

    return render_template("login.html")



####
if __name__ == "__main__":
    app.run(debug=True)