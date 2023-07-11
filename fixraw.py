import base64
import re
import boto3
from botocore.client import Config
import os

# VTEC-x
devices = ["MS-IPc049ef49fbbb", "MS-IPc049ef485aaf", "MS-IPc049ef49fb27", "MS-IPc049ef4a0943", "MS-IPc049ef49fb0b", "MS-IPc049ef4a0b0b", "MS-IPc049ef4a08ef", "MS-IPc049ef48674f", "MS-IPc049ef4a0aff", "MS-IP90380cf33fe3", "MS-IPc049ef4a0af7"]


class Bucket:
    def __init__(self):
        self.s3 = boto3.resource(
            's3',
            aws_access_key_id='AWS_ACCESS_KEY_ID',
            aws_secret_access_key='AWS_SECRET_ACCESS_KEY',
            config=Config(signature_version='s3v4')
        )
        self.bucket = self.s3.Bucket('people-count-webeasy')

    def download_filtered_files(self, prefix):
        # s3obj = None
        for obj in self.bucket.objects.filter(Prefix=prefix):
            print(obj.key.split("/")[0])
            for device in devices:
                # print(device)
                if device in obj.key:
                    self.download_file(obj)
                    # print(device)
                    # s3obj = obj
                    print("----", obj.key)
                    # break
            # if s3obj:
                # break
            # print(obj, obj.key)
        # print(s3obj)
        # if s3obj:
            # self.download_file(s3obj)

    def upload_fileobj(self, src_path, dest_path):
        try:
            with open(src_path, 'rb') as data:
                self.bucket.upload_fileobj(data, dest_path)
        except Exception as e:
            print('error in uploading fileobj ', str(e))
            return False
        else:
            return True

    def upload_file(self, src_path, dest_path):
        try:
            self.bucket.upload_file(src_path, dest_path)
        except Exception as e:
            print('error in uploading file ', str(e))
            return False
        else:
            return True

    def download_file(self, obj):
        if not os.path.exists(os.path.dirname(obj.key)):
            os.makedirs(os.path.dirname(obj.key))
        try:
            self.bucket.download_file(obj.key, obj.key)
        except Exception as e:
            print('error in deleting ', str(e))
            return False
        else:
            return True


def decode_base64(data, altchars=b'+/'):
    data = re.sub(rb'[^a-zA-Z0-9%s]+' % altchars, b'', data)  # normalize
    missing_padding = len(data) % 4
    if missing_padding:
        data += b'=' * (4 - missing_padding)
    return base64.b64decode(data, altchars)


def process_images():
    for folder in os.listdir():
        if os.path.isdir(folder):
            for file in os.listdir(folder):
                if file.endswith(".jpg"):
                    path = folder + "/" + file
                    print(path)
                    base64Image = None
                    try:
                        with open(path, "rb") as f:
                            data = f.read()
                            print(data)
                            base64Image = base64.b64encode(data).decode('utf-8')
                            base64Image = bytes(base64Image[1:], 'utf-8')

                        if base64Image:
                            with open(path, 'wb') as f:
                                image = decode_base64(base64Image)
                                f.write(image)
                    except Exception as e:
                        print(e)


def upload_images(bucket):
    for folder in os.listdir():
        if os.path.isdir(folder):
            for file in os.listdir(folder):
                path = folder + "/" + file
                if file.endswith(".jpg") and os.path.isfile(path):
                    print(path)
                    bucket.upload_file(path, path)
                    os.remove(path)
                # if len(os.listdir(folder)) == 0:
                #     os.rmdir(folder)


try:
    bucket = Bucket()
    # bucket.download_filtered_files("2023-07-10T10")
    # process_images()
    upload_images(bucket)
except Exception as e:
    print('Error ', str(e))

# "2023-06-1"
