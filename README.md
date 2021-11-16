# Example Flask/Python code on how to rotate GCP Service Account keys
**Note**
Flask is only used so it can be easily deployed in Cloud Run. Remove flask and deploy as Cloud Function for instance or run manually.

Create virtual environment
```
python -m venv venv
```

Enable venv (MacOS)
```
source venv/bin/activate
```

Install requirements
```
pip install -r requirements.txt
```

Create .env file to pass environment variables (and pass in values)
```
touch .env
```
Update *keys.json* file with your service accounts or modify the script to for instance connect to Firestore.

**Run script (will start flask Rest API)**
```
python main.py
```
**Run rotation**
```
POST http://127.0.0.1:8080/rotate
```

# Docker
#### Build
```
docker build -t gcp-key-rotation .
```
#### Run
```
docker run \
-v -v /path/to/keys:/tmp/keys:ro \
-e GCP_PROJECTID=<GCP Project> \
-e GOOGLE_APPLICATION_CREDENTIALS=/tmp/keys/<key>.json \
-p 8080:8080 \
gcp-key-rotation
```

## Environment variables
**Put this into your .env file**
1. GCP_PROJECTID="\<GCP Project\>"
2. ACCOUNTFILE_PATH=./keys.json
