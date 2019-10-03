import datetime
from time import gmtime,localtime, strftime
import time

from flask import Flask
from flask import jsonify
import socket

# print a nice greeting.
def say_hello(username = "World"):
    return 'Hello %s!</p>\n' % username


def get_date_time():
    secs = int(time.time())
    dtval = localtime()
    return jsonify(date=strftime("%d %b %Y ", dtval),
                   day=strftime("%A", dtval),
                   timezone=strftime("%Z (%z)", dtval),
                   time=strftime('%X', dtval),
                   hostname=socket.gethostname(),
                   epoc=secs)


# some bits of text for the page.
header_text = '''
    <html>\n<head> <title>EB Flask Test</title> </head>\n<body>'''
instructions = '''
    <p><em>Hint</em>: This is a RESTful web service! Append a username
    to the URL (for example: <code>/Thelonious</code>) to say hello to
    someone specific.</p>\n
    <h2>links</h2>
    <ul>
        <li><a href="./freddy">Hello Freddy</a></li>
        <li><a href="./date">Get date</a></li>
        <li><a href="./">home</a></li>
    </ul>
    '''
home_link = '<p><a href="/">Back</a></p>\n'
footer_text = '</body>\n</html>'

# EB looks for an 'application' callable by default.
application = Flask(__name__)

# add a rule for the index page.
application.add_url_rule('/', 'index', (lambda: header_text +
        say_hello() + instructions + footer_text))



# add a rule when the page is accessed with a name appended to the site
# URL.
application.add_url_rule('/<username>', 'hello', (lambda username:
    say_hello(username) + home_link))


application.add_url_rule('/date', 'next', get_date_time)


# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()