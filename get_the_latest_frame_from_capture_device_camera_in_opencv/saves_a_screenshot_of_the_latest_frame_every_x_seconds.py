'''
Here's a widget which saves a screenshot of the latest frame every x seconds. This idea is to create another thread just for obtaining the frames as cv2.VideoCapture.read() is a blocking operation. By putting this operation into a separate dedicated thread that focuses only on grabbing frames, we can ensure that we have the latest frame without any buffer. This will improve performance by I/O latency reduction as the main thread does not have to wait until there is a new frame. I used my own RTSP stream link and saved a screenshot every 1 second. Change it to your RTSP link and however long you want to save a screenshot

Ecco un widget che salva uno screenshot dell'ultimo frame ogni x secondi. 
L'idea è creare un altro thread solo per ottenere i frame poiché 
cv2.VideoCapture.read() è un'operazione bloccante. 
Inserendo questa operazione in un thread dedicato separato che si concentra solo sull'acquisizione dei frame, 
possiamo assicurarci di avere il frame più recente senza alcun buffer. 
Ciò migliorerà le prestazioni riducendo la latenza di I/O poiché il thread 
principale non deve attendere fino a quando non è presente un nuovo frame. 
Ho usato il mio link di streaming RTSP e ho salvato uno screenshot ogni 1 secondo. 
Cambialo nel tuo collegamento RTSP e per quanto tempo desideri salvare uno screenshot

'''
# saves a screenshot of the latest frame every x seconds
# saves_a_screenshot_of_the_latest_frame_every_x_seconds.py
from threading import Thread
import cv2
import time

src = 0 # 'rtsp://admin:a211256ntimo@192.168.1.129'
# http://192.168.1.129:80/admin a211256ntimo
# http://admin:a211256ntimo@192.168.1.129/video.cgi?.mjpg   # Funziona in qualsiasi browser!!!

class VideoScreenshot(object):
    def __init__(self, src=0):
        # Create a VideoCapture object
        # self.capture = cv2.VideoCapture(src) #con src = 0 non funziona
        #self.capture = cv2.VideoCapture(0) # Funziona!!! Ma vede la mia webcam.
        self.capture = cv2.VideoCapture('http://admin:a211256ntimo@192.168.1.129/video.cgi?.mjpg') # Funziona!!!


        # Take screenshot every x seconds
        self.screenshot_interval = 1

        # Default resolutions of the frame are obtained (system dependent)
        self.frame_width = int(self.capture.get(3))
        self.frame_height = int(self.capture.get(4))

        # Start the thread to read frames from the video stream
        self.thread = Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()

    def update(self):
        # Read the next frame from the stream in a different thread
        while True:
            if self.capture.isOpened():
                (self.status, self.frame) = self.capture.read()

    def show_frame(self):
        # Display frames in main program
        if self.status:
            cv2.imshow('frame', self.frame)

        # Press Q on keyboard to stop recording
        key = cv2.waitKey(1)
        if key == ord('q'):
            self.capture.release()
            cv2.destroyAllWindows()
            exit(1)

    def save_frame(self):
        # Save obtained frame periodically
        self.frame_count = 0
        def save_frame_thread():
            while True:
                try:
                    cv2.imwrite('frame_{}.png'.format(self.frame_count), self.frame)
                    self.frame_count += 1
                    time.sleep(self.screenshot_interval)
                except AttributeError:
                    pass
        Thread(target=save_frame_thread, args=()).start()

if __name__ == '__main__':
    rtsp_stream_link = 'your stream link!'
    video_stream_widget = VideoScreenshot(rtsp_stream_link)
    video_stream_widget.save_frame()
    while True:
        try:
            video_stream_widget.show_frame()
        except AttributeError:
            pass
