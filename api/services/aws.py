import boto3
import os
from dotenv import load_dotenv
import io
from PIL import Image



load_dotenv()

settings = {
    "AWS_SERVER_PUBLIC_KEY": os.getenv("C_AWS_ACCESS_KEY"),
    "AWS_SERVER_SECRET_KEY": os.getenv("C_AWS_SECRET_KEY")
}

def refresh_session():
    global boto4
    boto4 = boto3.Session(
        aws_access_key_id=settings["AWS_SERVER_PUBLIC_KEY"],
        aws_secret_access_key=settings["AWS_SERVER_SECRET_KEY"],
    )
def upload(series):
    refresh_session()
    s3 = boto4.resource('s3') 
    for item in series:
        print(item["file"],item["name"])
        
        object = s3.Object('uca.student-faces','index/'+ item["file"].name   )
        ret = object.put(Body=item["file"],
                            Metadata={'FullName': item["name"]}
                        )

def match(file):
    refresh_session()

    rekognition = boto4.client('rekognition', region_name='us-east-1')
    dynamodb = boto4.client('dynamodb', region_name='us-east-1')

    image = Image.open(file)
    stream = io.BytesIO()
    image.save(stream,format="JPEG")
    image_binary = stream.getvalue()


    response = rekognition.search_faces_by_image(
            CollectionId='faces',
            Image={'Bytes':image_binary}                                       
            )

    found = False
    for match in response['FaceMatches']:
        print (match['Face']['FaceId'],match['Face']['Confidence'])

        face = dynamodb.get_item(
            TableName='uca_student_faces',  
            Key={'RekognitionId': {'S': match['Face']['FaceId']}}
            )

        if 'Item' in face:
            res = ("Found Person: ",face['Item']['FullName']['S'])
            found = True

    if not found:
        return ("Person cannot be recognized")
    else:
        return res