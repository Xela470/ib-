from ibflex import client
import xml.etree.ElementTree as ET
import requests
from notion_client import Client
import os
import json
from collections import OrderedDict


token = '125734676551632065614931'
query_id = '1141754'

webhook_url = 'https://xela47.app.n8n.cloud/webhook-test/4367e10f-7314-47da-85e3-c16a9b9fcdc1'

try:
    response = client.download(token, query_id)
    root = ET.fromstring(response)

    change_in_nav = root.find('.//ChangeInNAV')
    if change_in_nav is not None:
        twr = change_in_nav.get('twr')
        ending_value = change_in_nav.get('endingValue')
    else:
        twr = None
        ending_value = None

    data_dict = {
        "TWR": twr,
        "EndingValue": ending_value
    }

    print("Données extraites:", data_dict)
    print("URL du webhook:", webhook_url)

    pabbly_response = requests.post(webhook_url, json=data_dict)
    print("Statut de la réponse Pabbly:", pabbly_response.status_code)
    print("Contenu de la réponse Pabbly:", pabbly_response.text)

except Exception as e:
    print("Une erreur s'est produite:", str(e))