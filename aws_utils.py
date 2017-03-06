#########################################
# Amazon Web Service related functions  #
# author: snortingcode.com              #
# date: 4th March, 2017                 #
#########################################

import time
from os import listdir
from os.path import isfile, join
import csv, json

import boto3

COLLECTION_ID = 'snortingcode-face-collection'
FACES_DIR = 'face-directory/face-directory.csv'
FACES_MATCH_DB_FILE = 'face-directory/face-matches'

session = boto3.Session(profile_name='TEK-PRAVEEN')
client = session.client('rekognition')

def create_rekognition_collection(collection_id):
    return client.create_collection(CollectionId=collection_id)

def delete_rekognition_collection(collection_id):
    return client.delete_collection(CollectionId=collection_id)

def readimage(image):
    with open(image, 'r') as f:
        return f.read()

def add_face_to_collection(collection_id, faces_directory, file_name):
    facepath = faces_directory + '/' + file_name
    response = client.index_faces(
        CollectionId=collection_id,
        Image={
            'Bytes':readimage(facepath)
        },
        ExternalImageId=file_name)
    return response

def add_faces_directory_to_collection(collection_id, face_directory):
    top_level_directory_path = ''.join(face_directory.split('/')[0:-1])
    face_match_directory = open('%s/face-matches' % top_level_directory_path, 'w')

    with open(face_directory, 'rb') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in csvreader:
            response = add_face_to_collection(collection_id, top_level_directory_path, row[1])
            response['empId'] = row[0]
            response['empName'] = row[2]
            print response
            json.dump(response, face_match_directory)
            face_match_directory.write('\n')



def match_against_known_faces(faceimage, image_path):

    #Get confidence score from AWS Rekognition
    response = client.search_faces_by_image(
        CollectionId=COLLECTION_ID,
        Image={
            'Bytes': readimage(image_path)
        },
        MaxFaces=5,
        FaceMatchThreshold=50)
    response = json.dumps(response)
    print response
    with open(FACES_MATCH_DB_FILE, 'r') as face_match_file:
        for row in face_match_file:
            row_json = json.loads(row)
            input_image_id = row_json['FaceRecords'][0]['Face']['ImageId']
            emp_name = row_json['empName']
            emp_id = row_json['empId']

            response_json = json.loads(response)
            if len(response_json['FaceMatches']) == 0:
                return ('Sorry, your face needs registration!', 0)
            print('Input image id: %s' % input_image_id)
            print('Matched image id:  %s' % response_json['FaceMatches'][0]['Face']['ImageId'])
            if input_image_id == response_json['FaceMatches'][0]['Face']['ImageId']:
                return (emp_name, emp_id)

def get_face_from_collection(faceid):
    return client.search_faces(
        CollectionId=COLLECTION_ID,
        FaceId=faceid,
        MaxFaces=1,
        FaceMatchThreshold=50)
def main():
    #Create a collection for known faces
    delete_rekognition_collection(COLLECTION_ID)
    create_rekognition_collection(COLLECTION_ID)
    add_faces_directory_to_collection(COLLECTION_ID, FACES_DIR)

if __name__ == '__main__':
    main()
