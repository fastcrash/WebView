import Homematic
from flask import Flask
from flask import render_template


app = Flask(__name__)
conf = Homematic.Config()
conf.loadconfig()
print(conf.categorielist)


@app.route('/<categorie>')
def index(categorie):
    subcategories = conf.subcategorieslist
    categories = conf.categorielist

    baseurl = "http://localhost:5000"
    return render_template('index.html', categorie=categorie, categories=categories, subcategories=subcategories, baseurl=baseurl )





if __name__ == '__main__':
    app.run()
