# Flask JSON endpoints through YELP API
> Flask Back-End server that calls Yelp API for JSON data, sorts it, and returns it in an easy to read jsonified endpoint. 
Front-End provides forms to utilize endpoints' search/filters, and navigation.

To Do:
- Finish Comments and README
- Change some if statements to try blocks
- I like this project so Imma expand it later.

How-To:
- Download repository
- CD to root folder
- Install requirements
- Create missing files (See Below)
- On Linux terminal type 'flask run'
- Head on over to localhost:5000
- For unit tests type 'python -m pytest tests'

### What's Literally Missing
Config and secrets not added due to them being secret.
They are as follows:

app/main/secrets.py
```python
headers = {'Authorization':'Bearer insert-yelp-api-key'}
```
root/config.py
```python
class Config(object):
    SECRET_KEY = 'insert-secret'
```