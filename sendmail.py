import httplib2
import logging
from urllib import urlencode

MAILGUN_API_KEY = 'key-4b87291653134a800f45522ab1679d39'
MAILGUN_DOMAIN_NAME = 'mg.casparwre.de'
REQUEST_URL = 'https://api.mailgun.net/v3/{0}/messages'.format(MAILGUN_DOMAIN_NAME)
SUBJECT = "A story on Blankz.co was just completed"
BODY_TEXT = "Click here to see it: https://blankz.co/game/%s"
DEFAULT_RECIPIENT='caspar.wrede@gmail.com'

def gameComplete(game):
    http = httplib2.Http()
    http.add_credentials('api', MAILGUN_API_KEY)

    data = {
        'from': 'Blankz <no-reply@blankz.co>',
        'to': 'mail@blankz.co',
        'bcc': game.emails,
        'SUBJECT': SUBJECT,
        'text': BODY_TEXT % game.get_game_key()
    }
    resp, content = http.request(
        REQUEST_URL, 'POST', urlencode(data),
        headers={"Content-Type": "application/x-www-form-urlencoded"})

    if resp.status != 200:
        logging.error(
            'Mailgun API error: {} {}'.format(resp.status, content))
