# SummitSeeker
Backend code written in DRF for SummitSeeker app which is a comprehensive app for trekkers in Nepal.

Steps:
1. Clone the project
2. cd SummitSeeker
3. python3 -m venv env [ for linux/unix ]
4. source env/bin/activate [ for linux/unix ]
5. pip install -r requirements.txt
6. cd summitseeker
7. touch .env
8. put the secret key provided
9. cd ..
10. python manage.py runserver


## API Documentation:

#### API Response is in following same format:

Response:

```
As always Follow these:
  Check for 'success' in response:
    a. if True, read 'data'
    b. if False, read 'validation_error':
          a. if 'validation_error' is True, then read 'errors' to show errors to user
          b. if 'validation_error' is False, then read 'message' to show popup to user

```



#### I.  Not requiring previous authentication credentials:

###### User Authentication:

1. /api/user/register

Accepts: POST only

---

Request body example:

a. As Tourist:
```
{
    "email": "liya@gmail.com",
    "date_of_birth": "2001-03-22",
    "gender": "F",
    "nationality": "AF",
    "password":"nepalGreat123",
    "contactNum": 2222678662,
    "languages": [
        "CN",
        "JP"
    ],
    "first_name": "liya",
    "last_name": "pina",
    "userType":"TR",
    "experience":"B"
}
```

b. As Guide:
```
{
    "email": "liya@gmail.com",
    "date_of_birth": "2001-03-22",
    "gender": "F",
    "nationality": "AF",
    "password":"nepalGreat123",
    "contactNum": 2222678662,
    "languages": [
        "CN",
        "JP"
    ],
    "first_name": "liya",
    "last_name": "pina",
    "userType":"GD",
    "total_trek_count":12,
    "availability":True
}
```

Optional in TR registration:

```
experience =[
        ('N','Never Done'),
        ('B','Beginner' [Default] ),
        ('S','Seasoned'),
        ('P','Professional')
    ]
```

Optional in GD registration:

```
total_trek_count = [number] [ default = 0 ]
availability = [ boolean (True/False) ] [ default = True ]
```


---



2. /api/user/login

#### II. Requiring authentication credentials:

###### Info about the user:

Accepts GET request only

/api/user/profile



###### Info about Trail and Guides:

3. /api/trails/
4. /api/trails/<int:trail_id>
5. /api/trails/<int:trail_id>/guides

###### Info about Trail reviews:

5. /api/reviews/trail/<int:trail_id>
6. /api/reviews/guide/<int:guide_id>
7. /api/reviews/guide/<int:guide_id>/review/check

###### Hiring guide:

8./api/trails/<int:trail_id>/guides/<int:guide_id>/hire
