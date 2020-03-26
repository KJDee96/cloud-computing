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
```bash
python3 -m venv <dir_name>
```

Activate virtual environment
```bash
source <dir_name>/bin/activate
```

Install wheel first or nothing will build
```bash
pip3 install wheel
```

Clone repo and move contents to <dir_name>
Install project requirements inside project folder
```bash
pip3 install -r requirements.txt
```

### DB Setup:
If you edit model.py, run this to generate a new migration
```bash
flask db migrate -m <"migration description">
```

To run DB migrations against a DB - if no DB exists, this will also create one (currently running SQLite3)
```bash
flask db upgrade
```

### uwsgi
Install
```bash
pip3 install uwsgi
```
