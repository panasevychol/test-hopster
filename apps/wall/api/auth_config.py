import endpoints


WEB_CLIENT_ID = 'replace this with your web client application ID'
ANDROID_CLIENT_ID = 'replace this with your Android client ID'
IOS_CLIENT_ID = 'replace this with your iOS client ID'
ANDROID_AUDIENCE = WEB_CLIENT_ID
ALLOWED_CLIENT_IDS = [
    WEB_CLIENT_ID, ANDROID_CLIENT_ID, IOS_CLIENT_ID,
    endpoints.API_EXPLORER_CLIENT_ID]
