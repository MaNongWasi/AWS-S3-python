import boto3
from botocore.client import Config


class Bucket:
    def __init__(self, data, file, file_des):
	self.bucket_name = 'BUCKET NAME'
	self.s3 = boto3.resource(
	    's3',
    	    aws_access_key_id='ACCESS KEY ID',
    	    aws_secret_access_key='ACCESS KEY',
            config=Config(signature_version='s3v4')
    	)
	self.file = file
	self.file_des = file_des
	self.data = data

    def upload(self):
	try:
	    self.s3.Bucket(self.bucket_name).put_object(Key=self.file, Body=data, ACL='public-read')
	except Exception as e:
	    print 'error in uploading ', str(e)
	    return False
	else:
	    return True

    def upload_file(self):
	try:
	    with open('test.png', 'rb') as data:
    		self.s3.Bucket(self.bucket_name).upload_fileobj(data, self.file)
	except Exception as e:
            print 'error in deleting ', str(e)
            return False
        else:
            return True

    def download(self):
	try:
	    with open(self.file_des, 'wb') as data:
    		self.s3.Bucket(self.bucket_name).download_fileobj(self.file, data)
	except Exception as e:
            print 'error in uploading ', str(e)
            return False
        else:
            return True


    def delete(self):
	try:
	    self.s3.Bucket(self.bucket_name).delete_objects(Delete={'Objects':[{'Key':self.file},]})
	except Exception as e:
            print 'error in deleting ', str(e)
            return False
        else:
            return True

    def download_file(self):
	try:
	    self.s3.Bucket(self.bucket_name).download_file(self.file, self.file_des)
	except Exception as e:
            print 'error in deleting ', str(e)
            return False
        else:
            return True


if __name__ == "__main__":

    FILE_NAME = '2017/test.png'
    data = open('bitmoji.png', 'rb')
    file_save = 'test.png'

    try:
        bucket = Bucket(data, FILE_NAME, file_save)
#        print(bucket.upload())
#	print bucket.download_file()
#	print (bucket.download())
#	print(bucket.delete())
	print (bucket.upload_file())
    except Exception as e:
        print ('Error ', str(e))
