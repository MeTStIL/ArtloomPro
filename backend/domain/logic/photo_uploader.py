import boto3
import uuid
import io
from datetime import datetime
from botocore.exceptions import NoCredentialsError, ClientError
from starlette.responses import JSONResponse
from fastapi import UploadFile, File, HTTPException
from backend.config import YC_STORAGE_ENDPOINT, YC_BUCKET_NAME
from backend.api_keys import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
from PIL import Image


def get_s3_client():
    session = boto3.session.Session()
    return session.client(
        service_name='s3',
        endpoint_url=YC_STORAGE_ENDPOINT,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )


def upload_photo_to_yc(file: UploadFile = File(...)):
    s3 = get_s3_client()

    try:
        unique_filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex}.jpg"

        image = Image.open(file.file)
        if image.mode in ("RGBA", "P"):
            image = image.convert("RGB")

        img_byte_arr = io.BytesIO()
        image.save(
            img_byte_arr,
            format="JPEG",
            quality=100,
        )
        img_byte_arr.seek(0)

        s3.upload_fileobj(
            img_byte_arr,
            YC_BUCKET_NAME,
            unique_filename,
            ExtraArgs={
                "ContentType": "image/jpeg",
                "ContentDisposition": "inline"
            }
        )

        return JSONResponse(
            status_code=200,
            content={
                "img_url": f"{YC_STORAGE_ENDPOINT}/{YC_BUCKET_NAME}/{unique_filename}"
            }
        )
    except NoCredentialsError:
        raise HTTPException(
            status_code=500,
            detail="AWS credentials not available"
        )
    except ClientError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Yandex Cloud Storage error: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error uploading file: {str(e)}"
        )


def delete_photo_from_yc(img_path):
    s3 = get_s3_client()
    filename = img_path.split('/')[-1]
    forDeletion = [{'Key': filename}]
    s3.delete_objects(Bucket=YC_BUCKET_NAME, Delete={'Objects': forDeletion})
