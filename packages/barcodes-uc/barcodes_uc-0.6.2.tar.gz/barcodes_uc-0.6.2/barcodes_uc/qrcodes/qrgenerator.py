
#imports
from . import qrutils
from PIL import Image
import numpy as np
from enum import Enum
# from aenum import extend_enum, Enum

finderPattern = [
    [1,1,1,1,1,1,1],
    [1,0,0,0,0,0,1],
    [1,0,1,1,1,0,1],
    [1,0,1,1,1,0,1],
    [1,0,1,1,1,0,1],
    [1,0,0,0,0,0,1],
    [1,1,1,1,1,1,1]
]

alignmentPattern = [
    [1,1,1,1,1],
    [1,0,0,0,1],
    [1,0,1,0,1],
    [1,0,0,0,1],
    [1,1,1,1,1]
]

#White and black background colors
class ModuleColors:
    WHITE = '\x1b[0;37;47m'
    BLACK = '\x1b[0;30;40m'
    RESET = '\x1b[0m'

class NewColour:
    def __init__(self, name, rgb: list[float]) -> None:
        if len(rgb) != 3:
            raise ValueError("RGB list must have 3 values")
        for i in rgb:
            if i < 0 or i > 1:
                raise ValueError("RGB values must be in range [0-1]")
        
        self.value = rgb
        self.name = name

#Colour class to save qr code as an image with colour
class QRColour(Enum):
    black = [0, 0, 0]
    red = [1, 0, 0]
    green = [0, 1, 0]
    blue = [0, 0, 1]
    yellow = [1, 1, 0]
    cyan = [0, 1, 1]
    magenta = [1, 0, 1]
    white = [1, 1, 1]

    @classmethod
    def new_colour(cls, name, rgb: list[float]):
        if len(rgb) != 3:
            raise ValueError("RGB list must have 3 values")
        for i in rgb:
            if i < 0 or i > 1:
                raise ValueError("RGB values must be in range [0-1]")
        
        return NewColour(name, rgb)

class QR:
    def __init__(self, encoding: qrutils.QREncoding, message: str, error_correction: qrutils.QRErrorCorrectionLevels, version: qrutils.QRVersion = qrutils.QRVersion.v1) -> None:
        self.size = qrutils.qr_size(version)
        self.version = version
        self.encoding = encoding
        self.message = message
        self.error_correction = error_correction
        self.matrix = [['X' for i in range(self.size)] for j in range(self.size)]
        self.reserved_positions = [[0 for i in range(self.size)] for j in range(self.size)]

    # def set_size(self, size: int):
    #     self.size = size
    #     self.matrix = [[0 for i in range(size)] for j in range(size)]

    def __str__(self): #TODO: Make this look better
        buildString = ""
        for row in self.matrix:
            for col in row:
                buildString += str(col)
            buildString += "\n"

        return buildString
    
    def show(self):
        #Add quiet zone
        for _ in range(4):
            for _ in range(self.size + 8):
                print(ModuleColors.WHITE + ' ' + ModuleColors.RESET, end="")
            print()

        for row in self.matrix:
            for _ in range(4):
                print(ModuleColors.WHITE + ' ' + ModuleColors.RESET, end="")

            for col in row:
                if col == 0:
                    print(ModuleColors.WHITE + ' ' + ModuleColors.RESET, end="")
                else:
                    print(ModuleColors.BLACK + ' ' + ModuleColors.RESET, end="")

            for _ in range(4):
                print(ModuleColors.WHITE + ' ' + ModuleColors.RESET, end="")
            print()
    
        for _ in range(4):
            for _ in range(self.size + 8):
                print(ModuleColors.WHITE + ' ' + ModuleColors.RESET, end="")
            print()

    #Function to save the QR code as a png image
    def save(self, filename: str = "qr.png", imgSize: int = 300, quietZone: bool = True, quietZoneSize: int = 4, 
    colour: list[QRColour] = [QRColour.black], bckgrndColour: QRColour = QRColour.white):
        #Add quiet zone
        if quietZone:
            img_pixels = [[[1 for _ in range(3)] for _ in range(self.size + quietZoneSize*2)] for _ in range(self.size + quietZoneSize*2)]
            # print(len(img_pixels), len(img_pixels[0]), len(img_pixels[0][0]))
            for i in range(self.size):
                for j in range(self.size):
                    for k in range(3):
                        img_pixels[i+quietZoneSize][j+quietZoneSize][k] = 0 if self.matrix[i][j] == 1 else 1
        else:
            img_pixels = [[[1 for _ in range(3)] for _ in range(self.size + quietZoneSize*2)] for _ in range(self.size + quietZoneSize*2)]
            for i in range(self.size):
                for j in range(self.size):
                    for k in range(3):
                        img_pixels[i+quietZoneSize][j+quietZoneSize][k] = 0 if self.matrix[i][j] == 1 else 1

        #Add colour
        if len(colour) == 1:
            # img_pixels = np.array(img_pixels, dtype=np.uint8)*colour[0].value
            for i in range(len(img_pixels)):
                for j in range(len(img_pixels[0])):
                    if img_pixels[i][j][0] == 0 and img_pixels[i][j][1] == 0 and img_pixels[i][j][2] == 0: #If black
                        img_pixels[i][j][0] = colour[0].value[0]
                        img_pixels[i][j][1] = colour[0].value[1]
                        img_pixels[i][j][2] = colour[0].value[2]
        else:
            for i in range(len(img_pixels)):
                for j in range(len(img_pixels[0])):
                    if img_pixels[i][j][0] == 0 and img_pixels[i][j][1] == 0 and img_pixels[i][j][2] == 0: #If black
                        #randomly choose a colour
                        c = np.random.choice(colour)
                        img_pixels[i][j][0] = c.value[0]
                        img_pixels[i][j][1] = c.value[1]
                        img_pixels[i][j][2] = c.value[2]
        # print(len(img_pixels), len(img_pixels[0]), len(img_pixels[0][0]))
        # print(img_pixels)

        #Add background colour
        for i in range(len(img_pixels)):
            for j in range(len(img_pixels[0])):
                if img_pixels[i][j][0] == 1 and img_pixels[i][j][1] == 1 and img_pixels[i][j][2] == 1:
                    img_pixels[i][j][0] = bckgrndColour.value[0]
                    img_pixels[i][j][1] = bckgrndColour.value[1]
                    img_pixels[i][j][2] = bckgrndColour.value[2]
        
        pixels = np.array(img_pixels, dtype=np.uint8)*255
        # pixels = img_pixels*255

        image = Image.fromarray(pixels, 'RGB')
        image = image.resize((imgSize, imgSize), Image.NEAREST)
        image.save(filename)

class QRGenerator:
    def __init__(self, msg: str = "Hello World", encoding: qrutils.QREncoding = qrutils.QREncoding.byte, version: qrutils.QRVersion = qrutils.QRVersion.v1, error_correction: qrutils.QRErrorCorrectionLevels = qrutils.QRErrorCorrectionLevels.L):
        self.msg = msg
        self.encoding = encoding
        self.version = version
        self.error_correction = error_correction

    def __str__(self):
        return f"QR(msg={self.msg}, encoding={self.encoding}, version={self.version}, error_correction={self.error_correction})"
    
    def __repr__(self):
        return f"QR(msg={self.msg}, encoding={self.encoding}, version={self.version}, error_correction={self.error_correction})"
    
    def check(self):
        max_character_count = qrutils.MAX_CHARACTERS[qrutils.QREncoding(self.encoding).name][self.error_correction][self.version]

        if len(self.msg) >= max_character_count:
            return False
        else:
            return True
        
    def generate(self):
        # if not self.check():
        #     raise ValueError("Message is too long for the specified encoding, version and error correction level.")
        rawData = qrutils.qr_encode_data(self.version, self.encoding, self.error_correction, self.msg)
        # print(rawData)

        #interleave data blocks and error correction blocks if necessary
        interleavedData = qrutils.interleave_blocks(rawData['dataBytes'], rawData['ErrorCorrection'], self.version)
        #Join the interleaved data blocks into one string
        interleavedData = ''.join(interleavedData)

        #Place the modules and function patterns in the matrix
        qr = QR(version=self.version, encoding=self.encoding, message=self.msg, error_correction=self.error_correction)
        # print(qr)

        #1 - Place the finder patterns, at (0,0), (0, qr.size - 7), (qr.size - 7, 0)
        #(0,0)
        for posx,row in enumerate(finderPattern):
            for posy,col in enumerate(row):
                qr.matrix[posx][posy] = col

        #(0, qr.size - 7)
        for posx,row in enumerate(finderPattern):
            for posy,col in enumerate(row):
                qr.matrix[posx][qr.size - 7 + posy] = col

        #(qr.size - 7, 0)
        for posx,row in enumerate(finderPattern):
            for posy,col in enumerate(row):
                qr.matrix[qr.size - 7 + posx][posy] = col

        #2 - Add the separators
        #2.1 - Top left
        for i in range(8):
            qr.matrix[i][7] = 0
        for i in range(8):
            qr.matrix[7][i] = 0

        #2.2 - Top right
        for i in range(8):
            qr.matrix[i][qr.size - 8] = 0
        for i in range(8):
            qr.matrix[7][qr.size - 1 - i] = 0

        #2.3 - Bottom left
        for i in range(8):
            qr.matrix[qr.size - 8 + i][7] = 0
        for i in range(8):
            qr.matrix[qr.size - 8][i] = 0

        #3 - Add timing patterns
        #Horizontal
        value = 1
        for i in range(8, qr.size - 8):
            qr.matrix[6][i] = value%2
            value += 1

        #Vertical
        value = 1
        for i in range(8, qr.size - 8):
            qr.matrix[i][6] = value%2
            value += 1

        #4 - Add alignment patterns
        patternLocations = qrutils.alignment_pattern_locations(self.version)

        for patternLocation in patternLocations:
            posx = patternLocation[0]
            posy = patternLocation[1]
            #Put pattern at center posx, posy
            offset = [-2, -1, 0, 1, 2]
            for i in range(5):
                for j in range(5):
                    qr.matrix[posx + offset[i]][posy + offset[j]] = alignmentPattern[i][j]

        #5 - Add dark module
        qr.matrix[qr.size - 8][8] = 1

        #6 - Reserve format information area
        #Top-left
        for i in range(9):
            if i != 6:
                qr.matrix[i][8] = 'x'
        for i in range(9):
            if i != 6:
                qr.matrix[8][i] = 'x'
        
        #Top-right
        for i in range(1,9):
            qr.matrix[8][qr.size - i] = 'x'

        #Bottom-left
        for i in range(1,8):
            qr.matrix[qr.size - i][8] = 'x'

        #7 - Reserve version information area
        if self.version.value >= qrutils.QRVersion.v7.value:
            for i in range(6):
                for j in range(3):
                    qr.matrix[i][qr.size - 11 + j] = 'x'
                    qr.matrix[qr.size - 11 + j][i] = 'x'

        #Copy reserved positions to reserved_positions
        for posx,row in enumerate(qr.matrix):
            for posy,col in enumerate(row):
                if col != 'X':
                    qr.reserved_positions[posx][posy] = 1
        # print(qr.reserved_positions)

        #8 - Add data
        #Start from bottom right
        posx = qr.size - 1
        posy = qr.size - 1
        directionUD = 1 #1 = up, -1 = down
        directionLR = 1 #1 = left, -1 = right
        dataPos = 0
        while dataPos < len(interleavedData):
            #Check if we can place data
            if qr.matrix[posx][posy] == 'X':
                qr.matrix[posx][posy] = interleavedData[dataPos]
                dataPos += 1 #Move to next data bit
            # print(posx, posy, dataPos, len(interleavedData))

            #Move to next position
            if directionUD == 1 and directionLR == 1:
                posy -= 1
                directionLR = -1
            elif directionUD == 1 and directionLR == -1:
                posx -= 1
                posy += 1
                directionLR = 1
            elif directionUD == -1 and directionLR == 1:
                # posx += 1
                posy -= 1
                directionLR = -1
            elif directionUD == -1 and directionLR == -1:
                posy += 1
                posx += 1
                directionLR = 1

            #Check if we need to change direction
            if posx == -1:
                directionUD = -1
                posx = 0
                directionLR = 1
                posy -= 2
            elif posx == qr.size:
                directionUD = 1
                posx = qr.size - 1
                directionLR = 1
                posy -= 2

            if posy == 6:
                posy -= 1

            if posy < 0:
                print('No more space for data')
                #exit loop
                break
                
        #9 - Masking
        qr.matrix = qrutils.qr_masking(qr.matrix, qr.reserved_positions, self.error_correction, self.version)
        # originalMatrix = qr.matrix
        # for i in range(8):
        #     qr.matrix = qrutils.qr_masking(originalMatrix, qr.reserved_positions, self.error_correction, self.version, [i])
        #     #Turn every position into int 
        #     #TODO: Find a better way to do this
        #     for posx,row in enumerate(qr.matrix):
        #         for posy,col in enumerate(row):
        #             qr.matrix[posx][posy] = int(col)
            
        #     qr.show()

        # print(qr)
        # print(dataPos, len(interleavedData), (len(interleavedData)-dataPos))

        return qr

#Function to get the correct encoding for the message
def get_encoding(msg: str):
    #Check if message is numeric
    if msg.isnumeric():
        return qrutils.QREncoding.numeric
    #Check if message is alphanumeric
    elif msg.isalnum():
        return qrutils.QREncoding.alphanumeric
    #Check if message is kanji
    elif qrutils.is_byte(msg):
        return qrutils.QREncoding.byte
    elif qrutils.is_kanji(msg):
        return qrutils.QREncoding.kanji


#Function that returns the minimum QR version needed to encode the message
def get_min_version(msg: str, encoding: qrutils.QREncoding = qrutils.QREncoding.byte, error_correction: qrutils.QRErrorCorrectionLevels = qrutils.QRErrorCorrectionLevels.Q):
    min_version = None
    #assign max value to minlength
    minlength = 9999999
    for version in qrutils.QRVersion:
        if len(msg) < qrutils.MAX_CHARACTERS[qrutils.QREncoding(encoding).name][error_correction][version.value] and qrutils.MAX_CHARACTERS[qrutils.QREncoding(encoding).name][error_correction][version.value] < minlength:
            min_version = version
            minlength = qrutils.MAX_CHARACTERS[qrutils.QREncoding(encoding).name][error_correction][version.value]

    return min_version, error_correction

def smallest_qr(msg: str, error_correction: qrutils.QRErrorCorrectionLevels = qrutils.QRErrorCorrectionLevels.Q):
    #Get the encoding
    encoding = get_encoding(msg)
    #Get the minimum version
    version, err = get_min_version(msg, encoding, error_correction)
    #Generate QR code
    generator = QRGenerator(msg=msg, encoding=encoding, version=version, error_correction=err)
    qr = generator.generate()
    #Return QR code
    return qr
            