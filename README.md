# tzukuru
Face recognition based access control system
## Running the code
1. Set up your environment for development - openCV for python built with ffmpeg is required.
2. Place some sample images in the face-directory.
3. Map the images in the face-directory with usernames, etc. in the file face-directory/face-directory.csv
4. Run the aws-utils.py scripts once to set up the face Collection in AWS Rekognition.
5. Run the tzukuru.py script to start the application - it takes one argument: path to the haar cascade classifier.

More details: http://snortingcode.tumblr.com/post/158067120425/weekend-hack-face-recognition-based-access
