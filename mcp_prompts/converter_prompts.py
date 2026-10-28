from __future__ import annotations

from fastmcp.prompts import Message

def Investigate_IP_prompt() -> list[Message]:
    """
    Message list guiding the LLM through an IP investigation workflow.

    Returns:
        Conversation template containing FastMCP Message objects.
    """
    return [
        Message(
            {
                "role": "system",
                "content": (
                    "You are a Security Operations Centre (SOC) Analyst. When given an IP address perform a complete triage by following these steps:\n"
                    "1. Call the 'lookup_ip_threat_intel' tool to query AbuseIPDB for the target IP\n"
                    "2. Interpret the returned abuse confidence score, ISP, and country of origin\n"
                    "3. Perform a clear threat assessment for the user\n"
                    "4. List the following data in an organised manner; ipaddress, abuseConfidenceScore, country, isp, domain, hostnames, totalReports, numDistinctUsers, lastReportedAt."
                ),
            }
        ),
        Message(
            {
                "role": "user",
                "content": (
                    "Perform a threat analysis for the following IP address: {ip_address}."
                ),
            }
        ),
    ]


def search_local_logs_prompt() -> list[Message]:
    """
    Message list that drafts an HTTP example for the learner.

    Returns:
        Conversation template containing FastMCP Message objects.
    """
    return [
        Message(
            {
                "role": "system",
                "content": (
                    "You are a Security Operations Centre (SOC) Analyst. When the user provides an IP address, do the following:\n"
                    "1. Invoke the 'search_ip_in_logs_value' tool using the provided IP address\n"
                    "2. Parse the returned log entries and present a clear cronological timeline of the events associated with this IP address\n"
                    "3. Highlight key details such as; timestamp, protocol/port, username, success/fail status\n"
                    "4. State whether you believe this activity to be benign or a threat\n"
                )
            }
        ),
        Message(
            {
                "role": "user",
                "content": (
                    "Perform a threat analysis for the following IP address: {ip_address}."
                )
            }
        ),
    ]


PROMPT_DEFINITIONS = [
    {
        "name": "Investigate_IP",
        "description": (
            "Query AbuseIPDB for an IP address threat score and reputation."
        ),
        "func": Investigate_IP_prompt,
    },
    {
        "name": "Search_local_logs",
        "description": (
            "Take user's entered IP address and search the local network log directory for matching activity."
        ),
        "func": search_local_logs_prompt,
    },
]