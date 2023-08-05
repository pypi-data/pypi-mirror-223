# CLI for creating QR codes

#imports
import argparse
from . import qrgenerator, qrutils

class TerminalColors:
    """Class for terminal colors"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    INFO = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

def main():
    # Create the parser
    parser = argparse.ArgumentParser(description='Create QR codes', prog='qrcode', epilog='Made by Pedro Juan Royo, @UnstrayCato')

    # Add the arguments
    parser.add_argument('message', metavar='message', type=str, help='Message to encode')
    parser.add_argument('-e', '--encoding', type=str, help='Encoding of the message', choices=['byte', 'numeric', 'alphanumeric', 'kanji'])
    parser.add_argument('-V', '--qr-version', type=int, help='QR version, 1-40')
    parser.add_argument('-E', '--qr-error-correction', help='QR error correction', choices=['L', 'M', 'Q', 'H'])
    parser.add_argument('--save', help='Save the QR code to a file', type=str)

    # Execute the parse_args() method
    args = parser.parse_args()
    
    if args.encoding:
        encoding = qrutils.QREncoding[args.encoding]
    else:
        encoding = qrgenerator.get_encoding(args.message)
        print('Encoding detected: ' + TerminalColors.OKGREEN + f'{encoding.name}' + TerminalColors.ENDC)

    if args.qr_version and args.qr_error_correction:
        version = qrutils.QRVersion[args.qr_version]
        error_correction = qrutils.QRErrorCorrectionLevels[args.qr_error_correction]
        generator = qrgenerator.QRGenerator(args.message, encoding, version, error_correction)
    else:
        version, error_correction = qrgenerator.get_min_version(args.message, encoding, qrutils.QRErrorCorrectionLevels.Q)
        generator = qrgenerator.QRGenerator(args.message, encoding, version, error_correction)

    qr = generator.generate()
    qr.show()

    if args.save:
        qr.save(f'{args.save}.png')

if __name__ == '__main__':
    main()