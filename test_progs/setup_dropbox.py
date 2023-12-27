import webbrowser

APP_KEY = '70yem8c9kt0r29f'
url = f'https://www.dropbox.com/oauth2/authorize?client_id={APP_KEY}&' \
      f'response_type=code&token_access_type=offline'

webbrowser.open(url)