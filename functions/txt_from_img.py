import io
import json
import logging
import binascii
import os
from base64 import b64decode

import PIL.Image
import pytesseract

LAMBDA_TASK_ROOT = os.environ.get(
    "LAMBDA_TASK_ROOT", os.path.dirname(os.path.abspath(__file__))
)
os.environ["PATH"] += os.pathsep + LAMBDA_TASK_ROOT

ALLOWED_METHODS = ["POST"]
LOG = logging.getLogger()
LOG.setLevel(logging.INFO)


def main(event, context):
    body = event.get("body", None)

    if body is None:
        err = "A base64 image string is required"
        LOG.error(err)
        return {"statusCode": 400, "body": json.dumps({"error": err})}

    image = json.loads(body)
    image_base64 = image.get("image64", None)
    try:
        binary = b64decode(image_base64)
        image = PIL.Image.open(io.BytesIO(binary))
        text = pytesseract.image_to_string(image, config="--psm 6")

        message = {"success": True, "text_in_image": text}
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(message),
        }
    except binascii.Error as wrong_base64:
        LOG.error(wrong_base64)
        message = "Incorrect base64 string: {}".format(wrong_base64)
        return {
            "statusCode": 400,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(message),
        }
    except Exception as failed_extract:
        LOG.error(failed_extract)
        message = "Failed to get text: {}".format(failed_extract)
        return {
            "statusCode": 400,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(message),
        }
