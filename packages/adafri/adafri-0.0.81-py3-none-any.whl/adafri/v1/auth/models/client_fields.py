
from dataclasses import dataclass
from typing import Any
from utils.utils import DictUtils

@dataclass
class ClientFields:
    id = "id"
    name = "name"
    uid = "uid"
    description = "description"
    client_id = "client_id"
    client_secret = "client_secret"
    redirect_uris = "redirect_uris"
    allowed_redirect_uris = "allowed_redirect_uris"
    uri = "uri"
    grant_types = "grant_types" 
    response_types = "response_types"
    token_endpoint_auth_method  = "token_endpoint_auth_method"
    scopes = "scopes"
    client_id_issued_at = "client_id_issued_at"
    created_at = "createdAt"

    @staticmethod
    def keys():
        return DictUtils.get_keys(ClientFieldProps);

    @staticmethod
    def filtered_keys(field, condition=True):
        mutable = DictUtils.filter(ClientFieldProps, DictUtils.get_keys(ClientFieldProps), field, condition)
        return DictUtils.get_keys(mutable);

ClientFieldProps = {
     ClientFields.id: {
        "type": str,
        "required": True,
        "mutable": False,
        "editable": False,
        "interactive": True,
        "default_value": "",
        "pickable": True
    },
    ClientFields.name: {
        "type": str,
        "required": True,
        "mutable": True,
        "editable": False,
        "interactive": True,
        "default_value": "",
        "pickable": True
    },
    ClientFields.uid: {
        "type": str,
        "required": True,
        "mutable": True,
        "editable": False,
        "interactive": True,
        "default_value": "",
        "pickable": True
    },
    ClientFields.description: {
        "type": str,
        "required": True,
        "mutable": True,
        "editable": False,
        "interactive": True,
        "default_value": "",
        "pickable": True
    },
    ClientFields.client_id: {
        "type": str,
        "required": True,
        "mutable": False,
        "editable": False,
        "interactive": True,
        "default_value": "",
        "pickable": True
    },
    ClientFields.uri: {
        "type": str,
        "required": True,
        "mutable": True,
        "editable": True,
        "interactive": True,
        "default_value": "",
        "pickable": True
    },
    ClientFields.token_endpoint_auth_method: {
        "type": str,
        "required": True,
        "mutable": True,
        "editable": False,
        "interactive": True,
        "default_value": "",
        "pickable": True
    },
    ClientFields.client_secret: {
        "type": str,
        "required": True,
        "mutable": False,
        "editable": False,
        "interactive": True,
        "default_value": "",
        "pickable": True
    },
    ClientFields.redirect_uris: {
        "type": list,
        "required": True,
        "mutable": True,
        "editable": False,
        "interactive": True,
        "default_value": [],
        "pickable": True
    },
    ClientFields.allowed_redirect_uris: {
        "type": list,
        "required": True,
        "mutable": True,
        "editable": False,
        "interactive": True,
        "default_value": [],
        "pickable": True
    },
    ClientFields.grant_types: {
        "type": list,
        "required": True,
        "mutable": True,
        "editable": False,
        "interactive": True,
        "default_value": [],
        "pickable": True
    },
    ClientFields.response_types: {
        "type": list,
        "required": True,
        "mutable": True,
        "editable": False,
        "interactive": True,
        "default_value": [],
        "pickable": True
    },
    ClientFields.scopes: {
        "type": list,
        "required": True,
        "mutable": True,
        "editable": False,
        "interactive": True,
        "default_value": [],
        "pickable": True
    },
    ClientFields.client_id_issued_at: {
        "type": int,
        "required": True,
        "mutable": False,
        "editable": False,
        "interactive": True,
        "default_value": 0,
        "pickable": True
    },
    ClientFields.created_at: {
        "type": str,
        "required": True,
        "mutable": False,
        "editable": False,
        "interactive": True,
        "default_value": 0,
        "pickable": True
    },
}

STANDARD_FIELDS = ClientFields.filtered_keys('pickable', True)