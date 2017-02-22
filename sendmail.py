import httplib2
import logging
from urllib import urlencode

MAILGUN_API_KEY = 'key-4b87291653134a800f45522ab1679d39'
MAILGUN_DOMAIN_NAME = 'mg.casparwre.de'
request_url = 'https://api.mailgun.net/v3/{0}/messages'.format(MAILGUN_DOMAIN_NAME)
subject = "A story on Blankz.co was just completed"
body_text = "Click here to see it: https://flask-156210.appspot.com/game/%s"

def gameComplete(game):
    http = httplib2.Http()
    http.add_credentials('api', MAILGUN_API_KEY)

    data = {
        'from': 'Blankz <hello@blankz.co>',
        'to': game.emails,
        'subject': subject,
        'text': body_text % game.get_game_key()
    }

    resp, content = http.request(
        request_url, 'POST', urlencode(data),
        headers={"Content-Type": "application/x-www-form-urlencoded"})

    if resp.status != 200:
        logging.error(
            'Mailgun API error: {} {}'.format(resp.status, content))
