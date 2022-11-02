import webview
from flask import Flask, render_template, jsonify, request
import threading
from functools import wraps
import json

app = Flask(__name__)

@app.route('/')
def landing():
    return ''

def verify_token(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        """
        pass through wrapper
        """
        return function(*args, **kwargs)
    # def wrapper(*args, **kwargs):
    #     data = json.loads(request.data)
    #     token = data.get('token')
    #     if token == webview.token:
    #         return function(*args, **kwargs)
    #     else:
    #         raise Exception('Authentication error')

    return wrapper

def start_server():
    app.run(host='0.0.0.0', port=17080)

@app.route('/api/close', methods=['POST'])
@verify_token
def close():
    webview.windows[0].destroy()
    return jsonify({})

def _not_steel_focus(window):
    from qtpy.QtCore import Qt
    view = window.gui.BrowserView.instances['master']
    view.setWindowFlag(Qt.WindowDoesNotAcceptFocus)

def show_image(window, imgpath):
    import time
    time.sleep(0.1)
    window.load_html(f'<img src="{imgpath}" alt=""/>')
    _not_steel_focus(window)

import urllib
def get_youtube_id(value):
    """
    see: https://stackoverflow.com/questions/4356538/how-can-i-extract-video-id-from-youtubes-link-in-python

    Examples:
    - http://youtu.be/SA2iWivDJiE
    - http://www.youtube.com/watch?v=_oPAwA_Udwc&feature=feedu
    - http://www.youtube.com/embed/SA2iWivDJiE
    - http://www.youtube.com/v/SA2iWivDJiE?version=3&amp;hl=en_US
    """
    query = urllib.parse.urlparse(value)
    if query.netloc == 'youtu.be':
        return query.path[1:]
    if query.netloc in ('www.youtube.com', 'youtube.com'):
        if query.path == '/watch':
            p = urllib.parse.parse_qs(query.query)
            return p['v'][0]
        if query.path[:7] == '/embed/':
            return query.path.split('/')[2]
        if query.path[:3] == '/v/':
            return query.path.split('/')[2]
    # fail?
    return None

def show_youtube(window, url):
    videoid = get_youtube_id(url)
    if videoid is None:
        print('failed to parse youtube url. abort')
        window.destroy()
        return
    htmlcode = f"""
    <html>
    <head>
    <style>
    .videoContainer {{
      position: absolute;
      width: 100%;
      height: 100%;
      top: 0;
      left: 0;
      bottom: 0;
      right: 0;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
    }}
    iframe {{
      width: 100%;
      height: 100%; 
    }}
    </style>
    </head>
    <body>
    <div class="videoContainer">
        <iframe class="videoContainer__video" width="1920" height="1080" src="http://www.youtube.com/embed/{videoid}?modestbranding=1&autoplay=1&controls=1&fs=0&loop=0&rel=0&showinfo=0&disablekb=1" frameborder="0"></iframe>
    </div>
    </body></html>
    """

    import time
    time.sleep(0.1)
    window.load_html(htmlcode)
    _not_steel_focus(window)

if __name__ == '__main__':
    t = threading.Thread(target=start_server)
    t.daemon = True
    t.start()

    print(webview.token)
    window = webview.create_window('', transparent=True, on_top=True, frameless=True, hidden=False)

    # show image
    webview.start(show_image, [window, '/home/sifi/sandbox/popup_webview/Tux.jpg'], gui='qt')

    # show youtube
    # webview.start(show_youtube, [window, 'https://www.youtube.com/watch?v=be_XkA6pEQc'], gui='qt')
