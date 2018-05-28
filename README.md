# Phone Billing Service API

A REST API that receives start and end phone call records, and returns detailed bill based on the source phone number and / or period informed.

## Approach Description

The main goal of this API is to calculate the popularity of Youtube video themes, based on the given formula:

```
Score = views * TimeFactor * PositivityFactor
```
Where:
```
TimeFactor = max(0, 1 - (days_since_upload/365))
PositivityFactor = 0.7 * GoodComments + 0.3 * ThumbsUp
GoodComments = positive_comments/(positive_comments+negative_comments)
ThumbsUp = thumbs_up/(thumbs_up+thumbs_down)
```

## Software Requirements

To start a local version of this API on your machine you have to met the following requirements and follow this instructions (they assume a linux based os):

- [python 3.6+](https://www.python.org/)
- [virtualenv](https://virtualenv.pypa.io/en/stable/)
- [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/)
- [Django 1.11](https://www.djangoproject.com/download/)
- [Django Rest Framework](http://www.django-rest-framework.org/#installation)


### Installing Dependencies

```bash
# Create a virtualenv to install the python requirements
$ mkvirtualenv --python="python3.6_dir_path" deep-test
# Activate it
$ workon deep-test
# Install the requirements
$ pip install -r requirements.txt
```

### Running the Project

```bash
# Execute migrations
$ python manage.py migrate
# Start the server
$ python manage.py runserver

```

### API Documentation

Endpoints:

 - `youtube-stats/get_popular_themes` for gettiting themes based on the given formula
 - `youtube-stats/get_popular_themes` for gettiting themes based on the given formula
 - `youtube-stats/get_popular_themes` for gettiting themes based on the given formula

### Extra Content
 - A [postman](https://www.getpostman.com/) collection with the get for your local env
