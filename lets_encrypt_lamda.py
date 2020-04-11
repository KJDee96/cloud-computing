import boto3
import certbot.main
import datetime
import os
import time
import re

# Method to read contents of pem files
def read_and_delete_file(path):
    with open(path, 'r') as file:
        contents = file.read()
    os.remove(path)
    return contents


def provision_cert(email, domain):
    certbot.main.main([
        'certonly',  # Obtain a cert but don't install it
        '--standalone',  # Use standalone challenge
        '--dry-run',  # test challenge
        '-n',  # Run in non-interactive mode
        '--agree-tos',  # Agree to the terms of service,
        '-m', email,  # Email
        '-d', domain,  # Domains to provision certs for
        # Override directory paths so script doesn't have to be run as root
        '--config-dir', '/tmp/config-dir/',
        '--work-dir', '/tmp/work-dir/',
        '--logs-dir', '/tmp/logs-dir/'
    ])

    path = '/tmp/config-dir/live/' + domain + '/'
    return {
        'name': domain,
        'certificate': read_and_delete_file(path + 'cert.pem'),
        'private_key': read_and_delete_file(path + 'privkey.pem'),
        'certificate_chain': read_and_delete_file(path + 'chain.pem')
    }


# Check if domain cert exists and is expiring soon - default = less than 30 days
def should_provision(domain, days=30):
    existing_cert = find_existing_cert(domain)
    if existing_cert:
        now = datetime.datetime.now(datetime.timezone.utc)
        not_after = existing_cert['Expiration']
        return (not_after - now).days <= days
    else:
        return True


# method to find cert on aws account
def find_existing_cert(domain):
    found = None
    certificates = list_certs()
    for cert in certificates:
        if domain == cert["ServerCertificateName"]:
            found = cert
    return found


def list_certs():
    client = boto3.client('iam')
    response = client.list_server_certificates()
    return response['ServerCertificateMetadataList']


def upload_cert_to_iam(cert):
    client = boto3.client('iam')
    iam_response = client.upload_server_certificate(
        ServerCertificatiam_responseeName=cert['name'],
        CertificateBody=cert['certificate'],
        PrivateKey=cert['private_key'],
        CertificateChain=cert['certificate_chain']
    )
    return iam_response


# method add cert to elb
def add_cert_to_elb(listener_arn, cert_arn):
    region_name = listener_arn.split(':')[3]
    client = boto3.client('elbv2', region_name=region_name)
    response = client.add_listener_certificates(
        ListenerArn=listener_arn,
        Certificates=[
            {
                'CertificateArn': cert_arn,
            }
        ]
    )
    return response


# method to remove cert from LB and delete from iam
def delete_cert(listener_arn, domain):
    iam_client = boto3.client('iam')
    region_name = listener_arn.split(':')[3]
    elb_client = boto3.client('elbv2', region_name=region_name)
    cert = find_existing_cert(domain)
    elb_client.remove_listener_certificates(
        ListenerArn=listener_arn,
        Certificates=[
            {
                'CertificateArn': cert['Arn'],
            }
        ]
    )
    try:
        iam_client.delete_server_certificate(
            ServerCertificateName=cert['ServerCertificateName']
        )
    except Exception as err:
        print(err)
        pass


def lambda_handler():
    elb_listener_arn = os.environ.get('elb_listener_arn')
    letsencrypt_email = os.environ.get('letsencrypt_email')
    domain = os.environ.get('letsencrypt_domain')
    days = int(os.environ.get('letsencrypt_period'))
    if should_provision(domain, days):
        cert = provision_cert(letsencrypt_email, domain)
        delete_cert(elb_listener_arn, domain)
        iam_response = upload_cert_to_iam(cert)
        cert_arn = iam_response['ServerCertificateMetadata']['Arn']
        time.sleep(15)
        add_cert_to_elb(elb_listener_arn, cert_arn)
