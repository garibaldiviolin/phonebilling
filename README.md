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

 - `/callrecord/` - receives the call record (start and end) from the client. The client must send the pair (start and end) so the other endpoint (phonebill) can include the call in the bill

JSON expected formats

- Start Record
```
{
  "id":  // Record unique identificator (must be an integer value);
  "type":  // indicate if the data is a start record ("type": 1) or end record ("type": 2);
  "timestamp":  // The timestamp of when the call started (the format must be yyyy/mm/ddThh:mm:ssZ');
  "call_id":  // Unique for each call record pair (must be an integer value);
  "source":  // The subscriber phone number that originated the call (the number must have 10 or 11
             // digits, the first two digits are the );
  "destination":  // The phone number receiving the call. It must have the same format as the source
                  // phone number, but must have a different number
}
```

- End Record
```
{
   "id":  // Record unique identificator (must be an integer value);
   "type":  // indicate if the data is a start record ("type": 1) or end record ("type": 2);
   "timestamp":  // The timestamp of when the call started (the format must be yyyy/mm/ddThh:mm:ssZ');
   "call_id":  // Unique for each call record pair (must be an integer value).
}
```

 - `/phonebill/` - responds a detailed phone bill based on the source phone number and / or period given in this URL. The source phone number must always be informed (same format as detailed above), but the period is optional (mm/yyyy format, where mm is the month, and yyyy is the year). If the period is not informed, the application will consider that it's the last month's period (based on the request's current date). Example: /phonebill?source=11999999999&period=10/2018

### Development Environment

- Python 3.5.2
- Django 1.11.7
- Django Rest Framewok 3.7.3
- Sublime Text 3.1.1 with Anaconda (Python package)
- Xubuntu GNU/Linux Operating System
- SQLite DBMS
