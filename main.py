from flask import Flask, render_template, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'salainen_avain_ristinolla'

def alusta_peli():
    session['lauta'] = [""] * 9
    session['vuoro'] = "X"
    session['voittaja'] = None

def tarkista_voitto(lauta):
    voittoyhdistelmät = [
        [0,1,2], [3,4,5], [6,7,8],
        [0,3,6], [1,4,7], [2,5,8],
        [0,4,8], [2,4,6]
    ]
    for yhd in voittoyhdistelmät:
        a, b, c = yhd
        if lauta[a] and lauta[a] == lauta[b] == lauta[c]:
            return lauta[a]
    if "" not in lauta:
        return "Tasapeli"
    return None

@app.route("/",  methods=["GET", "HEAD"])
def index():
    if 'lauta' not in session:
        alusta_peli()
    if 'x_voitot' not in session:
        session['x_voitot'] = 0
        session['o_voitot'] = 0
    return render_template("peli.html",
                           lauta=session['lauta'],
                           vuoro=session['vuoro'],
                           voittaja=session['voittaja'],
                           x_voitot=session['x_voitot'],
                           o_voitot=session['o_voitot'])

@app.route("/siirto/<int:ruutu>", methods=["POST"])
def siirto(ruutu):
    if session['lauta'][ruutu] == "" and session['voittaja'] is None:
        session['lauta'][ruutu] = session['vuoro']
        voittaja = tarkista_voitto(session['lauta'])
        session['voittaja'] = voittaja
        if voittaja == "X":
            session['x_voitot'] += 1
        elif voittaja == "O":
            session['o_voitot'] += 1
        if not voittaja:
            session['vuoro'] = "O" if session['vuoro'] == "X" else "X"
    return redirect(url_for("index")+"#lauta")

@app.route("/nollaa")
def nollaa():
    alusta_peli()
    return redirect(url_for("index")+"#lauta")

@app.route("/resetoi")
def resetoi_voitot():
    session['x_voitot'] = 0
    session['o_voitot'] = 0
    return redirect(url_for("index")+ "#lauta")

if __name__ == "__main__":
    app.run(debug=True)
