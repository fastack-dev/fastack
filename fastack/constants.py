from enum import Enum
from typing import Dict


class APIEndpoint(str, Enum):
    LIST = "list"
    RETRIEVE = "retrieve"
    CREATE = "create"
    UPDATE = "update"
    DESTROY = "destroy"


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

MAPPING_ENDPOINTS: Dict[str, str] = {
    APIEndpoint.LIST.value: "",
    APIEndpoint.CREATE.value: "",
    APIEndpoint.RETRIEVE.value: "/{id}",
    APIEndpoint.UPDATE.value: "/{id}",
    APIEndpoint.DESTROY.value: "/{id}",
}
METHOD_ENDPOINTS: Dict[str, str] = {
    APIEndpoint.LIST.value: "GET",
    APIEndpoint.CREATE.value: "POST",
    APIEndpoint.RETRIEVE.value: "GET",
    APIEndpoint.UPDATE.value: "PUT",
    APIEndpoint.DESTROY.value: "DELETE",
}
