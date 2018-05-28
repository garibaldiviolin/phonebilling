# Phone Billing Service API

A REST API that receives start and end phone call records, and returns detailed bill based on the source phone number and / or period informed.


## Software Requirements

- [python 3.5+](https://www.python.org/)
- [virtualenv](https://virtualenv.pypa.io/en/stable/)
- [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/)
- [Django 1.10+](https://www.djangoproject.com/download/)
- [Django Rest Framework](http://www.django-rest-framework.org/#installation)


### Installing Dependencies

```bash
# Create a virtualenv to install the python requirements
$ mkvirtualenv --python="python3.5_dir_path" deep-test
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

 - `/startrecord/` - receives the call start record from the client
 - `/endrecord/` - receives the call end record from the client
 - `/phonebill/` - responds a detailed phone bill based on the source phone number and / or period given
