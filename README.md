# cloud-computing
Cloud Computing Coursework - A simple web application integrated into AWS cloud services

Project by Kieran Dee, Oliver Favell and Timothy Lockwood

Required Programs:
- python3 (Ver 3.7+)
- pip3
- virtualenv
- virtualenvwrapper

## Virtualbox setup to test
1. VM settings -> network -> Adapter 2 -> set to bridged
2. Run "ip addr" to find both adapter names -> edit /etc/netplan/<file name here (tab complete it, it exists by default)> as follows (make sure to use spaces, do not use tabs)
    ```bash
    network:
        ethernets:
            <device 1>:
                dhcp4: true
            <device 2>:
                dhcp4: true
        version 2
    ```
3. run netplan apply + reboot

## EASY Installation (tested on ubuntu server 18.04)

```bash
sudo mkdir /var/www
cd /var/www
git clone <this repo>
cd <dir>
sudo -i
chmod 645 install.sh
./install.sh
exit
```

Then edit /etc/nginx/sites-available/cloud-computing with the local IP address for the adapter

## HARD Installation
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

Install wheel first or nothing will build (deactivate venv)
```bash
pip3 install wheel
```

Install project requirements inside project folder (activate venv)
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
Install uswgi (activate venv)
```bash
pip3 install uwsgi
```
