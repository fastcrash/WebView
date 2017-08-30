from Homematic import Homematic
from Config import Config
from flask import Flask,redirect
from flask import render_template


app = Flask(__name__)




@app.route('/')
def root():
    return redirect("/Home", code=302)

@app.route('/<categorie>')
def index(categorie):
    hm = Homematic(categorie)
    #conf = hm.config

    #categories = conf.categorielist
    #complist = conf.componentslist
    for c in hm.components:
        print(c)
    baseurl = "http://localhost:5000"
    return render_template('index.html',
                           categorie=categorie,
                           categories=hm.categories,
                           subcategories=hm.subcats,
                           baseurl=baseurl,
                           complist=hm.components )


@app.route('/favicon.ico')
def favicon():
    return ""


if __name__ == '__main__':
    app.run()
