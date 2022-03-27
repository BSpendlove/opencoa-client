from fastapi import APIRouter
from pyrad.client import Client, Timeout
from opencoa_api.models.generic import COAGeneric
from opencoa_api.config import Config

router = APIRouter(
    prefix="/coa",
    tags=["coa"],
    responses={404: {"Error": True, "description": "Not Found"}},
)

config = Config(RADIUS_DICTIONARY_PATH="./attributes")


@router.post("/")
def coa_request(coa: COAGeneric):
    config.load_dictionary()
    unsupported_attributes = config.validate_attributes(coa.attributes)

    if unsupported_attributes:
        formatted_string = f", ".join(unsupported_attributes)
        return {
            "error": True,
            "message": f"The following attributes sent by the client are not supported: {formatted_string}",
        }

    client = Client(
        server=str(coa.ip_address),
        coaport=coa.port,
        secret=coa.secret.encode(),
        timeout=coa.timeout,
        dict=config.RADIUS_DICTIONARY,
    )

    try:
        request = client.CreateCoAPacket(**config.normalize_attributes(coa.attributes))
    except Exception as error:
        return {
            "error": True,
            "message": "Exception caught when trying to create COA packet",
            "exception": str(error),
        }

    try:
        result = client.SendPacket(request)
    except Timeout:
        return {"error": True, "message": "COA Request timeout."}

    if result.code == 45:  # CoANAK
        return {"error": True, "message": "Server returned COANAK", "code": result.code}

    return_code_description = config.get_return_code_description(result.code)
    return {"error": False, "message": return_code_description, "code": result.code}
