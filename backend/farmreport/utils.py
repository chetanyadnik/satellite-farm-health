import requests
import datetime

CLIENT_ID = "822f360a-afa8-44f8-8186-25ed9f024d03"
CLIENT_SECRET = "VNBmHcII8cz4HpdARCJF5k3x4bPOY3aR"

OAUTH_URL = 'https://services.sentinel-hub.com/oauth/token'
PROCESS_URL = 'https://services.sentinel-hub.com/api/v1/process'

def authenticate():
    response = requests.post(OAUTH_URL, data={
        'grant_type': 'client_credentials',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    })
    response.raise_for_status()
    return response.json()['access_token']

# def get_ndvi_from_sentinel(farm_polygon):
    access_token = authenticate()

    today = datetime.date.today()
    date_from = (today - datetime.timedelta(days=30)).isoformat()
    date_to = today.isoformat()

    payload = {
        "input": {
            "bounds": {
                "geometry": farm_polygon['geometry']
            },
            "data": [{
                "type": "sentinel-2-l2a",
                "dataFilter": {
                    "timeRange": {
                        "from": f"{date_from}T00:00:00Z",
                        "to": f"{date_to}T23:59:59Z"
                    }
                }
            }]
        },
        "output": {
            "responses": [{
                "identifier": "default",
                "format": {
                    "type": "image/tiff"
                }
            }]
        },
        "evalscript": """
        //VERSION=3
        function setup() {
          return {
            input: ["B08", "B04"],
            output: { bands: 1 }
          };
        }
        function evaluatePixel(sample) {
          let ndvi = (sample.B08 - sample.B04) / (sample.B08 + sample.B04);
          return [ndvi];
        }
        """
    }

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    response = requests.post(PROCESS_URL, json=payload, headers=headers)

    if response.status_code == 200:
        # Save the TIFF image locally
        with open("farm_ndvi.tiff", "wb") as f:
            f.write(response.content)

        return {"status": "success", "message": "NDVI image saved as farm_ndvi.tiff"}
    else:
        return {"status": "error", "message": response.text}


def get_ndvi_from_sentinel(farm_polygon, width=1024, height=1024):
    access_token = authenticate()

    today = datetime.date.today()
    date_from = (today - datetime.timedelta(days=30)).isoformat()
    date_to = today.isoformat()

    payload = {
        "input": {
            "bounds": {
                "geometry": farm_polygon['geometry']
            },
            "data": [{
                "type": "sentinel-2-l2a",
                "dataFilter": {
                    "timeRange": {
                        "from": f"{date_from}T00:00:00Z",
                        "to": f"{date_to}T23:59:59Z"
                    }
                }
            }]
        },
        "output": {
            "width": width,
            "height": height,
            "responses": [{
                "identifier": "default",
                "format": {
                    "type": "image/tiff"
                }
            }]
        },
        "evalscript": """
        //VERSION=3
        function setup() {
          return {
            input: ["B08", "B04"],
            output: { bands: 1, sampleType: "FLOAT32" }
          };
        }

        function evaluatePixel(sample) {
          let denominator = sample.B08 + sample.B04;
          if (denominator === 0) {
            return [0];
          }
          let ndvi = (sample.B08 - sample.B04) / denominator;
          return [ndvi];
        }
        """
    }

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    response = requests.post(PROCESS_URL, json=payload, headers=headers)

    if response.status_code == 200:
        with open("farm_ndvi.tiff", "wb") as f:
            f.write(response.content)
        return {"status": "success", "message": "NDVI image saved as farm_ndvi.tiff"}
    else:
        return {"status": "error", "message": response.text}
