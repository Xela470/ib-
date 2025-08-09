from ibflex import client
import xml.etree.ElementTree as ET
import requests
from notion_client import Client
import os
import json
from collections import OrderedDict


token = '125734676551632065614931'
query_id = '1141754'


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

except Exception as e:
    print("Une erreur s'est produite:", str(e))