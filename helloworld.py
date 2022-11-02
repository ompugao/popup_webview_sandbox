#!/usr/bin/env python3
import webview

def display_screen_info():
    screens = webview.screens
    print('Available screens are: ' + str(screens))
htmlcode="""
<!DOCTYPE html>
<html>
  <body>
    <!-- 1. The <iframe> (and video player) will replace this <div> tag. -->
    <div id="player"></div>

    <script>
      // 2. This code loads the IFrame Player API code asynchronously.
      var tag = document.createElement('script');

      tag.src = "https://www.youtube.com/iframe_api";
      var firstScriptTag = document.getElementsByTagName('script')[0];
      firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

      // 3. This function creates an <iframe> (and YouTube player)
      //    after the API code downloads.
      var player;
      function onYouTubeIframeAPIReady() {
        player = new YT.Player('player', {
          height: '360',
          width: '640',
          videoId: 'M7lc1UVf-VE',
          events: {
            'onReady': onPlayerReady,
            'onStateChange': onPlayerStateChange
          }
        });
      }

      // 4. The API will call this function when the video player is ready.
      function onPlayerReady(event) {
        event.target.playVideo();
      }

      // 5. The API calls this function when the player's state changes.
      //    The function indicates that when playing a video (state=1),
      //    the player should play for six seconds and then stop.
      var done = false;
      function onPlayerStateChange(event) {
        if (event.data == YT.PlayerState.PLAYING && !done) {
          setTimeout(stopVideo, 6000);
          done = true;
        }
      }
      function stopVideo() {
        player.stopVideo();
      }
    </script>
  </body>
</html>
"""
csscode2 = """
.videoContainer {
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
}

iframe {
  /* optional */
  width: 100%;
  height: 100%; 
}
"""
htmlcode2 = """
<html><body>
<div class="videoContainer">
    <iframe class="videoContainer__video" width="1920" height="1080" src="http://www.youtube.com/embed/be_XkA6pEQc?modestbranding=1&autoplay=1&controls=1&fs=0&loop=1&rel=0&showinfo=0&disablekb=1" frameborder="0"></iframe>
</div>
</body></html>
"""


def load_css(window):
    window.load_css(csscode2)


def initial_hook(window):
    window.load_html('<img src="Tux.jpg" alt=""/>')
    from qtpy.QtCore import Qt
    view = window.gui.BrowserView.instances['master']
    view.setWindowFlag(Qt.WindowDoesNotAcceptFocus)
    window.show()
    # import time
    # window.hide()
    # time.sleep(3)
    # window.show()

# import sys, termios
# import subprocess
# subprocess.run("echo -e '\033[6n' ; read -sd R CURPOS ; echo ${CURPOS#*[}".split(' '))
# 
# def get_cursor_position():
#     print("\033[6n", end="", flush=True)
#     fd = sys.stdin.fileno()
#     oldterm = termios.tcgetattr(fd)
#     newattr = termios.tcgetattr(fd)
#     newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
#     termios.tcsetattr(fd, termios.TCSANOW, newattr)
#     try:
#         sys.stdin.read(2)
#         s = ""
#         while True:
#             c = sys.stdin.read(1)
#             if c == "R":
#                 break
#             s += c
#         print(tuple(map(int, s.split(";"))))
#     except IOError:
#         pass
#     finally:
#         termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
# print(get_cursor_position())

if __name__ == '__main__':
    # display_screen_info()
    # webview.create_window('Woah dude!', html='<h1>Woah dude!<h1>', frameless=True)
    # webview.create_window('title', 'https://www.youtube.com/watch?v=be_XkA6pEQc&v=ultrawide', frameless=True)
    # webview.create_window('title', html=htmlcode, frameless=True, width=640, height=360)
    # webview.start(display_screen_info)
    # window = webview.create_window('title', html=htmlcode2, frameless=True, transparent=True)
    # webview.start(load_css, window)

    window = webview.create_window('', frameless=True, transparent=True, hidden=True, on_top=True)
    webview.start(initial_hook, window, gui='qt')
