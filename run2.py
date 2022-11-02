# -*- coding: utf-8 -*-
from contextlib import redirect_stdout, redirect_stderr
from functools import wraps
from io import StringIO
import json
import logging
import sys
import threading
import webview

log = logging.getLogger(__name__)

def run_server_on_end(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        ret = function(*args, **kwargs)
        stdinout_server(*args, **kwargs)
    return wrapper

def _not_steel_focus(window):
    from qtpy.QtCore import Qt
    view = window.gui.BrowserView.instances['master']
    view.setWindowFlag(Qt.WindowDoesNotAcceptFocus)
    # for key, view in window.gui.BrowserView.instances.items():
    #     if key == 'master':
    #         view.setWindowFlag(Qt.WindowDoesNotAcceptFocus)

def stdinout_server(window, *args, **kwargs):
    import time
    time.sleep(1)
    _not_steel_focus(window)
    while line := sys.stdin.readline():
        if line.startswith('close'):
            window.destroy()
            return
        elif line.startswith('hide'):
            window.hide()
        elif line.startswith('show'):
            window.show()
        elif line.startswith('youtube'):
            url = line[len('youtube '):]
            show_youtube(window, url)
            window.show()
        elif line.startswith('image'):
            path = line[len('image '):]
            show_image(window, path)
            window.show()
        else:
            print('{"error": "Invalid Command"}')

def show_image(window, imgpath):
    # do not create a new window
    # window = webview.create_window('', transparent=True, on_top=True, frameless=True, hidden=False)
    import time
    time.sleep(0.1)
    window.load_html(f'<img src="{imgpath}" alt=""/>')

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
    stream = StringIO()
    with redirect_stdout(stream):
        window.load_html(htmlcode)

if __name__ == '__main__':

    fileHandler = logging.FileHandler("popupview.log")
    logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
    fileHandler.setFormatter(logFormatter)
    rootlogger = logging.getLogger()
    rootlogger.addHandler(fileHandler)
    rootlogger.setLevel(logging.INFO)
    # consoleHandler = logging.StreamHandler()
    # consoleHandler.setFormatter(logFormatter)
    # rootlogger.addHandler(consoleHandler)

    print('{{"token": "{0}"}}'.format(webview.token))

    window = webview.create_window('', transparent=True, on_top=True, frameless=True, hidden=True)
    # show image
    # webview.start(show_image, [dummywindow, '/home/sifi/sandbox/popup_webview/Tux.jpg'], gui='qt')

    # show youtube
    # webview.start(show_youtube, [window, 'https://www.youtube.com/watch?v=be_XkA6pEQc'], gui='qt')

    # run server
    webview.start(stdinout_server, window, gui='qt')
