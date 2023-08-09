from aqvify import (AqvifyAPI, DeviceDataAPI)
import requests_mock

api = AqvifyAPI("https://public.aqvify.com", "secret-api-token")
device_data_api = DeviceDataAPI(api)
device_key = "AQ01337"


def mock_response(mock_request, endpoint, response):
    mock_request.get(
        f"https://public.aqvify.com/api/v1/DeviceData/{endpoint}",
        json=response,
        status_code=200,
        request_headers={"x-api-key": "secret-api-token"}
    )


def test_get_latest_value():
    MOCK_LATEST_VALUE_RESPONSE = {
        "dateTime": "2023-08-04T21:13:14+00:00",
        "waterLevel": -10.566849,
        "meterValue": 19.433151,
        "status": None
    }

    with requests_mock.Mocker() as mock_request:
        mock_response(mock_request, 'LatestValue', MOCK_LATEST_VALUE_RESPONSE)

        assert device_data_api.get_latest_value(
            device_key) == MOCK_LATEST_VALUE_RESPONSE


def test_get_day_aggregate_values():
    MOCK_DAY_AGGREGATE_RESPONSE = [
        {
            "dateTime": "2023-01-01T00:00:00+00:00",
            "minWaterLevel": -11.808182,
            "maxWaterLevel": -8.953991,
            "avgWaterLevel": -9.073668760750998,
            "validGroundWaterLevel": -8.953991,
            "inFlow": 229.19423041342733,
            "outVolume": 153.6682785322458,
            "minMeterValue": 18.191818,
            "maxMeterValue": 21.046009,
            "avgMeterValue": 20.926331239249002,
            "validGroundMeterValue": 21.046009
        },
        {
            "dateTime": "2023-01-02T00:00:00+00:00",
            "minWaterLevel": -12.668528,
            "maxWaterLevel": -7.04627,
            "avgWaterLevel": -8.999206529595627,
            "validGroundWaterLevel": -8.872566,
            "inFlow": 489.0206490716455,
            "outVolume": 136.11686312641382,
            "minMeterValue": 17.331472,
            "maxMeterValue": 22.95373,
            "avgMeterValue": 21.000793470404375,
            "validGroundMeterValue": 21.127434
        }
    ]

    with requests_mock.Mocker() as mock_request:
        mock_response(mock_request, 'DayAggregateValues',
                      MOCK_DAY_AGGREGATE_RESPONSE)

        latest_value_data = device_data_api.get_day_aggregate_values(
            device_key, begin_time='2023-01-01', end_time='2023-01-02')

        assert latest_value_data == MOCK_DAY_AGGREGATE_RESPONSE


def test_get_hour_aggregate_values():
    MOCK_HOUR_AGGREGATE_RESPONSE = [
        {
            "dateTime": "2023-01-01T00:00:00+00:00",
            "minWaterLevel": -10.241255,
            "maxWaterLevel": -8.965099,
            "avgWaterLevel": -9.162341813559323,
            "validGroundWaterLevel": -8.965099,
            "inFlow": 115.4453087329417,
            "outVolume": 16.850726119941523,
            "minMeterValue": 19.758745,
            "maxMeterValue": 21.034901,
            "avgMeterValue": 20.837658186440677,
            "validGroundMeterValue": 21.034901
        },
        {
            "dateTime": "2023-01-01T01:00:00+00:00",
            "minWaterLevel": -9.153214,
            "maxWaterLevel": -8.97274,
            "avgWaterLevel": -9.009268105263159,
            "validGroundWaterLevel": -8.975603,
            "inFlow": 13.339092003527902,
            "outVolume": 0,
            "minMeterValue": 20.846786,
            "maxMeterValue": 21.02726,
            "avgMeterValue": 20.990731894736843,
            "validGroundMeterValue": 21.024397
        }
    ]

    with requests_mock.Mocker() as mock_request:
        mock_response(mock_request, 'HourAggregateValues',
                      MOCK_HOUR_AGGREGATE_RESPONSE)

        latest_value_data = device_data_api.get_hour_aggregate_values(
            device_key, begin_time='2023-01-01T00:00', end_time='2023-01-01T01:00')

        assert latest_value_data == MOCK_HOUR_AGGREGATE_RESPONSE


def test_get_minute_values():
    MOCK_MINUTE_VALUES_RESPONSE = [
        {
            "dateTime": "2023-01-01T00:00:21+00:00",
            "waterLevel": -8.968798,
            "meterValue": 21.031202,
            "status": "Good"
        },
        {
            "dateTime": "2023-01-01T00:01:21+00:00",
            "waterLevel": -8.968864,
            "meterValue": 21.031136,
            "status": "Good"
        }
    ]

    with requests_mock.Mocker() as mock_request:
        mock_response(mock_request, 'MinuteValues',
                      MOCK_MINUTE_VALUES_RESPONSE)

        latest_value_data = device_data_api.get_minute_values(
            device_key, begin_time='2023-01-01T00:00', end_time='2023-01-01T00:02')

        assert latest_value_data == MOCK_MINUTE_VALUES_RESPONSE
