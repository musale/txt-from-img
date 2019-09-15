import base64
import json
from pathlib import Path

from functions import txt_from_img


def test_main_requires_image():
    event = {}
    context = {}
    response = txt_from_img.main(event, context)
    body = response.get("body", None)
    statusCode = response.get("statusCode", None)
    assert "body" in response
    assert "statusCode" in response
    assert '{"error": "A base64 image string is required"}' in body
    assert statusCode == 400


def test_main_fails_base64_decode():
    event = {"body": '{"image64": "notBase64"}'}
    context = {}
    response = txt_from_img.main(event, context)
    body = response.get("body", None)
    statusCode = response.get("statusCode", None)
    assert "body" in response
    assert "statusCode" in response
    assert '"Incorrect base64 string: Incorrect padding"' in body
    assert statusCode == 400


def test_main_passes():
    event = {}
    context = {}
    image_path = Path("tests/data/img.png")
    assert image_path.exists() is True

    with image_path.open("rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
        image_64 = {"image64": encoded_string.decode()}
        event["body"] = json.dumps(image_64)
    response = txt_from_img.main(event, context)
    body = response.get("body", None)
    statusCode = response.get("statusCode", None)
    assert "body" in response
    assert "statusCode" in response
    assert statusCode == 200
    res = json.loads(body)
    text = res.get("text_in_image")
    assert text == "Tesseract OCR on AWS Lambda"
