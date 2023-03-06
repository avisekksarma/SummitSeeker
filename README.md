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
  Check for 'token_invalid' in response:
    if True redirect to login page
    if False go for next step
  Check for 'success' in response:
    a. if True, read 'data'
    b. if False, read 'validation_error':
          a. if 'validation_error' is True, then read 'errors' to show errors to user
          b. if 'validation_error' is False, then read 'message' to show popup to user

```



#### I.  Not requiring previous authentication credentials:

##### User Authentication:

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

##### Info about the user:

Accepts GET request only

/api/user/profile



##### Info about Trail and Guides:

- /api/trails/ [ Accepts GET ] 
> Gets all the trails
- /api/trails/<int:trail_id> [ Accepts GET ]
> Gets detail trail info of a trail
- /api/trails/<int:trail_id>/guides [ Accepts GET ] 
> Gets all the guides available in a trail

##### Info about Reviews:

- /api/reviews/ [ Accepts GET ] 
> Gets all the reviews of user himself/herself [ valid for both guide and tourist ]
- /api/reviews/trail/<int:trail_id> [ Accepts GET , POST ]
> Gets all reviews in a trail, also make a review in that trail
- /api/reviews/guide/<int:guide_id> [ Accepts GET , POST ]
> Gets all reviews of a guide and also make a review on a guide only by those tourists who have once gone with the guide
- /api/reviews/guide/<int:guide_id>/review/check [ Accepts GET ]
> Checks if the tourist has ever reviewed that specific guide or not

##### Hiring guide:

- /api/trails/<int:trail_id>/guides/<int:guide_id>/hire [ Accepts GET, POST ] 
> GET: gets some useful default data to fill up in form before hiring that specific guide
> POST: for making initial hire request to guide
