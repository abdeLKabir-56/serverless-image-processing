import boto3
from PIL import Image
import os
import io

s3 = boto3.client('s3')

def lambda_handler(event, context):
    # 1. Lire les infos de l'événement S3
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    object_key = event['Records'][0]['s3']['object']['key']

    print(f"New image uploaded: {object_key} in bucket {bucket_name}")

    # 2. Télécharger le fichier dans /tmp (max 512MB disponible)
    download_path = f"/tmp/{object_key}"
    upload_key = f"processed-{object_key}"

    s3.download_file(bucket_name, object_key, download_path)

    # 3. Traitement de l'image
    img = Image.open(download_path)

    # — Resize à 800x800 max —
    img.thumbnail((800, 800))

    # — Convertir l'image dans un buffer mémoire —
    buffer = io.BytesIO()
    img.save(buffer, "JPEG")
    buffer.seek(0)

    # 4. Upload vers le bucket output
    output_bucket = "image-output-votre-nom"
    s3.upload_fileobj(buffer, output_bucket, upload_key)

    print(f"Processed image uploaded to {output_bucket}/{upload_key}")

    return {
        "status": "OK",
        "processed_file": upload_key
    }
