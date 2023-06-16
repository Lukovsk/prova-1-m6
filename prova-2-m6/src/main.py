import cv2

face_cascade = cv2.CascadeClassifier(
    filename=f"{cv2.data.haarcascades}/haarcascade_frontalface_alt2.xml"
)

input_video = cv2.VideoCapture('./arsene.mp4')

if not input_video.isOpened():
    print('Error opening video stream or file')
    exit(1)
    
width = int(input_video.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(input_video.get(cv2.CAP_PROP_FRAME_HEIGHT))

output_video = cv2.VideoWriter('./saida/out.avi', cv2.VideoWriter_fourcc(*'DIVX'), 24, (width, height))

while True:
    ret, frame = input_video.read()
    
    if not ret:
        break
    
    faces = face_cascade.detectMultiScale(
        image=frame,
        scaleFactor=1.94,
        minNeighbors=3)
    
    for (x,y,w,h) in faces:
        print(x,y,w,h)

        cv2.rectangle(
            img=frame,
            pt1=(x, y),
            pt2=(x+w, y+h),
            color=(0,0,255),
            thickness=3
        )
    
    cv2.imshow('Video Playback', frame)
    
    output_video.write(frame)
    
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break
    
output_video.release()
input_video.release()
cv2.destroyAllWindows()