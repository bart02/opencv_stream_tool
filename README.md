# opencv_stream_tool
The easiest stream tool for using on Autonomous Cars Competitions

## Usage
### Streamer
```python
import cv2
from send import Streamer

s = Streamer('localhost', 5555, 'slave')  # Init streamer

cap = cv2.VideoCapture(0)
while True:
    _, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Multi-window
    s.stream('color', frame)
    s.stream('gray', gray)

    cv2.waitKey(1)
```

### Viewer
```python
import cv2
from view import Viewer
from time import time

def f(window, frame):  # Callback function
    global windows
    vi = cv2.resize(frame, (400, 300))
    windows[window] = time()
    for e, t in windows.items():
        if time() - t > 1:
            cv2.destroyWindow(e)

    cv2.imshow(window, vi)
    cv2.waitKey(1)

windows = {}

v = Viewer(f, ip='localhost', port=5555, mode='master')
while True:
    pass
    # Do smth
```