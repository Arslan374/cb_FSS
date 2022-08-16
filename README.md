# cb_FSS
## Cloud Based File Sharing System

Developed as a university final year project, CloudBased File Sharing System was built to allow the
users to upload their files, access them anywhere
and share them with each other without any size
and type restrictions

## How to Run 
- Install dependencies `pip3 install -r requirments.txt`
- Make migrations `python3 manage.py makemigrations`
- Migrate `python3 manage.py migrate`
- Create Super User (Admin) `python3 manage.py createsuperuser`
- Run Server `python3 manage.py runserver 0.0.0.0:8000`
