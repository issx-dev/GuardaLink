##
from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)

# Diccionario temporal para almacenar usuarios
usuarios = {}

##
@app.route("/")
def index():
    return redirect("acceso")
    return render_template("index.html")


##
@app.route("/acceso", methods=["GET", "POST"])
def acceso():
    if request.method == "POST":
        nombre_completo = request.form.get("nombre-completo")
        email = request.form.get("email")
        contraseña = request.form.get("contraseña")

        if "registrarse" in request.form:
            print(nombre_completo, email, contraseña)
            print("Registro")


        elif "iniciar-sesion" in request.form:
            print(email, contraseña)
            print("Inicio de sesion")

        

    return render_template("login.html")



####
if __name__ == "__main__":
    app.run(debug=True)