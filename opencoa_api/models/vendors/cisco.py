from opencoa_api.models.generic import COAGenericSession


class CiscoCOAGenericSession(COAGenericSession):
    """Cisco COA Generic Model based on User-Name attribute

    Username can also be the Accounting Session ID (Acct-Session-Id) which is preferred."""

    username: str


class CiscoCOAService(CiscoCOAGenericSession):
    """Cisco COA Service Model"""

    service_name: str


class CiscoCOAPolicyChange(CiscoCOAGenericSession):
    """Cisco COA Model to change sub-qos-policy-(in|out)"""

    policy_in: str
    policy_out: str


class CiscoCOAACLChange(CiscoCOAGenericSession):
    """Cisco COA Model to change v4 ACL (in|out)"""

    acl_in: str
    acl_out: str
