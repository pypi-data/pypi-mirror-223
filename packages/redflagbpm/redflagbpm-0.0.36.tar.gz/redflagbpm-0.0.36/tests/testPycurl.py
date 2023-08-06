

# curl -X GET "https://ws.sycinversiones.com/mavCheques?estado=Pendientes" -H  "accept: application/json" -H  "Authorization: Bearer [token]"

import pycurl
from io import BytesIO
import json

url = "https://ws.sycinversiones.com/mavCheques?estado=Autorizados"

buffer = BytesIO()
headers = [
    "accept: application/json",
    "Authorization: Bearer [token]"
]

curl = pycurl.Curl()
curl.setopt(curl.WRITEDATA, buffer)
curl.setopt(curl.URL, url)
curl.setopt(curl.HTTPHEADER, headers)
curl.perform()
respondeCode=curl.getinfo(curl.RESPONSE_CODE)
curl.close()

print(respondeCode)
if respondeCode==200:
    response = buffer.getvalue().decode("utf-8")
    parsed=json.loads(response)
    for cheque in parsed:
        print(f'Cheque: {cheque["id"]}  Comitente: {cheque["comitente"]}')
else:
    print("Error de autorización")

