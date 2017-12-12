# Build a url shortener

Your primary task is to build a url shortener api using python.

## Requirements

- Your webservice should have a `POST /shorten_url` endpoint that receives a json body with the url to shorten. A successful request will return a json body with the shortened url. If a get request is made to the shortened url then the user should be redirected to the the original url, or returned the contents of the original url.
- Perform appropriate validatation on the url to be shortened, and return appropriate error responses if the url is not valid
- Contain a `README.md` file with instructions on how to run your service.

## Note:
This task is simple and straight forward but we will be assessing you on your implementation of web service / python / software engineering best practices. So please use this as an oppertunity to demonstrate how your write code and solve problems. You should also build your webservice in a way that a devops enginer (or you) could configure your backend in a way that your webservice could handle high traffic (eg. 1000 rps). Please explain in your `README.md` file how to configure your backend for scale.

## Example usage:

1)

`www.helloworld.com` -> <html><body> hello world </body> </html>

2)
```
Request:
    POST www.your_service.com/shorten_url

    body:
    {
        "url": "www.helloworld.com"
    }

Response: 
    Status code: 201
    response_body:
    {
        "shortened_url": 'http://www.your_service.com/ouoYFY48'
    }
```
3)

`http://www.your_service.com/ouoYFY48` -> <html><body> hello world </body> </html>

## Mihaela Comments:
Install sqlite3 from here `https://www.sqlite.org/download.html` (this link might help `http://www.sqlitetutorial.net/download-install-sqlite/`). This will be the database we use for the webservice to store our URLs. There are plenty other database options but I chose to go with this one since it uses SQL syntax and the queries we need here are simple.

`cd` to `\url_shortener_test` folder and check that you have a `urls.db` file. If not, call `sqlite3 urls.db` to create the database for URLs.

`pip install flask` - we will be using flask to run our service. Django was my second option but many seem to favour Flask in term of easy and fast setup.
`pip install -U flask-cors` - will enable CORS for our requests

To run server do: `python app.py` and go to `http://127.0.0.1:5000` in a browser.

## Scaling:
Out of the box, a simple Flask webservice can only handle one request at a time. How we choose to host the application and run it will define the scalability of the service and how many requests we can serve at one time. The beauty of Flask as a framework is that it's very simple and does not add any bloat to your application, so when it comes to scaling it's all based on how and where you deploy.

When talking about how many rps an app can handle we are looking at the scalability of the app. To solve this sort of issue we have 2 options:

1) asynchronous calls - this can be solved by using Gunicorn.
This is a very simple wrapper which you can use to define how many asynchronous workers you want for your app. The result is a number of processes managed by Gunicorn which behave like the development server. These processes use coroutines so each worker can still only handle one thing at a time but with the possibility of "pausing" while waiting on database queries, thus being able to handle multiple requests at once. This would be the simplest way to scale-up our application.

2) load balancer & containers - this is a more appropriate way of scaling a production application.
Deciding where you will host your application is part of solving the scalability issue. There are plenty hosting options (see Heroku, AWS etc.) and they all have different approaches to scaling up (be it manual or automated). We can even host on multiple local servers if we have the available hardware but this is generally expensive and the best approach is to look at cloud.
In general terms, the approach here is to containerise your application and deploy it on multiple nodes. A load balancer will be used to asses the load of every node your service is running on and send the request to the least loaded one. The decision algorithm there is more complicated but the idea is that the load balancer will make the decision and send the request to the best node.
There are a few things to consider when using this approach:
a) storage - you will need a common database that these webservices will use. We will need a shared database reachable via all the nodes we deploy on and a smart way to handle database transactions to make sure we don't corrupt our data. For now we can use the local databases and setup data replication to all local databases which will have to be instant so we can retrieve a stored URL on all of our nodes. Or setup the load balancer to send "retrieve" request onto the same node where the "store" request happened so we ensure the URL is in the local database of the node.
b) monitoring - we need a way to monitor load per node and per the entire service to identify the need for scaling-up/down.
c) scaling - intially we can rely on manually scaling-up when we reach high traffic but we have to start thinking about spinning new nodes up automatically when traffic increases.

The first approach would be a good initial step in scaling up for 1000rps, depending on the capacity of the server we are deployed on. But if we intend to serve this application to the wider public, we might want to consider scalability for the future and start looking into the cloud.