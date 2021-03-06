# Phone Billing Service API

A REST API that receives start and end phone call records, and returns detailed bills based on the source phone number and / or period informed.


## Software Requirements

- [python 3.5+](https://www.python.org/)
- [virtualenv](https://virtualenv.pypa.io/en/stable/)
- [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/)
- [Django 1.10+](https://www.djangoproject.com/download/)
- [Django Rest Framework](http://www.django-rest-framework.org/#installation)


### Installing Dependencies

```bash
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

 - `/callrecord/` - receives call records (start and end) from the client. The client must send the pair (start and end) with the same call_id so the call can be included in the bill

JSON expected formats

- Start Record
```
{
    "id":  // Record unique identificator (must be an integer value);
    "type":  // indicate if the data is a start record ("type": 1) or end record ("type": 2);
    "timestamp":  // The timestamp of when the call started (the format must be YYYY-MM-DDThh:mm:ssZ,
                  // where T and Z are fixed letters);
    "call_id":  // Unique for each call record pair (must be an integer value);
    "source":  // The subscriber phone number that originated the call (must be a string with 10 or 11
               // digits, where the first two digits are the area code, and the other ones
               // are the phone number);
    "destination":  // The phone number receiving the call. It must have the same format as the source
                  // phone number, but must have a different number.
}
```

Example:
```
{
    "id": 1,
    "type": 1,
    "timestamp": "2018-10-25 14:30:59Z",
    "call_id": 1,
    "source": "11997870978",
    "destination": "11996295422"
}
```

- End Record
```
{
    "id":  // Record unique identificator (must be an integer value);
    "type":  // indicate if the data is a start record ("type": 1) or end record ("type": 2);
    "timestamp":  // The timestamp of when the call ended (the format is the same as the
                  // start record's timestamp, but must be greater);
    "call_id":  // Unique for each call record pair (must be an integer value).
}
```

Example:
```
{
    "id": 1,
    "type": 2,
    "timestamp": "2018-10-25 14:31:59Z",
    "call_id": 1
}
```

 - `/phonebill/` - responds a detailed phone bill based on the source phone number and / or period given in this URL. The source phone number must always be informed (same format as detailed above), but the period is optional (mm/yyyy format, where mm is the month, and yyyy is the year). If the period is not informed, the application will consider as the last month's period (based on the request's current date). Example: /phonebill?source=11999999999&period=10/2018

JSON returned format:
```
{
    "destination": // the same informed in the start record;
    "start_date": // the date part of the timestamp informed in the start record;
    "start_time": // the time part of the timestamp informed in the start record;
    "duration": // call's duration, that is, the difference between the start record's
                // and end record's timestamp (format is 99h99m99s);
    "price": // the call's price, based on the time of the day and duration
}
```

Example:
```
[
    {
        "destination": "11988884444",
        "start_date": "25/10/2018",
        "start_time": "14:30:59",
        "duration": "0h01m00s",
        "price": "R$ 0,45"
    }
]
```

### Development Environment

- Python 3.5.2
- Django 1.11.7
- Django Rest Framewok 3.7.3
- Sublime Text 3.1.1 with Anaconda (Python package)
- Xubuntu GNU/Linux Operating System
- SQLite DBMS (for production use, MySQL or PostgreSQL is recommended instead)

### Running django unit tests

```bash
# Execute tests
$ python manage.py test
```

- If the tests were executed with no errors, then the command shell should show the following messages (the time period may have a different value on different computers):

```bash
Ran 23 tests in 0.455s

OK
Destroying test database for alias 'default'
```
