# cloud-computing
Cloud Computing Coursework - A simple web application integrated into AWS cloud services

Project by Kieran Dee, Oliver Favell and Timothy Lockwood

Required Programs:
- python3 (Ver 3.7+)
- pip3
- virtualenv
- virtualenvwrapper

## Installation:
### Pip3
```
sudo apt-get install python3-pip
```
### VirtualEnv & VirtualEnv Wrapper:
```
sudo apt-get install virutalenv virtualenvwrapper
```

### Flask Env Setup:
Create virtual environment folder
```
python3 -m venv <dir_name>
```

Activate virtual environment
```
source <dir_name>/bin/activate
```

Clone repo and move contents to <dir_name>
Install project requirements inside project folder
```
pip3 install -r requirements.txt
```

### DB Setup:
If you edit model.py, run this to generate a new migration
```
flask db migrate -m <"migration description">
```
To run DB migrations against a DB - if no DB exists, this will also create one (currently running SQLite3)
```
flask db upgrade
```