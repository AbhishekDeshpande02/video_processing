from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate
import cv2
import numpy as np
from django.http import StreamingHttpResponse
from django.views.decorators import gzip
from django.contrib.auth.decorators import login_required
from .models import videoSettings, User_Credentials
from django.contrib import messages


# Create your views here.
from django.shortcuts import render, redirect
from django.contrib import messages

def login(request):
  if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass')
        user= authenticate(request,username = username,password =pass1)
        if user is not None :
         
           return redirect('video_edit')
        else:
           return HttpResponse("Username and Password is incorrect")
  return render(request,'login.html')

def processor(request):
    return render(request,'video_edit.html')
@login_required
def video_edit(request):
    user = request.user
    video_settings = videoSettings.objects.get_or_create(user=user)[0]
    if request.method == 'POST':
        # Handle form submission for editing video settings
        color = request.POST.get('color', 'default_color')
        fps = int(request.POST.get('fps', 30))  # Read FPS value from form

        # Retrieve the logged-in user's username
        uname = user.username

        # Define video paths for each user
        user_video_paths = {
            'user1': 'C:/Users/Abhishek/Desktop/assessment/videoprocessor/user1_video.mp4',
            'user2': 'C:/Users/Abhishek/Desktop/assessment/videoprocessor/user2_video.mp4',
        }

        # Check if the user has a specific video path assigned
        video_path = user_video_paths.get(uname)

        print(f"Username: {uname}")  # Debug print
        print(f"Video path: {video_path}")  # Debug print

        if video_path is not None:
            cap = cv2.VideoCapture(video_path)

            # Edit video color
            def apply_color_effect(frame):
                if color == 'red':
                    return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                elif color == 'blue':
                    return cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                elif color == 'green':
                    return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Corrected to use BGR2GRAY for green
                else:
                    return frame

            # Edit video FPS
            frame_rate = cap.get(cv2.CAP_PROP_FPS)  # Get original frame rate
            scale_factor = frame_rate / fps  # Calculate scale factor based on desired FPS

            # Process and save the edited video
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter('edited_video.mp4', fourcc, fps, (int(cap.get(3)), int(cap.get(4))))
            while cap.isOpened():
                ret, frame = cap.read()
                if ret:
                    frame = apply_color_effect(frame)
                    out.write(frame)
                    # Adjust frame rate if needed
                    for _ in range(int(scale_factor) - 1):
                        out.write(frame)
                else:
                    break
            cap.release()
            out.release()

        # Redirect to video streaming page
        return redirect('video_stream')

    return render(request, 'video_edit.html', {'video_settings': video_settings})



@gzip.gzip_page
def video_stream(request):
    def stream():
        video_path = "edited_video.mp4"  # Path to the edited video file
        cap = cv2.VideoCapture(video_path)
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frame = cv2.imencode('.jpg', frame)[1].tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        cap.release()

    return StreamingHttpResponse(stream(), content_type='multipart/x-mixed-replace; boundary=frame')