from mcp.server.fastmcp import FastMCP, Context
from . import base
from pydantic import Field
from typing import Literal


def register_tools(mcp: FastMCP):
    @mcp.tool()
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
        """
            Load transaction history from DIDLogic

            Args:
                transaction_type: Type of transaction to search where:
                    adjustment = Adjustments made by DIDLogic finances
                    activation = Activation payments for DID
                    month = Monthly payments for DID
                    paypal_in = Paypal TopUps
                    call = Per minute charges for inbound calls
                    call_fix_fee = Per minute charges for PSTN DID destinations
                    sms = SMS charges
                    inbound_sms = Inbound SMS charges
                    cc_in = Credit card TopUps
                    stripe_in = Stripe express payments TopUps
                    porting = Porting Fees
                start_date: Search start date in format YYYY-MM-DD
                end_date: Search end date in format YYYY-MM-DD

            Returns a CSV table of transactions where:
                Date: Date of transaction
                Time: Time of transaction
                Transaction type: Type of transaction
                Comment: Comment for transaction
                Amount: Transaction Amount
                Balance: Balance after transaction creation
                Status: Transaction status where:
                    Confirmed = transaction confirmed but not commited yet
                    Committed = transaction settled
                    Rejected = transaction reverted back

            Example:
            ```
            Date,Time,Transaction type,Comment,Amount,Balance,Status
            01/05/25,06:00 am,Monthly fees,Monthly fee for 18565999999,$-0.9900,$16.1273,Committed
            ```
        """
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
