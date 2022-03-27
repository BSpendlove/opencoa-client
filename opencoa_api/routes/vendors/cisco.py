from fastapi import APIRouter
from opencoa_api.models.generic import COAGeneric
from opencoa_api.models.vendors.cisco import (
    CiscoCOAGenericSession,
    CiscoCOAService,
    CiscoCOAPolicyChange,
    CiscoCOAACLChange,
)
from opencoa_api.routes.coa import coa_request

router = APIRouter(
    prefix="/coa/cisco",
    tags=["coa_cisco"],
    responses={404: {"Error": True, "description": "Not Found"}},
)

# Generic AV-Pair endpoint can be created and called for majority of these routes, I'll get round to it one day...


@router.patch("/account_logon")
def account_logon(coa_session: CiscoCOAGenericSession):
    """Logs on a session via COA based on ASR9000/IOS-XR

    https://community.cisco.com/t5/service-providers-documents/asr9000-xr-bng-vsa-s-vendor-specific-attributes-and-services/ta-p/3141601/show-comments/true"""
    coa_generic = COAGeneric(
        **{
            "ip_address": coa_session.ip_address,
            "port": coa_session.port,
            "secret": coa_session.secret,
            "timeout": coa_session.timeout,
            "attributes": {
                "User-Name": coa_session.username,
                "AVPair": "subscriber:command=account-logon",
            },
        }
    )
    request = coa_request(coa_generic)
    return request


@router.patch("/account_logoff")
def account_logoff(coa_session: CiscoCOAGenericSession):
    """Disconnects a session via COA based on ASR9000/IOS-XR

    https://community.cisco.com/t5/service-providers-documents/asr9000-xr-bng-vsa-s-vendor-specific-attributes-and-services/ta-p/3141601/show-comments/true"""
    coa_generic = COAGeneric(
        **{
            "ip_address": coa_session.ip_address,
            "port": coa_session.port,
            "secret": coa_session.secret,
            "timeout": coa_session.timeout,
            "attributes": {
                "User-Name": coa_session.username,
                "AVPair": "subscriber:command=account-logoff",
            },
        }
    )
    request = coa_request(coa_generic)
    return request


@router.patch("/account_update")
def account_update(coa_session: CiscoCOAGenericSession):
    """Update a session via COA based on ASR9000/IOS-XR

    https://community.cisco.com/t5/service-providers-documents/asr9000-xr-bng-vsa-s-vendor-specific-attributes-and-services/ta-p/3141601/show-comments/true"""
    coa_generic = COAGeneric(
        **{
            "ip_address": coa_session.ip_address,
            "port": coa_session.port,
            "secret": coa_session.secret,
            "timeout": coa_session.timeout,
            "attributes": {
                "User-Name": coa_session.username,
                "AVPair": "subscriber:command=account-update",
            },
        }
    )
    request = coa_request(coa_generic)
    return request


@router.patch("/service_activate")
def account_update(coa_session: CiscoCOAService):
    """Activates a service via COA based on ASR9000/IOS-XR

    https://community.cisco.com/t5/service-providers-documents/asr9000-xr-bng-vsa-s-vendor-specific-attributes-and-services/ta-p/3141601/show-comments/true"""
    coa_generic = COAGeneric(
        **{
            "ip_address": coa_session.ip_address,
            "port": coa_session.port,
            "secret": coa_session.secret,
            "timeout": coa_session.timeout,
            "attributes": {
                "User-Name": coa_session.username,
                "AVPair": f"subscriber:sa={coa_session.service_name}",
            },
        }
    )
    request = coa_request(coa_generic)
    return request


@router.patch("/service_deactivate")
def account_update(coa_session: CiscoCOAService):
    """Deactivates a service via COA based on ASR9000/IOS-XR

    https://community.cisco.com/t5/service-providers-documents/asr9000-xr-bng-vsa-s-vendor-specific-attributes-and-services/ta-p/3141601/show-comments/true"""
    coa_generic = COAGeneric(
        **{
            "ip_address": coa_session.ip_address,
            "port": coa_session.port,
            "secret": coa_session.secret,
            "timeout": coa_session.timeout,
            "attributes": {
                "User-Name": coa_session.username,
                "AVPair": f"subscriber:sd={coa_session.service_name}",
            },
        }
    )
    request = coa_request(coa_generic)
    return request


@router.patch("/hqos_policy")
def change_hqos_policy(coa_session: CiscoCOAPolicyChange):
    """Changes the policy map (HQoS with SPI) based on subscriber:sub-qos-policy-(in|out)"""
    coa_generic = COAGeneric(
        **{
            "ip_address": coa_session.ip_address,
            "port": coa_session.port,
            "secret": coa_session.secret,
            "timeout": coa_session.timeout,
            "attributes": {
                "User-Name": coa_session.username,
                "AVPair": [
                    f"subscriber:sub-qos-policy-in={coa_session.policy_in}",
                    f"subscriber:sub-qos-policy-out={coa_session.policy_out}",
                ],
            },
        }
    )
    request = coa_request(coa_generic)
    return request


@router.patch("/acl_v4")
def change_acl_v4(coa_session: CiscoCOAACLChange):
    """Changes the v4 ACL"""
    coa_generic = COAGeneric(
        **{
            "ip_address": coa_session.ip_address,
            "port": coa_session.port,
            "secret": coa_session.secret,
            "timeout": coa_session.timeout,
            "attributes": {
                "User-Name": coa_session.username,
                "AVPair": [
                    f"ipv4:inacl={coa_session.acl_in}",
                    f"ipv4:outacl={coa_session.acl_out}",
                ],
            },
        }
    )
    request = coa_request(coa_generic)
    return request


@router.patch("/acl_v6")
def change_acl_v6(coa_session: CiscoCOAACLChange):
    """Changes the v4 ACL"""
    coa_generic = COAGeneric(
        **{
            "ip_address": coa_session.ip_address,
            "port": coa_session.port,
            "secret": coa_session.secret,
            "timeout": coa_session.timeout,
            "attributes": {
                "User-Name": coa_session.username,
                "AVPair": [
                    f"ipv6:ipv6_inacl={coa_session.acl_in}",
                    f"ipv6:ipv6_outacl={coa_session.acl_out}",
                ],
            },
        }
    )
    request = coa_request(coa_generic)
    return request
