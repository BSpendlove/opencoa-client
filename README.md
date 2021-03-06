# opencoa-client
CoA Client API to interact with a CoA Server (eg. an ASR9k or Juniper BNG)

Getting started with docker-compose
```
version: "3.9"
   
services:
  opencoa_api:
    build: .
    ports:
      - 8080:8000
    environment:
      - HOST=0.0.0.0
```

Example POST request
```
curl --location --request POST 'http://10.4.20.100:8080/coa' \
--header 'Content-Type: application/json' \
--data-raw '{
    "ip_address": "10.4.20.98",
    "port": 1700,
    "secret": "mysecret",
    "timeout": 5,
    "attributes": {
        "User-Name": "Ciscodisco"
    }
}'
```

NOTE: This project is not intended to run in a production environment (lacks basic security/authentication functionality) and should be used at your own discretion.

The idea behind this small API is to avoid having to run subprocesses in Python using something like radclient to send CoA messages to a BNG to perform actions such as deactivating a subscriber, changing policy maps, etc... You can extend it to support other vendors however there a few tasks you need to perform:

1) Attributes are loaded into the pyrad dictionary which then helps build the format of the packet (such as vendor specific attributes and length of the attribute), therefore you need to ensure you add a dictionary.<vendor> into the `attributes` folder, and then include it within the root dictionary file... For example:

```
$INCLUDE dictionary.cisco
$INCLUDE dictionary.juniper
$INCLUDE dictionary.microsoft
$INCLUDE dictionary.freeradius
```

A lot of pre-built templates can be found on Freeradius github, you can download them and just drop them into the folder.

2) A very generic CoA packet can be built using the /coa endpoint. The majority of vendor specific endpoints are built using this endpoint and just send more specific attributes related to the task (eg. deactiving or updating a service, or changing a policy map). Visit `http://<your-ip>:<your-port>/docs` to see Swagger documentation which FastAPI generates automatically based on the available routes and data models.

3) Add your FastAPI APIRouter in the `routes/vendors/<vendor>` and register the APIRouter in main.py with `app.include_router(<your-api-router>)`

The `/coa` endpoint will perform some basic checks to ensure the Attributes you send in the body are actually available, this attribute dictionary is pulled every time the endpoint is called so there is no need to restart the API if you add a new dictionary. Common RADIUS return codes will be available upon success/errors if pyrad fails to build the CoA packet or receive a valid response (eg. a CoAACK). The status codes are defined within the `config.py` or snippet from the file can be found below:

```
RETURN_CODES = {
    1: "AccessRequest",
    2: "AccessAccept",
    3: "AccessReject",
    4: "AccountRequest",
    5: "AccountingResponse",
    11: "AccessChallenge",
    12: "StatusServer",
    13: "StatusClient",
    40: "DisconnectRequest",
    41: "DisconnectACK",
    42: "DisconnectNAK",
    43: "COARequest",
    44: "COAACK",
    45: "COANAK",
}
```

POSTMAN API examples can be found in the postman_collection.json file located in the Github repository. The current routes implemented (with a brief description) are below:

`/coa` [POST] - Sends a CoA packet with the specified attributes, vendor is expected to return CoAACK if their AAA framework has processed the packet correctly. 
```
{
    "ip_address": "127.0.0.1",
    "port": 1700,
    "secret": "mysecret",
    "timeout": 5,
    "attributes": {
        "User-Name": "Ciscodisco"
    }
}
```

Sending multiple attributes with the same key can easily be done with creating a list as the value like so:
```
{
    "ip_address": "127.0.0.1",
    "port": 1700,
    "secret": "mysecret",
    "timeout": 5,
    "attributes": {
        "AVPair": ["some-cisco-attribute='yes'", "some-other-avpair-value='probably']
    }
}
```

Vendor specific routes can be found within the Swagger API (or in the opencoa_api/routes/vendors/<vendor>)

`coa_server.py` can be used to test attributes locally (127.0.0.1) or on a remote server, this script will simply print the attribute key/value pairs to the console and return CoAACK. If you want to generate a CoANAK scenario, you can include the attribute "Framed-IP-Netmask" in the attributes when sending a request to the `/coa` endpoint and this will on purpose, return the CoANAK code. This is purely for testing purpose and is simply the example from the pyrad github repository so please don't try to use this as a base template to build a CoA server

Existing attribute dictionaries are by FreeRADIUS @ https://github.com/FreeRADIUS/freeradius-server/tree/master/share/dictionary

Shield: [![CC BY 4.0][cc-by-shield]][cc-by]

This work is licensed under a
[Creative Commons Attribution 4.0 International License][cc-by].

[![CC BY 4.0][cc-by-image]][cc-by]

[cc-by]: http://creativecommons.org/licenses/by/4.0/
[cc-by-image]: https://i.creativecommons.org/l/by/4.0/88x31.png
[cc-by-shield]: https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg