from mcp.server.fastmcp import FastMCP, Context
from . import base
from typing import Optional
from pydantic import Field


def register_tools(mcp: FastMCP):
    @mcp.tool()
    async def list_countries(
            ctx: Context,
            sms_enabled: Optional[bool] = Field(
                description="Filter for sms enabled numbers", default=None
            )
    ) -> str:
        """
            List available countries with DID for purchase on DIDLogic

            Args:
                sms_enabled: search for DID with SMS functionality

            Returns a JSON object with available countries for purchase.
            Returned countries list have following fields:
                id: ID of country
                name: Name of country in DIDLogic
                short_name: ISO code of country
                has_provinces_or_states: do country have provinces or states
                    which can be queried by list_country_regions tool.

            403 error indicates disabled API calls for purchase.

            Example:
            ```
                {
                    "countries": [
                        {
                            "id": 8669,
                            "name": "Argentina",
                            "short_name": "AR",
                            "has_provinces_or_states": false
                        }
                    ]
                }
            ```


        """
        params = {}
        if sms_enabled is not None:
            params["sms_enabled"] = int(sms_enabled)
        response = await base.call_didlogic_api(
            ctx,
            "GET",
            "/v2/buy/countries",
            params=params
        )
        return response.json()

    @mcp.tool()
    async def list_country_regions(
        ctx: Context,
        country_id: int = Field(description="Country ID"),
        sms_enabled: Optional[bool] = Field(
            description="Filter for sms enabled numbers", default=None
        )
    ) -> str:
        """
            List country regions with available DIDs for purchase

            Args:
                country_id: ID of country for search
                sms_enabled: search for DID with SMS functionality

            Returns a JSON object with available regions for purchase.
            Returned countries list have following fields:
                id: ID of region
                name: Name of region in DIDLogic
                short_name: short code for region

            403 error indicates disabled API calls for purchase.

            Example:
            ```
            {
                "regions": [
                    {
                        "id": 1,
                        "name": "Alberta",
                        "short_name": "AB"
                    }
            }
            ```
        """
        params = {}
        if sms_enabled is not None:
            params["sms_enabled"] = int(sms_enabled)

        response = await base.call_didlogic_api(
            ctx,
            "GET",
            f"/v2/buy/countries/{country_id}/regions",
            params=params
        )
        return response.json()

    @mcp.tool()
    async def list_country_cities(
        ctx: Context,
        country_id: int = Field(description="Country ID"),
        sms_enabled: Optional[bool] = Field(
            description="Filter for sms enabled numbers", default=None
        )
    ) -> str:
        """
            List of Cities with available DID for purchase in a country

            Args:
                country_id: ID of country for search
                sms_enabled: search for DID with SMS functionality

            Returns a JSON object with available cities for purchase DIDs.
            Returned cities list have following fields:
                id: ID of city
                name: Name of city in DIDLogic
                area_code: Area code within country
                count: count of available DIDs for purchasing

            403 error indicates disabled API calls for purchase.

            Example:
            ```
            {
                "cities": [
                    {
                        "id": 118557,
                        "name": "Ottawa-Hull, ON",
                        "area_code": "613800",
                        "count": 81
                    }
                ]
            }
            ```
        """
        params = {}
        if sms_enabled is not None:
            params["sms_enabled"] = int(sms_enabled)

        response = await base.call_didlogic_api(
            ctx,
            "GET",
            f"/v2/buy/countries/{country_id}/cities",
            params=params
        )
        return response.json()

    @mcp.tool()
    async def list_country_cities_in_region(
        ctx: Context,
        country_id: int = Field(description="Country ID"),
        region_id: int = Field(description="Region ID"),
        sms_enabled: Optional[bool] = Field(
            description="Filter for sms enabled numbers", default=None
        )
    ) -> str:
        """
            List of Cities with available DID in a region of a country

            Args:
                country_id: ID of country for search
                region_id: ID of region in a country
                sms_enabled: search for DID with SMS functionality

            Returns a JSON object with available cities for purchase DIDs.
            Returned cities list have following fields:
                id: ID of city
                name: Name of city in DIDLogic
                area_code: Area code within country
                count: count of available DIDs for purchasing

            403 error indicates disabled API calls for purchase.

            Example:
            ```
            {
                "cities": [
                    {
                        "id": 118557,
                        "name": "Ottawa-Hull, ON",
                        "area_code": "613800",
                        "count": 81
                    }
                ]
            }
            ```
        """
        params = {}
        if sms_enabled is not None:
            params["sms_enabled"] = int(sms_enabled)

        response = await base.call_didlogic_api(
            ctx,
            "GET",
            f"/v2/buy/countries/{country_id}/regions/{region_id}/cities",
            params=params
        )
        return response.json()

    @mcp.tool()
    async def list_dids_in_country_city(
        ctx: Context,
        country_id: int = Field(description="Country ID"),
        city_id: int = Field(description="City ID"),
        sms_enabled: Optional[bool] = Field(
            description="Filter for sms enabled numbers", default=None
        ),
        page: Optional[int] = Field(description="Search page", default=None),
        per_page: Optional[int] = Field(
            description="Search per page", default=None
        )
    ) -> str:
        """
            List of available DID in a city of a country

            Args:
                country_id: ID of country for search
                city_id: ID of city in a country
                sms_enabled: search for DID with SMS functionality
                page: page of result starting with 1
                per_page: how many results should be on per page

            Returns a JSON object with available DIDs where:
                dids: Array of DID available for purchasing where:
                    id: ID of DID
                    country: Country name
                    city: City name
                    sms_enabled: Is number capable of receiving SMS
                    channels: How many parallel channels have DID
                    free_min: How many free minutes per month DID have
                    activation: Activation cost for DID in USD
                    monthly: Monthly fee for DID
                    per_minute: Per minute cost for DID
                    origination_per_min: per minute cost if origin based rate applied
                    required_documents: required documents for activating number, where:
                        1 = Any form of ID
                        2 = Proof of address
                        3 = Proof of local address
                    number: DID Number in E164 format
                pagination: Pagination details for results
                    page: current page of results
                    total_pages: total pages results
                    total: total query records

            403 error indicates disabled API calls for purchase.

            Example:
            ```
            {
                "dids": {
                    "pagination": {
                        "total": 52,
                        "total_pages": 1,
                        "current_page": 1
                    },
                    "dids": [
                        {
                            "id": 112370,
                            "country": "Canada",
                            "city": "Edmonton, AB",
                            "sms_enabled": false,
                            "no_local_cli": false,
                            "channels": 4,
                            "free_min": 0,
                            "cnam": null,
                            "activation": 1.0,
                            "monthly": 1.0,
                            "per_minute": 0.01,
                            "origination_per_min": null,
                            "required_documents": [],
                            "state": "Alberta",
                            "country_short_name": "CA",
                            "number": "17806999999"
                        }
                    ]
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
            ctx,
            "GET",
            f"/v2/buy/countries/{country_id}/cities/{city_id}/dids",
            params=params
        )
        return response.json()

    @mcp.tool()
    async def purchase_did(
        ctx: Context,
        number: str | int = Field(
            description="DID number for purchase"
        )
    ) -> str:
        """
            Purchase DID from DIDLogic

            Args:
                number: DID number for purchase in E164 format

            Returns a JSON object with purchased DID details where:
                errors: Errors what happened in purchase process
                purchases: Array of purchased dids where:
                    id: ID of purchased DID
                    number: number of DID
                    country: Country name
                    area: City name
                    sms_enabled: Is number capable of receiving SMS
                    channels: How many parallel channels have DID
                    free_minutes: How many free minutes per month DID have
                    activation: Activation cost for DID in USD
                    monthly_fee: Monthly fee for DID
                    per_minute: Per minute cost for DID
                    origination_per_min: per minute cost if origin based rate applied
                    requir_docs: required documents for activating number, where:
                        1 = Any form of ID
                        2 = Proof of address
                        3 = Proof of local address
                    codec: what SIP codec is preferred for this number

            Example:
            ```
            {
                "purchase": {
                    "errors": {},
                    "purchases": [
                        {
                            "id": 728070,
                            "number": "17806999999",
                            "sms_enabled": false,
                            "no_local_cli": false,
                            "channels": 4,
                            "country": "Canada",
                            "area": "Edmonton, AB",
                            "free_minutes": 0,
                            "codec": "G711",
                            "require_docs": "",
                            "activation": 1.0,
                            "monthly_fee": 1.0,
                            "per_minute": 0.01,
                            "origination_per_min": 0.0
                        }
                    ]
                }
            }
            ```
        """
        response = await base.call_didlogic_api(
            ctx, "POST",
            "/v2/buy/purchase",
            data={"did_numbers": number}
        )
        return response.json()

    @mcp.tool()
    async def remove_purchased_did(
        ctx: Context,
        number: str | int = Field(
            description="Number for remove from DIDLogic account"
        )
    ) -> str:
        """
            Remove DID from DIDLogic account

            Args:
                number: DID number for removing in E164 format

            Returns a JSON object with removed DID details where:
                dids: Array of removed dids where:
                    id: ID of purchased DID
                    number: number of DID
                    country: Country name
                    area: City name
                    sms_enabled: Is number capable of receiving SMS
                    channels: How many parallel channels have DID
                    free_minutes: How many free minutes per month DID have
                    activation: Activation cost for DID in USD
                    monthly_fee: Monthly fee for DID
                    per_minute: Per minute cost for DID
                    origination_per_min: per minute cost if origin based rate applied
                    requir_docs: required documents for activating number, where:
                        1 = Any form of ID
                        2 = Proof of address
                        3 = Proof of local address
                    codec: what SIP codec is preferred for this number

            Example:
            ```
            {
                "dids": [
                    {
                        "id": 728070,
                        "number": "17806999999",
                        "sms_enabled": false,
                        "no_local_cli": false,
                        "channels": 4,
                        "country": "Canada",
                        "area": "Edmonton, AB",
                        "free_minutes": 0,
                        "codec": "G711",
                        "require_docs": "",
                        "activation": 1.0,
                        "monthly_fee": 1.0,
                        "per_minute": 0.01,
                        "origination_per_min": 0.0
                    }
                ]
            }
            ```
        """

        response = await base.call_didlogic_api(
            ctx, "DELETE",
            "/v2/buy/purchase",
            data={"did_numbers": number}
        )
        return response.json()
