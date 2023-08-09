from aqvify import (AqvifyAPI, DevicesAPI)
import requests_mock

MOCK_DEVICES_RESPONSE = [
    {"deviceKey": "AQ01337", "name": "AQ01337 Strandvägen"},
    {"deviceKey": "DEMO", "name": "Min brunn"},
]

def test_get_devices():
    with requests_mock.Mocker() as mock_request:
        base_url = "https://public.aqvify.com"
        mock_request.get(
            f"{base_url}/api/v1/Device/Devices",
            json=MOCK_DEVICES_RESPONSE,
            status_code=200,
            request_headers={"x-api-key": "secret-api-token"}
        )

        api = AqvifyAPI(base_url, "secret-api-token")

        devices_api = DevicesAPI(api)

        devices_data = devices_api.get_devices()

        assert devices_data == MOCK_DEVICES_RESPONSE
