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

**Run script**
```
python main.py
```

## Environment variables
**Put this into your .env file**
1. GCP_PROJECTID="\<GCP Project\>"
2. ACCOUNTFILE_PATH=./keys.json
