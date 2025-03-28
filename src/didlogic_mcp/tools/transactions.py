from mcp.server.fastmcp import FastMCP, Context
from . import base
from pydantic import Field
from typing import Literal


def register_tools(mcp: FastMCP):
    @mcp.tool(description="Load transaction history from DIDLogic")
    async def get_transactions(
        ctx: Context,
        transaction_type: Literal[
            "adjustment", "activation", "month",
            "paypal_in", "call", "call_fix_fee",
            "sms", "cc_in", "stripe_in", "porting", "inbound_sms"
        ] = Field(description="Transaction type for search", default="month"),
        start_date: str = Field(
            description="Search start date in format YYYY-MM-DD"
        ),
        end_date: str = Field(
            description="Search end date in format YYYY-MM-DD"
        ),
    ) -> str:
        params = {}
        if transaction_type is not None:
            params["type"] = transaction_type
        if start_date is not None:
            params["start_date"] = start_date
        if end_date is not None:
            params["end_date"] = end_date

        result = await base.call_didlogic_api(
            ctx, "GET", "/v1/transactions", params=params
        )
        return result.text
