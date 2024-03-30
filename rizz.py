from flask import Flask, request, redirect
import requests

app = Flask(__name__)
CLIENT_ID = '1223598711100407910'
CLIENT_SECRET = 'lc6IB_TDID-dnd8YxvSCzerV2gYwUGPi'
REDIRECT_URI = 'http://localhost:5000/callback'
WEBHOOK_URL = 'https://discord.com/api/webhooks/1214597527521722488/Vp8XXa8dRxKI3bnt2DqZDrCwYbx-mndazm6v6kOYltBHMrB2JLAhq269BWqWjOOz8RiZ'

@app.route('/verify')
def verify():
    # Construct the verification link
    verification_link = f"https://discord.com/api/oauth2/authorize?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code&scope=identify%20email"

    return redirect(verification_link)

@app.route('/callback')
def callback():
    # Handle the OAuth2 callback
    code = request.args.get('code')
    
    # Exchange authorization code for access token
    data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'scope': 'identify email'
    }
    response = requests.post('https://discord.com/api/oauth2/token', data=data)
    access_token = response.json()['access_token']

    # Fetch user information including email
    headers = {'Authorization': f'Bearer {access_token}'}
    user_response = requests.get('https://discord.com/api/users/@me', headers=headers)
    user_data = user_response.json()
    username = user_data['username']
    email = user_data.get('email', 'Email not provided')

    # Send username and email to webhook
    data = {'content': f'Authenticated user: {username}, Email: {email}'}
    requests.post(WEBHOOK_URL, json=data)

    return 'Success.'

if __name__ == '__main__':

    app.run(debug=True)
