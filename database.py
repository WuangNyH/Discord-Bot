import firebase_admin
from firebase_admin import credentials, firestore_async

cred = credentials.Certificate("./etc/secrets/discord-bot-edfdd-firebase-adminsdk-fbsvc-f30ce15c92.json")
firebase_admin.initialize_app(cred)

db = firestore_async.client()
