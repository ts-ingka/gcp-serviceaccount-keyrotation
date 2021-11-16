from oauth2client.client import GoogleCredentials
from googleapiclient import discovery
import base64
from flask import Flask
from dotenv import load_dotenv
import json
from os import getenv
load_dotenv()  # loads env variables from .env file in repo (easier than setting them manually)

app = Flask(__name__)


credentials = GoogleCredentials.get_application_default()
service = discovery.build('iam', 'v1', credentials=credentials)


def get_keys(sa):
    request = service.projects().serviceAccounts().keys().list(name=f"projects/{getenv('GCP_PROJECTID')}/serviceAccounts/{sa}")
    response = request.execute()
    return response


def filter_user_managed_keys(keys):
    return [key for key in keys["keys"] if key["keyType"] == "USER_MANAGED"]


def delete_gcp_keys(key_list):
    for key in key_list:
        print(f"Deleting key: {key['name']}", flush=True)
        request = service.projects().serviceAccounts().keys().delete(name=key["name"])
        request.execute()


def create_gcp_key(sa):
    request = service.projects().serviceAccounts().keys().create(name=f"projects/{getenv('GCP_PROJECTID')}/serviceAccounts/{sa}", body={
        "privateKeyType": "TYPE_GOOGLE_CREDENTIALS_FILE"
    })
    response = request.execute()
    return base64.b64decode(response["privateKeyData"])


@app.route("/rotate", methods=["POST"])
def rotate():
    try:
        with open(getenv("ACCOUNTFILE_PATH"), "r") as f:
            accounts = json.loads(f.read())

        for account in accounts["accounts"]:
            print(f"Extracing keys for {account}", flush=True)

            keys = get_keys(account)  # extract all keys
            user_keys = filter_user_managed_keys(keys)  # all user created keys

            print(f"Found {len(user_keys)} user managed keys", flush=True)

            if user_keys:
                delete_gcp_keys(user_keys)

            new_key = create_gcp_key(account)

            # TODO Implement logic to do something with the key
            # Remove this if you rather do something else
            # Example stores as json key on disk
            with open(f"{account}.json", "w") as f:
                f.write(json.dumps(json.loads(new_key)))

        return "Done", 200

    # TODO Implement exception logic
    except Exception as e:
        print(e)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
