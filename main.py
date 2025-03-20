from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'salainen_avain_123'  # Turvallisuuden vuoksi

@app.route("/", methods=["GET", "POST"])
def root():
    if request.method == "POST":
        nimi = request.form.get("nimi")
        tervehdys = request.form.get("tervehdys", "Hei")
        
        # Tarkistetaan, että nimi ei ole tyhjä
        if not nimi.strip():
            session["virhe"] = "Nimi ei voi olla tyhjä!"
            return redirect(url_for("root"))
        
        session["virhe"] = None  # Poistetaan vanha virheviesti
        return redirect(url_for("vastaus", nimi=nimi, tervehdys=tervehdys))
    
    virheviesti = session.get("virhe")
    return render_template("lomake.html", virhe=virheviesti)

@app.route("/vastaus")
def vastaus():
    nimi = request.args.get("nimi", "Tuntematon")
    tervehdys = request.args.get("tervehdys", "Hei")
    return render_template("vastaus.html", nimi=nimi, tervehdys=tervehdys)

if __name__ == "__main__":
    app.run(debug=True)
