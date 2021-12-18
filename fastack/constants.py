from enum import Enum
from typing import Dict, Union


class APIEndpoint(str, Enum):
    LIST = "LIST"
    RETRIEVE = "RETRIEVE"
    CREATE = "CREATE"
    UPDATE = "UPDATE"
    DESTROY = "DESTROY"


HTTP_METHODS = [
    "CONNECT",
    "DELETE",
    "GET",
    "HEAD",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
    "TRACE",
]

MAPPING_ENDPOINTS: Dict[Union[APIEndpoint, str], str] = {
    APIEndpoint.LIST: "",
    APIEndpoint.CREATE: "",
    APIEndpoint.RETRIEVE: "/{id}",
    APIEndpoint.UPDATE: "/{id}",
    APIEndpoint.DESTROY: "/{id}",
}
METHOD_ENDPOINTS: Dict[Union[APIEndpoint, str], str] = {
    APIEndpoint.LIST: "GET",
    APIEndpoint.CREATE: "POST",
    APIEndpoint.RETRIEVE: "GET",
    APIEndpoint.UPDATE: "PUT",
    APIEndpoint.DESTROY: "DELETE",
}
