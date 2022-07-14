'''
In sintesi:
all'indirizzo: 127.0.0.1:5000
visualizzo il debugger
e aprendo in un browser index.html
vedo il video! 

Video_Streaming_in_Web_Browsers_with_OpenCV_e_Flask.py

Video Streaming in Web Browsers with OpenCV & Flask
Step1- Install Flask & OpenCV :
You can use the ‘pip install flask’ and ‘pip install opencv-python’ command. I use the PyCharm IDE to develop flask applications.
 To easily install libraries in PyCharm follow these steps: 
 https://www.jetbrains.com/help/pycharm/installing-uninstalling-and-upgrading-packages.html#packages-tool-window
 
 
 Step2- Import necessary libraries, initialize the flask app :
We will now import the necessary libraries and initialize our flask app.


Step3- Capture Video using OpenCV :
Create a VideoCapture() object to trigger the camera and read the first image/frame of the video. We can either provide the path of the video file or use numbers to specify the use of local webcam. To trigger the webcam we pass ‘0’ as the argument. To capture the live feed from an IP Camera we provide the RTSP link as the argument. To know the RTSP address for your IP Camera go through this — Finding RTSP addresses.

Step4- Adding window and generating frames from the camera:

The gen_frames() function enters a loop where it continuously returns frames from the camera as response chunks. 
The function asks the camera to provide a frame then it yields with this frame formatted as a response chunk 
with a content type of image/jpeg, as shown above. The code is shown below :


Step5- Define app route for default page of the web-app :

Routes refer to URL patterns of an app (such as myapp.com/home or myapp.com/about). @app.route("/") is a Python decorator 
that Flask provides to assign URLs in our app to functions easily.

@app.route('/')
def index():
    return render_template('index.html')

The decorator is telling our @app that whenever a user visits our app domain (localhost:5000 for local servers) at the given .route(), 
execute the index() function. 
Flask uses the Jinja template library to render templates. In our application, 
we will use templates to render HTML which will display in the browser.

Step6- Define app route for the Video feed:
@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
The ‘/video_feed’ route returns the streaming response. Because this stream returns the images that are to be displayed in the web page, the URL to this route is in the “src” attribute of the image tag (see ‘index.html’ below). The browser will automatically keep the image element updated by displaying the stream of JPEG images in it, since multipart responses are supported in most/all browsers

Let’s have a look at our index.html file :

<body>
<div class="container">
    <div class="row">
        <div class="col-lg-8  offset-lg-2">
            <h3 class="mt-5">Live Streaming</h3>
            <img src="{{ url_for('video_feed') }}" width="100%">
        </div>
    </div>
</div>
</body>

Step7- Starting the Flask Server :

if __name__ == "__main__":
    app.run(debug=True)
app.run() is called and the web-application is hosted locally on [localhost:5000].

“debug=True” makes sure that we don’t require to run our app every time we makes changes, we can simply refresh our web page to see the changes while the server is still running.

In sintesi:
all'indirizzo: 127.0.0.1:5000
visualizzo il debugger
e aprendo in un browser index.html
vedo il video! 
'''

#Import necessary libraries
from flask import Flask, render_template, Response
import cv2
#Initialize the Flask app
app = Flask(__name__)

# Step3- Capture Video using OpenCV :

# camera = cv2.VideoCapture(0) # Funziona. Vede la mia webcam.
username = 'admin'
password = 'a211256ntimo'
user = username_password = password
#my IP camera: 192.168.1.129

#camera =  cv2.VideoCapture('rtsp://admin:a211256ntimo@192.168.1.129/H264?ch=1&subtype=0') # 1  H264?ch=1&subtype=0 # Non Funziona!!! 
camera =  cv2.VideoCapture('http://admin:a211256ntimo@192.168.1.129/video.cgi?.mjpg') # 1  H264?ch=1&subtype=0
#- rtsp://username:password@ip_address:554/user=username_password='password'_channel=channel_number_stream=0.sdp'
#http://admin:a211256ntimo@192.168.1.129/video.cgi?.mjpg
'''
for ip camera use - rtsp://username:password@ip_address:554/user=username_password='password'_channel=channel_number_stream=0.sdp' 
for local webcam use cv2.VideoCapture(0)
'''

# Step4- Adding window and generating frames from the camera:

def gen_frames():  
    while True:
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result

# Step5- Define app route for default page of the web-app :

@app.route('/')
def index():
    return render_template('index.html')

'''
The decorator is telling our @app that whenever a user visits our app domain 

(localhost:5000 for local servers) 

at the given .route(), execute the index() function. 
Flask uses the Jinja template library to render templates. 
In our application, we will use templates to render HTML which will display 
in the browser.
'''
# Step6- Define app route for the Video feed:

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
    
'''
The ‘/video_feed’ route returns the streaming response. 
Because this stream returns the images that are to be displayed in the web page, 
the URL to this route is in the “src” attribute of the image tag (see ‘index.html’ below). 
The browser will automatically keep the image element updated by displaying the stream of JPEG images in it, 
since multipart responses are supported in most/all browsers

Let’s have a look at our index.html file :
'''
'''
<body>
<div class="container">
    <div class="row">
        <div class="col-lg-8  offset-lg-2">
            <h3 class="mt-5">Live Streaming</h3>
            <img src="{{ url_for('video_feed') }}" width="100%">
        </div>
    </div>
</div>
</body>
'''
# Step7- Starting the Flask Server :

if __name__ == "__main__":
    app.run(debug=True)   
    
'''
app.run() is called and the web-application is hosted locally on [localhost:5000].

“debug=True” makes sure that we don’t require to run our app every time we makes changes, 
we can simply refresh our web page to see the changes while the server is still running.
'''     
