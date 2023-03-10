# SummitSeeker
Backend code written in DRF for SummitSeeker app which is a comprehensive app for trekkers in Nepal.

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
    "email": "chris@gmail.com",
    "date_of_birth": "2000-04-22",
    "gender": "M",
    "nationality": "KR",
    "password":"nepalGreat123",
    "contactNum": 128745673,
    "languages": [
        "EN",
        "JP"
    ],
    "first_name": "Chris",
    "last_name": "Lundstram",
    "userType":"GD",
    "total_trek_count":3,
    "availability":true
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
availability = [ boolean (true/false) ] [ default = true ]
```


---



2. /api/user/login

3. /api/languages [ Accepts GET ]
> Gets all the available languages 


#### II. Requiring authentication credentials:

##### Info about the user:

Accepts GET request only

/api/user/profile



##### Info about Trail and Guides:

- /api/trails/ [ Accepts GET ] 
> Gets all the trails
- /api/trails/<int:trail_id> [ Accepts GET ]
> Gets detail trail info of a trail
- /api/trails/<int:trail_id>/guides [ Accepts POST ] 
> Gets all the guides available in a trail
```

{
    "start_date":"2023-04-10"
}

```

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


##### Geting notification:

- /api/user/notifications/  [ Accepts GET only ]

> For Tourist: 'All' has every notification except 'accepted', and 'Accepted' has only accepted notifications

> For Guide: 'All' has every notification except 'requested', and 'requested' has only requested notifications

##### Accept or reject by guide:

- /api/response/<int:hire_id>/ [ Accept POST only ]

In request.body:

```
    status = 'AC' or 'RJ' [ for accept / reject a request of tourist]
```

##### Cancel request by tourist:

- /api/user/cancelrequest/<int:hire_id> [ Accepts GET only ]