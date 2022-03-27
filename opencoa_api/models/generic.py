from ipaddress import IPv4Address
from pydantic import BaseModel, conint
from typing import Dict, Union, List


class COAGeneric(BaseModel):
    """Generic COA message for a v4 or v6 server"""

    ip_address: IPv4Address
    port: conint(ge=1, le=65535) = 1700
    secret: str
    timeout: conint(ge=0, le=300) = 30
    attributes: Dict[str, Union[str, List[str]]]

    class Config:
        schema_extra = {
            "example": {
                "ip_address": "127.0.0.1",
                "port": 1700,
                "secret": "mysecretradiussupersecurepassword",
                "timeout": 5,
                "attributes": {
                    "User-Name": "supercoolusername",
                    "AVPair": [
                        "somecisco:command=probably",
                        "justkidding:command=notreally",
                    ],
                },
            }
        }


class COAGenericSession(BaseModel):
    """Generic COA Session model"""

    ip_address: IPv4Address
    port: conint(ge=1, le=65535) = 1700
    secret: str
    timeout: conint(ge=0, le=300) = 30


class COADisconnectSession(COAGenericSession):
    """Generic COA Disconnect based User-Name attribute"""

    username: str
