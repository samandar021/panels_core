from fastapi import HTTPException, status
from geoip2.webservice import AsyncClient

from modules.config_manager.config_manager import get_configs

config_geoip = get_configs()['common']['geoip']
api_key = config_geoip['api_key']
license_key = config_geoip['license_key']


async def find_county_by_ip(client_ip: str) -> str:
    async with AsyncClient(api_key, license_key) as client:
        response = await client.city(client_ip)
        country_name = response.country.name
        if country_name is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={'status': 'fail', 'code': 403, 'message': 'client ip not found'}
            )
        return country_name
