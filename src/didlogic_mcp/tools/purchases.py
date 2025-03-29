from mcp.server.fastmcp import FastMCP, Context
from . import base
from pydantic import Field
from typing import Optional


def register_tools(mcp: FastMCP):
    @mcp.tool()
    async def list_purchases(
        ctx: Context,
        page: Optional[int] = Field(
            description="Page for purchases", default=None
        ),
        per_page: Optional[int] = Field(
            description="Results per page", default=None
        )
    ) -> str:
        """
            List purchased DIDs in DIDLogic

            Args:
                page: page of result starting with 1
                per_page: how many results should be on per page

            Returns a JSON object with a call history results where:
                purchases: List of purchased DIDs
                    number: Number of DID
                    channels: How many parallel channels DID have
                    country: Country name
                    area: City name
                    free_minutes: How many free minutes per month DID have
                    activation: Activation cost for DID in USD
                    monthly_fee: Monthly fee for DID
                    per_minute: Per minute cost for DID
                    codec: what SIP codec is preferred for this number
                    check_state: DID state

                pagination: Pagination details for results
                    page: current page of results
                    per_page: results per page
                    total_pages: total pages results
                    total_records: total query records (maximum 5000)

            Example response:
            ```
            {
                "purchases": [
                    {
                        "number": "441172999999",
                        "channels": 2,
                        "country": "United Kingdom",
                        "area": "Bristol",
                        "codec": "G711",
                        "activation": 0.0,
                        "monthly_fee": 0.99,
                        "per_minute": 0.001,
                        "check_state": "checked",
                        "free_minutes": 0
                    }
                ],
                "pagination": {
                    "pages": 1,
                    "page": 1,
                    "per_page": 100,
                    "total_records": 50
                }
            }
            ```
        """
        params = {}
        if page is not None:
            params["page"] = page
        if per_page is not None:
            params["per_page"] = per_page
        response = await base.call_didlogic_api(
            ctx, "GET",
            "/v1/purchases",
            params=params
        )
        return response.json()

    @mcp.tool()
    async def list_destinations(
            ctx: Context,
            number: str | int = Field(description="DID Number")
    ) -> str:
        """
            List DID destination.

            Args:
                number: DID number in DIDLogic

            Returns a JSON object with all did destinations where:
                id: ID of destination
                destination: destination
                priority: priority of selection
                callhunt: flag indicates do destination is part of ring all group
                active: flag indicates is destination enabled or not
                transport: transport of destination where:
                    1 = SIP address destination (ex: 123@example.com)
                    4 = PSTN (phone number) destination (ex: 15551231233)
                    5 = SIP account destination (ex: 12345)

            Example:
            ```
            {
                "destination": [
                    {
                        "id": 1234455,
                        "destination": "12345",
                        "priority": 1,
                        "callhunt": false,
                        "active": true,
                        "transport": 5
                    }
                ]
            }
            ```
        """

        response = await base.call_didlogic_api(
            ctx,
            "GET",
            f"/v1/purchases/{number}/destinations"
        )
        return response.json()

    @mcp.tool()
    async def add_destination(
        ctx: Context,
        number: str | int = Field(description="DID Number"),
        callhunt: bool = Field(
            description="Is it ring all group number", default=False
        ),
        active: bool = Field(
            description="Is this destination active", default=False
        ),
        transport: int = Field(
            description="Transport for destination", default=1
        ),
        destination: str | int = Field(description="Destination for DID")
    ) -> str:
        """
            Add a DID destination.

            Args:
                number: DID number in DIDLogic
                callhunt: flag indicates do destination is part of ring all group
                active: flag indicates is destination enabled or not
                transport: transport of destination where:
                    1 = SIP address destination (ex: 123@example.com)
                    4 = PSTN (phone number) destination (ex: 15551231233)
                    5 = SIP account destination (ex: 12345)
                destination: destination

            Returns a JSON object with did destination where:
                id: ID of destination
                destination: destination
                priority: priority of selection
                callhunt: flag indicates do destination is part of ring all group
                active: flag indicates is destination enabled or not
                transport: transport of destination where:
                    1 = SIP address destination (ex: 123@example.com)
                    4 = PSTN (phone number) destination (ex: 15551231233)
                    5 = SIP account destination (ex: 12345)

            Example:
            ```
            {
                "did_destination": {
                    "id": 1234455,
                    "destination": "12345",
                    "priority": 1,
                    "callhunt": false,
                    "active": true,
                    "transport": 5
                }
            }
            ```
        """
        data = {
            "destination[callhunt]": int(callhunt),
            "destination[active]": int(active),
            "destination[transport]": transport,
            "destination[destination]": destination
        }
        response = await base.call_didlogic_api(
            ctx, "POST", f"/v1/purchases/{number}/destinations",
            data=data
        )
        return response.json()

    @mcp.tool()
    async def delete_destination(
        ctx: Context, number: str | int = Field(
            description="DID Number"), id: int = Field(
            description="Destination ID from list_destinations")) -> str:
        """
            Remove destination from DID.

            Args:
                number: DID number in DIDLogic
                id: destination ID to remove

            Returns a `Destination deleted` on success
        """

        await base.call_didlogic_api(
            ctx, "DELETE",
            f"/v1/purchases/{number}/destinations/{id}"
        )
        return "Destination deleted"
