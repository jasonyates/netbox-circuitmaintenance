import boto3
import email
from email import policy
from circuit_maintenance_parser import init_provider
from circuit_maintenance_parser import NotificationData
import urllib3
import pynetbox
import json
from datetime import datetime

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Variables
S3_BUCKET_NAME = 'your-s3-bucket'
NB_URL = 'https://netbox.yourdomain.com'
NB_API_TOKEN = 'yournetboxtokenhere'
S3_DELETE_UNKNOWN = False
S3_DELETE_PROCESSED = False

# Determine the circuit_maintenance_parser provider from the email address
def _provider(from_email):

    if 'zayo.com' in from_email:
        return 'zayo'
    elif 'colt.net' in from_email:
        return 'colt'
    elif 'verizonbusiness.com' in from_email:
        return 'verizon'
    elif 'cogentco.com' in from_email:
        return 'cogent'
    elif 'aquacomms.com' in from_email:
        return 'aquacomms'
    elif 'arelion.com' in from_email:
        return 'arelion'
    elif 'amazon.com' in from_email:
        return 'aws'
    elif 'cogentco.com' in from_email:
        return 'cogent'
    elif 'bso.co' in from_email:
        return 'bso'
    elif 'equinix.com' in from_email:
        return 'equinix'
    elif 'lumen.com' in from_email:
        return 'lumen'
    elif 'momentumtelecom.com' in from_email:
        return 'momentum'
    elif 'superonline.net' in from_email:
        return 'seaborn'
    elif 'tisparkle.com' in from_email:
        return 'sparkle'
    elif 'telstra.com' in from_email:
        return 'telstra'
    else:
        return None

# Parse the inbound email
def _parse_email(mail):

    # Determine the provider
    provider = _provider(mail['from'])

    if provider != None:

        print("Using provider " + provider)
        
        # Load the provider and the email to circuit parser
        generic_provider = init_provider(provider)
        data_to_process = NotificationData.init_from_emailmessage(mail)
    
        # Parse the maintenances from the email body
        maintenances = generic_provider.get_maintenances(data_to_process)

        # Check if there was anything extracted
        if len(maintenances) > 0:
        
            # Return the maintenance event
            return maintenances[0].to_json()

        else:
            print("Unable to extract any maintenances from the email")
            return None

    else:
        print("Email does not match a provider. Email from " + mail['from'])
        return None

def _netbox_circuitmaintenance(maintenance, mail):

    maintenance = json.loads(maintenance)

    # Connect to Netbox
    nb = pynetbox.api(
        NB_URL,
        token=NB_API_TOKEN
    )
    nb.http_session.verify = False

    # Check if the maintenance event exists in Netbox
    nb_maintenance = nb.plugins.maintenance.circuitmaintenance.get(name=maintenance['maintenance_id'])

    if nb_maintenance == None:

        # Maintenance event is new
        # Get the Netbox provider
        nb_provider = nb.circuits.providers.get(name__ic=maintenance['provider'])
        
        # Check we matched a provider
        if nb_provider != None:

            # Maintenance event is new
            print("Maintenance event is new " + maintenance['maintenance_id'])

            # Add the maintenance event to netbox
            nb_maintenance = nb.plugins.maintenance.circuitmaintenance.create(
                name=maintenance['maintenance_id'], 
                summary=maintenance['summary'],
                status=maintenance['status'],
                provider=nb_provider.id,
                start=datetime.utcfromtimestamp(int(maintenance['start'])).strftime('%Y-%m-%d %H:%M:%S'),
                end=datetime.utcfromtimestamp(int(maintenance['end'])).strftime('%Y-%m-%d %H:%M:%S')
            )

        else:
            # Unable to match the parsed provider with one in Netbox. Cannot continue.
            print("Unable to match provider with one in Netbox. Parsed provider is: " + maintenance['provider'])
            return None

    else:

        print("Maintenance event is existing. Updating details " + maintenance['maintenance_id'])

        # Update existing maintenance event
        nb_maintenance.status = maintenance['status']
        nb_maintenance.start = datetime.utcfromtimestamp(int(maintenance['start'])).strftime('%Y-%m-%d %H:%M:%S')
        nb_maintenance.end = datetime.utcfromtimestamp(int(maintenance['end'])).strftime('%Y-%m-%d %H:%M:%S')
        nb_maintenance.save()

    # Validate parsed impact matches maintenance impact
    for circuit in maintenance['circuits']:

        # Check if the impacted circuit exists in Netbox
        nb_circuit = nb.circuits.circuits.get(cid__ic=circuit['circuit_id'])

        if nb_circuit != None:

            # Circuit ID is in Netbox. Check if it's associated to this event already
            print("Circuit ID " +circuit['circuit_id'] + " exists in Netbox.")
            nb_impact = nb.plugins.maintenance.circuitmaintenanceimpact.get(circuitmaintenance=nb_maintenance.id, circuit=nb_circuit.id)

            if nb_impact != None:

                # Circit impact is tagged to this maintenance event. Validate the impact is correct based on this notification
                if nb_impact.impact == circuit['impact']:
                    print("Circuit is tagged on this maintenance event already. Impact is " + circuit['impact'])
                else:
                    # Carrier impact in this notification doen't match previously saved impact. Use this notification as source of truth
                    print("Circuit is tagged on this maintenance event already. Impact does not match the carrier notification. Updating impact to " + circuit['impact'])
                    nb_impact.impact = circuit['impact']
                    nb_impact.save()
            else:

                # Circuit impact is not tagged to this notification. Add it
                print("Tagging circuit " + circuit['circuit_id'] + " with impact " + circuit['impact'])
                nb.plugins.maintenance.circuitmaintenanceimpact.create(
                    circuitmaintenance=nb_maintenance.id, 
                    circuit=nb_circuit.id,
                    impact=circuit['impact']
                )

        else:
            print("Circuit ID " +circuit['circuit_id'] + " does not exist in Netbox. Unable to associate with maintenance event.")


    # Store this maintenance notification
    print("Storing maintenance notification")
    nb.plugins.maintenance.circuitmaintenancenotifications.create(
        circuitmaintenance=nb_maintenance.id, 
        email_body=str(mail.get_body()), 
        subject=mail['subject'], 
        email_from=email.utils.parseaddr(mail['from'])[1], 
        email_recieved=datetime.utcfromtimestamp(int(maintenance['stamp'])).strftime('%Y-%m-%d %H:%M:%S')
    )

# Main lambda function
def lambda_handler(event, context):

    print("Processing inbound email " + event['Records'][0]['ses']['mail']['messageId'])

    s3_client = boto3.client("s3")

    try:
        # Load the email from S3 bucket based on the recieved event
        file_content = s3_client.get_object(
            Bucket=S3_BUCKET_NAME, Key=event['Records'][0]['ses']['mail']['messageId'])["Body"].read()
    except:
        print("Unable to load email from S3.")
        return None
    
    try:
        # Parse it to extract the parts
        mail = email.message_from_string(file_content.decode('utf-8'), policy=policy.default)
    except:
        print("Unable to parse email from S3 object.")
        return None

    # Parse the email
    maintenance = _parse_email(mail)

    if maintenance:

        # Load the maintenance event in Netbox
        _netbox_circuitmaintenance(maintenance,mail)

        print("Maintenance parsing complete")

    else:

        print("Maintenance parsing failed with errors.")