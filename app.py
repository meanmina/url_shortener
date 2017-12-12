from dataHandler import DataHandler

import string
from flask import Flask, request, render_template, redirect, Response, json
from flask_cors import CORS
from urlparse import urlparse

host = "http://localhost:5000/"
home_route = 'home.html'

app = Flask(__name__)
CORS(app)

# instantiate dataHandler
dataHandler = DataHandler()

# route to home
@app.route('/', methods=['GET'])
def home():
  return render_template(home_route)

#route to shorten_url
@app.route('/shorten_url', methods=['POST'])
def shorten_url():
  current_url = None

  # get JSON data
  if request.is_json:
    data = request.get_json()

  if "url" in data:
    current_url = data["url"]
  # sad response if JSON data was no good
  if len(current_url) == 0:
    return Response("Empty URL", status=400)

  # if no scheme defined then add one to the URL
  if len(urlparse(current_url).scheme) == 0:
    current_url = "http://" + current_url

  # shorten url
  encoded_url = dataHandler.shortenUrl(current_url)
  if encoded_url is None:
    return Response("Invalid URL", status=400)

  # new URL is local
  url = host + encoded_url
  # send response with status code 200 and url as json
  resp = Response(json.dumps({"shortened_url": url}), status=201, mimetype='application/json')
  return resp

# redirect route to short_url
@app.route('/<short_url>', methods=['GET'])
def redirect_short_url(short_url):
  url = dataHandler.getUrl(short_url)

  if url is None:
    return Response("Invalid short URL", status=400)

  # redirect to URL
  return redirect(url)

if __name__ =='__main__':
  app.run(debug=True)