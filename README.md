# Web Scraping and PyMongo Homework
All web scrape coding was written using mission_to_mars.ipynb. This document was then aggregated into scrape_mars.py into two functions, one to initialize the browser connection and one to perform the scrape and push data into a Mongo database.

* app.py used the Flask application to generate the code from the MongoDB source.
* index.html has the formatting for the page
* Screenshot 1 and 2 contain screenshots of the Flask-generated webpage

Challenges:
* Screenshot 1 shows that the mars facts html code did not format properly when pushed back in by flask.
* Screenshot 1 also shows a button for scraping, but this is nonfunctional, will likely need D3 to make it work.
* Screenshot 2 shows that the images are sequential rather than in a 2 x 2 grid as mandated by the example.