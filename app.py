#use flask to render a template, redirecting to another URL, and creating a URL.
from flask import Flask, render_template, redirect, url_for
# use PyMongo to interact with our Mongo database
from flask_pymongo import PyMongo
#using the scraping code, we will convert from Jupyter notebook to Python
import scraping

app = Flask(__name__)

#tell Python how to connect to Mongo using PyMongo
#use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

#ABOVE CODE
#app.config["MONGO_URI"] tells Python that our app will connect to Mongo using a URI, a uniform resource identifier similar 
#to a URL

# "mongodb://localhost:27017/mars_app" is the URI we'll be using to connect our app to Mongo. This URI is saying that the app
# can reach Mongo through our localhost server, using port 27017, using a database named "mars_app".

#define the route for the HTML page.
@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)

@app.route("/scrape")
def scrape():
   mars = mongo.db.mars
   mars_data = scraping.scrape_all()
   mars.update({}, mars_data, upsert=True)
   return redirect('/', code=302)

if __name__ == "__main__":
   app.run()
