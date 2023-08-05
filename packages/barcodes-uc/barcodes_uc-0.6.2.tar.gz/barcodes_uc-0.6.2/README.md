# Barcodes python module

**Thanks to Melisa for her precious help.**

⚠️ This python package is still in development. ⚠️

* For now only QR codes are available. Only alphanumeric and byte encodings are available.

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

## Future work

- [ ] Add byte and numeric encoding to qr codes.

- [ ] Save qr code as image in different styles.

- [ ] Generate barcodes.