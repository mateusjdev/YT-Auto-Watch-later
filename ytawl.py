import os
import sys
import json

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube",
          "https://www.googleapis.com/auth/youtube.force-ssl",
          "https://www.googleapis.com/auth/youtube.readonly",
          "https://www.googleapis.com/auth/youtubepartner"]

def main():
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    api_key = '' 
    if os.path.exists("apikey.txt"):
        with open('apikey.txt','r') as f:
            api_key = f.read()
    else:
        print("Api key need to be in apikey.txt file")
        sys.exit(1)
    youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey = api_key)
    nextPageToken = ['CDIQAQ','CDIQAA','CGQQAA']
    channelIds = []
    x = 0
    while(True):
        request = youtube.subscriptions().list(
            part="snippet",
            channelId="UCtY032ta9rjNv7oufabX9Pw",
            maxResults=50,
            pageToken=nextPageToken[x],
            fields="nextPageToken,items(snippet(resourceId(channelId)))"
        )
        response = request.execute()

        jdata = json.loads(json.dumps(response))

        for id in jdata['items']:
            channelIds.append(id['snippet']['resourceId']['channelId'])

        if not 'nextPageToken' in response:
            break
        x += 1

    with open('output.txt','w') as f:
        for id in channelIds:
            f.write(id + "\n")

if __name__ == "__main__":
    main()