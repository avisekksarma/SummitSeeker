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
#### Not requiring previous authentication credentials:

###### User Authentication:

1. /api/user/register
2. /api/user/login

#### Requiring authentication credentials:

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
