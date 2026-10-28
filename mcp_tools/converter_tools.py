# Conversion logic and HTTP endpoints are defined here so they can be reused
# by both the FastAPI app and the MCP tool registrations.

from fastapi import APIRouter, HTTPException, status

router = APIRouter(prefix="", tags=["unit-conversion"])


# --- Core conversion helpers -------------------------------------------------
def lookup_ip_threat_intel(ip_address: str, maxAgeInDays: str) -> dict:
    """
    Query an external threat intel API (eg. AbuseIPDB)

    Args:
        ip_address: a valid IPv4 address to evaluate
        api_key: a valid API key which can be used to access the target database.

    Returns:
        JSON dictionary containing the abuse score, country, domain name.
    """
    return {"abuse_score": 40, "country": "AU", "domain_name": "Anonymous"}


def search_ip_in_logs_value(ip_address: str) -> str:
    """
    Search local logs for occurences of specified IP address.

    Args:
        ip_address: Target IPv4 address to filter logs against

    Returns:
        Formated string of log entries.
    """
    return {}


# --- FastAPI endpoints -------------------------------------------------------
@router.post("/lookup_ip_threat")
def lookup_ip_threat_intel(ip_address: str, maxAgeInDays: str = ""):
    """
    Query an external threat intel API (eg. AbuseIPDB)

    Args:
        ip_address: a valid IPv4 address to evaluate
        maxAgeInDays: maximum number of days for a report.

    Returns:
        JSON dictionary containing the abuse score, country, domain name, etc.
    """

    import requests
    import json
    import ipaddress

    try:
        valid_ip = ipaddress.IPv4Address(ip_address)
    except ipaddress.AddressValueError:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = f"'{ip_address}' is not a valid IPv4 address."
        )

    # Defining the api-endpoint
    url = 'https://api.abuseipdb.com/api/v2/check'

    querystring = {
        'ipAddress': {ip_address},
        'maxAgeInDays': {maxAgeInDays}
    }

    headers = {
        'Accept': 'application/json',
        'Key': 'c6f0c6526cdd23eb2667ab330ca2172026a50bc4c8b1bdc880ebdf57fef69533518ce8dbace1d552'
    }

    response = requests.request(method='GET', url=url, headers=headers, params=querystring)

    # Formatted output get response
    decodedResponse = json.loads(response.text)

    return decodedResponse


@router.post("/search_ip_in_logs")
def search_ip_in_logs_value(ip_address: str) -> str:
    """
    Search local logs for occurences of specified IP address.

    Args:
        ip_address: Target IPv4 address to filter logs against

    Returns:
        Formated string of log entries.
    """
    import ipaddress
    from pathlib import Path
    network_logs_path = Path(__file__).resolve().parent.parent / "mcp_resources" / "network_logs_sample.txt"

    try:
        valid_ip = ipaddress.IPv4Address(ip_address)
    except ipaddress.AddressValueError:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = f"'{ip_address}' is not a valid IPv4 address."
        )

    if not network_logs_path.exists():
        return f"Error: Log file not found at {network_logs_path}"
    
    network_logs = network_logs_path.read_text(encoding="utf-8")
    results = network_logs.splitlines()

    matching_IP = [line for line in results if ip_address in line]

    if not matching_IP:
        return f"No network log entries for IP address {ip_address} found."

    return f"Found {len(matching_IP)} entries for IP address {ip_address}:\n" + "\n".join(matching_IP)


# --- Metadata for MCP tool registration ----
# Students can edit these sample tool entries or replace them entirely
# with tool definitions for their own assessment context.


# --- Metadata for MCP tool registration ----
TOOL_DEFINITIONS = [
    {
        "name": "lookup_ip_threat_intel",
        "description": "Query an external threat intel API (eg. AbuseIPDB)",
        "func": lookup_ip_threat_intel,
        "tags": {"IP", "threat"},
    },
    {
        "name": "search_ip_in_logs_value",
        "description": "Search local logs for occurences of specified IP address",
        "func": search_ip_in_logs_value,
        "tags": {"IP_address", "log_files"},
    },
]