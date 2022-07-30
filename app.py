from dotenv import load_dotenv
from botocore import client
from flask import (
    Flask,
    render_template,
    request,
)
import boto3
import uuid
import os

load_dotenv()

app = Flask(__name__)
s3 = boto3.client('s3',
                  aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
                  aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
                  region_name=os.environ['REGION_NAME'],
                  endpoint_url=os.environ['S3_ENDPOINT'],
                  config=client.Config(signature_version='s3v4'),
                  )

key = 'users/uploads/${filename}'
bucket = os.environ['BUCKET_NAME']
conditions = [
    {"acl": "public-read"},
    ["starts-with", "$key", "users/uploads"],
    {'success_action_redirect': os.environ['SUCCESS_ACTION_REDIRECT_URL']},
    ["content-length-range", 0, 31457280]
]
fields = {'success_action_redirect': os.environ['SUCCESS_ACTION_REDIRECT_URL']}


def get_form(form_fields):
    form = """
    <form action="{url}" method="post" enctype="multipart/form-data">
            <input type="hidden"    name="key" value="{fields[key]}" /><br />
            <input type="hidden"   name="x-amz-credential" value="{fields[x-amz-credential]}" />
            <input type="hidden"   name="acl" value="public-read" />
            <input type="hidden"   name="x-amz-algorithm" value="{fields[x-amz-algorithm]}" />
            <input type="hidden"   name="x-amz-date" value="{fields[x-amz-date]}" />
            <input type="hidden"   name="success_action_redirect" value="{fields[success_action_redirect]}" />
            <input type="hidden"   name="policy" value="{fields[policy]}" />
            <input type="hidden" name="x-amz-signature" value="{fields[x-amz-signature]}" />
            <label for="file">File to upload:</label>
            <input type="file"   name="file" /> <br />
            <input type="submit" name="submit" value="Upload" />
        </form>
    """
    return form.format(**form_fields)


def get_filename():
    return f'users/uploads/{uuid.uuid4()}.jpg'


@app.route('/')
def get_data():
    prepared_form_fields = s3.generate_presigned_post(Bucket=bucket,
                                                      Key=get_filename(),
                                                      Conditions=conditions,
                                                      Fields=fields,
                                                      ExpiresIn=60 * 60)
    return render_template('s3-form.html', form=get_form(prepared_form_fields),)


@app.route('/success')
def show_uploaded_file():
    return render_template(
        'show-uploaded-file.html',
        bucket=request.args.get('bucket'),
        file_name=request.args.get('key'),
    )


if __name__ == '__main__':
    app.run()
