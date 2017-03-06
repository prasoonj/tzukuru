###############################################################
# Face Recognition based access control system - Driver file  #
# author: snortingcode.com                                    #
# date: 4th March, 2017                                       #
###############################################################

import numpy
import  cv2
import sys, time, os

from aws_utils import match_against_known_faces, get_face_from_collection

cap = cv2.VideoCapture(0)

#For face detection
cascade_path = sys.argv[1]
faceCascade = cv2.CascadeClassifier(cascade_path)

count = 0

while(True):

    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #Detecting faces
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(100,100),
        flags=cv2.cv.CV_HAAR_SCALE_IMAGE
    )

    print "Found {0} faces!".format(len(faces))

    #Draw rectagles around the face
    for index, (x, y, w, h) in enumerate(faces):
        print (x, y ,w, h)
        cv2.rectangle(gray, (x, y), (x+w, y+h), (0, 225, 0), 2)
        cv2.imwrite('tempimages/detected-face.png', gray)
        cv2.imshow('Testing Face Recognition', gray)

        #Display the captured frame
        # cv2.imshow('frame', gray)
        emp_name, emp_id = match_against_known_faces(faces[index], 'tempimages/detected-face.png')
        if emp_id == 0:
            print('Unregistered face!')
            #TODO: Store these in a database to document unauthorized entry attempts.
            os.system("say '%s'" % emp_name)
        else:
          print('Welcome %s: %s' % (emp_name, emp_id))
          os.system("say 'Welcome %s: %s'" % (emp_name, emp_id))
        cv2.imshow(emp_name, gray)

    count += 1

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()

