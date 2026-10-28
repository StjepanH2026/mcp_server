"""Reusable MCP resources for the unit converter tutorial."""

from __future__ import annotations

from typing import Any, Dict


def AbuseIPDB() -> Dict[str, Any]:
    """
    An external IP database.

    Returns:
    Dictionary containing the AbuseIP DB abuse score and other data.
    """
    return {
        "ipaddress": "User entered IP address",
        "abuseConfidenceScore": "Abuse score associated with this IP, 0 being benign and 100 being malicious",
        "countryCode": "Two letter country code",
        "isp": "Original IP's Internet Service Provider name",
        "domain": "Domain associated with the IP address",
        "totalReports": "total number of reports filed against this IP address",
        "numDistinctUsers": "number of distinct user reports filed against this IP address",
        "lastReportedAt": "last report's date and time (ISO timestamp)",
    }


def network_logs() -> str:
    """
    Plain text network logs.

    Returns:
        Multi line string containing raw log files.
    """

    from pathlib import Path

    pcap_log_path = Path(__file__).resolve().parent / "network_logs_sample.txt"

    if pcap_log_path.exists():
        return pcap_log_path.read_text(encoding="utf-8")
    else:
        return "No network logs found."

# How would we scope this?
RESOURCE_DEFINITIONS = [
    {
        "name": "AbuseIPDB",
        "description": "JSON reference detailing AbuseIP DB threat level.",
        "mime_type": "application/json",
        "func": AbuseIPDB,
    },
    {
        "name": "network_logs",
        "description": "Plain text network firewall logs.",
        "mime_type": "text/plain",
        "func": network_logs,
    },
]
