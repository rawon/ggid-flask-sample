#GGID Flask Python Sample Application
## Dependencies 
To install dependencies run:

    pip install -r requirements.txt

## Base URL and Redirect URL
As a default when running this app you can access it from _http://127.0.0.1:5000/_. And a URL of _http://127.0.0.1:5000/consumer/exchange/_ is setup to be the designated view/url to exchange the code given by the server for access token, so you need to set your application redirect URL to this.

## Running the Application
To run this application:

    python app.py
