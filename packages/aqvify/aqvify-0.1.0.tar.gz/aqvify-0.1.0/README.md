# python-aqvify

A python module for reading values of Aqvify through the official API.

## Installation

```bash
pip install aqvify
```

## Usage

```python
from aqvify import (AqvifyAPI, DevicesAPI)

api = AqvifyAPI("https://public.aqvify.com", "secret-api-token")

devices_api = DevicesAPI(api)

devices_data = devices_api.get_devices()
```
