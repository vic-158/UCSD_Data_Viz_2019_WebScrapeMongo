from flask import Flask, render_template
import pymongo

app = Flask(__name__)

# setup mongo connection
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

# connect to mongo db and collection
db = client.mars_db
collection = db.marsinfo


@app.route("/")
def index():
    #Set Mars News Info
    news_title = collection.find_one()['news_title']
    news_p = collection.find_one()['news_p']
    featured_image = collection.find_one()['featured_image']
    mars_weather = collection.find_one()['mars_weather']
    mars_facts = collection.find_one()['mars_facts']
    hemispheres = collection.find_one()['hemispheres']

    # render an index.html template and pass it the data you retrieved from the database
    return render_template("index.html", news_title = news_title, news_p = news_p, featured_image = featured_image, 
    mars_weather = mars_weather, mars_facts = mars_facts, hemispheres = hemispheres)


if __name__ == "__main__":
    app.run(debug=True)
