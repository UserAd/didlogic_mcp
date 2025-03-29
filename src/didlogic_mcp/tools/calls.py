from mcp.server.fastmcp import FastMCP, Context
from . import base
from pydantic import Field
from typing import Optional, Literal


def register_tools(mcp: FastMCP):
    @mcp.tool()
    async def get_call_history(
        ctx: Context,
        call_type: Optional[Literal["sip", "incoming"]] = Field(
            description="Type of call, can be sip or incoming", default=None
        ),
        from_date: Optional[str] = Field(
            description="From date in format YYYY-MM-DD", Default=None
        ),
        to_date: Optional[str] = Field(
            description="To date in format YYYY-MM-DD", Default=None
        ),
        number: Optional[str | int] = Field(
            description="Number for search, E164 format", default=None
        ),
        sip_account: Optional[str | int] = Field(
            description="SIP Account name for search", default=None
        ),
        from_search: Optional[str | int] = Field(
            description="From number search, E164 format", default=None
        ),
        to_search: Optional[str | int] = Field(
            description="To number search, E164 format", default=None
        ),
        page: Optional[int] = Field(description="results page", default=None),
        per_page: Optional[int] = Field(
            description="results per page", default=None
        )
    ) -> str:
        """
            Query Call history in DIDlogic

            Args:
                call_type: Type of call history items where:
                    sip = outbound sip calls
                    incoming = inbound calls to DID
                from_date: Date to search from, should be in YYYY-MM-DD format
                to_date: Date to search to, should be in YYYY-MM-DD format
                number: Number to search for incoming calls
                sip_account: SIP account name to search for outbound calls
                from_search: Number from whom was the call
                to_search: Number to what was the call
                page: page of result starting with 1
                per_page: how many results should be on per page

            Returns a JSON object with a call history results where:
                calls: array of call history objects where:
                    timestamp: date of the call
                    type: call type where:
                        sip = outbound sip call
                        incoming = inbound call to DID
                    amount: charge for this call in USD
                    duration: duration of call in seconds
                    from: from number for this call
                    to: to number which this call was made
                    destination_name: destination network name for this call
                    sip_account: SIP account name for outbound SIP calls
                pagination: Pagination details for results
                    page: current page of results
                    per_page: results per page
                    total_pages: total pages results
                    total_records: total query records (maximum 5000)

            Example response:
            ```
                {
                    "calls": [
                        {
                            "timestamp": "2024-11-20T13:29:19Z",
                            "type": "sip",
                            "amount": 0.02,
                            "duration": 0,
                            "from": "\"\" <1212123123>",
                            "to": "1555123123",
                            "destination_name": "United States - NOT EXISTED",
                            "sip_account": "12345"
                        }
                    ],
                    "pagination": {
                        "page": 1,
                        "per_page": 100,
                        "total_pages": 50,
                        "total_records": 5000
                    }
                }
            ```
        """
        params = {}
        if call_type is not None:
            params["type"] = call_type
        if from_date is not None:
            params["from"] = from_date
        if to_date is not None:
            params["to"] = to_date
        if number is not None:
            params["filter"] = number
        if sip_account is not None:
            params["sip_account"] = sip_account
        if from_search is not None:
            params["from_search"] = from_search
        if to_search is not None:
            params["to_search"] = to_search
        if page is not None:
            params["page"] = page
        if per_page is not None:
            params["per_page"] = per_page

        response = await base.call_didlogic_api(
            ctx, "GET",
            "/v1/calls",
            params=params
        )

        return response.json()
