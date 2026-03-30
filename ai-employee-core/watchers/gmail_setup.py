"""Gmail Authentication Setup"""
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os

SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.send'
]

def authenticate_gmail():
    """Authenticate with Gmail and save token"""
    creds = None
    
    if os.path.exists('token.json'):
        print('Found existing token.json')
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print('Refreshing expired credentials...')
            creds.refresh(Request())
        else:
            print('Starting OAuth flow...')
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', 
                SCOPES
            )
            creds = flow.run_local_server(port=0)
        
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
        print('✅ token.json saved')
    
    print('✅ Gmail authentication successful!')
    return creds

if __name__ == '__main__':
    authenticate_gmail()
