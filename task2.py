import base64
import requests
import json
from dotenv import load_dotenv
import os
load_dotenv('.env')

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

def access_token():
    try:
        credentials = f"{CLIENT_ID}:{CLIENT_SECRET}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        response = requests.post(
            'https://accounts.spotify.com/api/token',
            headers={"Authorization": f"Basic {encoded_credentials}"},
            data={"grant_type": "client_credentials"}
        )
        return response.json()["access_token"]
    except Exception as e:
        print("Error in Token Generation...", e)

def get_new_release():
    try:
        token = access_token()
        header = {"Authorization": f"Bearer {token}"}
        params = {"limit": 50}

        response = requests.get(
            "https://api.spotify.com/v1/browse/new-releases",
            headers=header,
            params=params
        )

        if response.status_code == 200:
            data = response.json()
            albums = data['albums']['items']

            release = []

            for i in albums:
                a = {
                    'album_name': i['name'],
                    'artist_name': i['artists'][0]['name'],
                    'release_date': i['release_date'],
                    'album_type': i['album_type'],
                    'total_tracks': i['total_tracks'],
                    'spotify_url': i['external_urls']['spotify'],
                    'album_image': i['images'][0]['url'] if i['images'] else None
                }
                release.append(a)
                # print(json.dumps(a, indent=2))

            with open('new_releases.json', 'w') as f:
                json.dump(release, f, indent=2)

            print("JSON data saved successfully to new_releases.json")

        else:
            print("API Error:", response.status_code, response.text)

    except Exception as e:
        print("Error in latest release data fetching...", e)

get_new_release()


import boto3


ACCESS_KEY=os.getenv("ACCESS_KEY")
ACCESS_SECRET=os.getenv("ACCESS_SECRET")
BUCKET_NAME = os.getenv("BUCKET_NAME")
REGION_NAME = os.getenv("REGION_NAME")
OBJECT_NAME = "moviesdata.json"
FILE_NAME = "new_releases.json"

try:
    s3_client = boto3.client(
        service_name="s3",
        region_name=REGION_NAME,
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=ACCESS_SECRET
    )

    s3_client.upload_file(FILE_NAME,BUCKET_NAME,OBJECT_NAME)

    print("File uploaded successfully to S3")

except Exception as e:
    print(" File is not uploaded:", e)