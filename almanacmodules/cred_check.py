#!/bin/env python

""" this module validates the credentials stored in a token.json
    to give readonly access to the google sheet. If the credential
    validation fails, which is common as it has a short expiration date,
    then the user will be prompted to sign into google to gain access again.
"""

# BUILT INS
import os.path

# THIRD PARTY
from google.auth.transport.requests import Request
from google.oauth2.credentials import (
    Credentials,
)
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

def confirmation():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
    with open("token.json", "w") as token:
        token.write(creds.to_json())
    return creds
