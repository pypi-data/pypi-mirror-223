# Barcodes python module

**Thanks to Melisa for her precious help.**

⚠️ This python package is still in development. ⚠️

* For now only QR codes are available. Only alphanumeric and byte encodings are available.
* It looks like qr codes encoding a URL sometimes do not work unless you add a "/" at the end.

## OpenAPI

I used this package to learn how to use the fastapi package. The API that I created is available at [https://qrgeneratorapi-1-c9139268.deta.app](https://qrgeneratorapi-1-c9139268.deta.app).

* Use it to generate QR codes by sending GET requests to the API.
* For now the API can return the QR code data or the QR code image encoded in base64.
* Example usage:

  * ```python
    import requests
    from PIL import Image
    import base64

    url = 'https://qrgeneratorapi-1-c9139268.deta.app/qrimg/test'

    #get json
    r = requests.get(url)

    jsonData = r.json() #Get the json answer from the API
    size = jsonData["img"]["size"]
    base64Data = jsonData["img"]["base64"]
    imgdecoded = Image.frombytes('L', (size, size), base64.b64decode(base64Data)) #Decode the image

    imgdecoded.show() #Show the image 
    ```

## Installation

```bash
pip install barcodes-uc
```

You might want to install the package in a virtual environment. For that do:

```bash
python3 -m venv venv
source venv/bin/activate
pip install barcodes-uc
```

## Usage

```python
from barcodes_uc.qrcodes import qrgenerator, qrutils

# Generate a QR code
message = "Hello world!"
encoding = qrutils.QREncoding.byte
version, error_correction_level, qr = qrgenerator.get_min_version(message, encoding, qrutils.QRErrorCorrectionLevels.Q)
generator = qrgenerator.QRGenerator(msg=message, encoding=encoding, version=version, error_correction=error_correction_level)
qr = generator.generate()

qr.show() # Show the QR code in the terminal
qr.save("qr.png", imgSize = 1000, colour=[qrgenerator.QRColour.red]) # Save the QR code in a file
```

## CLI tools

The package comes with CLI tools:

### QR code generator

```bash
qrcode --help
```

```bash
usage: qrcode [-h] [-e {byte,numeric,alphanumeric,kanji}] [-V QR_VERSION] [-E {L,M,Q,H}] [--save SAVE] [--no-show] message

Create QR codes

positional arguments:
  message               Message to encode

optional arguments:
  -h, --help            show this help message and exit
  -e {byte,numeric,alphanumeric,kanji}, --encoding {byte,numeric,alphanumeric,kanji}
                        Encoding of the message
  -V QR_VERSION, --qr-version QR_VERSION
                        QR version, 1-40
  -E {L,M,Q,H}, --qr-error-correction {L,M,Q,H}
                        QR error correction
  --save SAVE           Save the QR code to a .png file, do not add the file format
  --no-show             Do not show the QR code
  
Made by Pedro Juan Royo, @UnstrayCato
```

The program will show the QR code in the terminal and save it to a file if the `--save` option is used.
If **no -e, -V or -E options are used, the program will try to guess the best options for the message.**

## Future work

- [x] Add byte and numeric encoding to qr codes.

- [ ] Save qr code as image in different styles.

- [ ] Generate barcodes.