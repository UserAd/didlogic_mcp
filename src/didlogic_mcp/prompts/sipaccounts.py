"""
SIP Account Prompts for Didlogic MCP Server
These prompts help users manage their SIP accounts (sipfriends).
"""

from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts import base


def register_prompts(mcp: FastMCP):
    """Register all SIP account-related prompts with the MCP server"""

    @mcp.prompt()
    def delete_sipaccount() -> list[base.Message]:
        """Help user delete sipaccount"""
        return [
            base.UserMessage("I do not need anymore one of my sipaccount"),
            base.AssistantMessage("I'll help you delete a SIP account. I'll need some information from you:"),
            base.AssistantMessage("What name it have?")]

    @mcp.prompt()
    def list_all_sipaccounts() -> str:
        """List all SIP accounts and their details"""
        return (
            "Please list all my Didlogic SIP accounts and provide a summary "
            "of each account including its name, label, caller ID, and any restrictions. "
            "Format the information in a clear, easy-to-read table.")

    @mcp.prompt()
    def create_new_sipaccount() -> list[base.Message]:
        """Guide the user through creating a new SIP account"""
        return [
            base.UserMessage(
                "I need to create a new SIP account on my Didlogic account. "
                "Please help me set up a properly configured account."
            ),
            base.AssistantMessage(
                "I'll help you create a new SIP account. I'll need some information from you:"
            ),
            base.AssistantMessage(
                "1. What password would you like to use?\n"
                "2. What caller ID should be associated with this account?\n"
                "3. What label or name would you like to give this account?\n"
                "4. Do you want to set up any restrictions like IP restrictions or call limits?"
            )
        ]

    @mcp.prompt()
    def enable_ip_restriction_for_sipaccount() -> list[base.Message]:
        """Enable IP restriction for selected SIP account"""
        return [
            base.UserMessage(
                "I need to enable ip restriction for sip account "
                "And add IP to allowed list"
            ),
            base.AssistantMessage(
                "First I will add IP to allowed list. "
            ),
            base.AssistantMessage(
                "Now I can change IP restriction setting in SIP account."
            )
        ]

    @mcp.prompt()
    def manage_allowed_ips() -> str:
        """Manage IP restrictions for a SIP account"""
        return (
            "I need to manage the allowed IP addresses for one of my Didlogic SIP accounts. "
            "Please help me see the current IP restrictions, add new IPs, or remove existing ones.")

    @mcp.prompt()
    def update_sipaccount() -> str:
        """Updates sipaccount settings"""
        return (
            "I need to change settings for one of my Didlogic SIP account."
        )

    @mcp.prompt()
    def update_sipaccount_security() -> list[base.Message]:
        """Update security settings for a SIP account"""
        return [
            base.UserMessage(
                "I'm concerned about the security of my SIP accounts. "
                "Please help me review and update the security settings."
            ),
            base.AssistantMessage(
                "I'll help you secure your SIP accounts. First, let me check your current accounts."
            ),
            base.AssistantMessage(
                "For each account, we should consider:\n"
                "1. Password strength\n"
                "2. IP restrictions\n"
                "3. Call limits and restrictions\n"
                "4. Cost limits\n"
                "Let me analyze your accounts and suggest improvements."
            )
        ]

    return mcp
