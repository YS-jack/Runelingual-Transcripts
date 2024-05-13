import os
import sys
from PIL import Image, ImageDraw, ImageFont
import unicodedata
import math

"""
edit below to add/remove languages
"""
# must mach lang code in LangCodeSelectableList.java
LANG = ['pt_br', 'no','jp']

"""
dont edit anything else below (unless you know what youre doing)
"""

TEXTCOLOR = [(60, 60,60, 255), (255, 255, 0, 255), (255, 0, 0, 255)
                    , (255, 165, 0, 255), (255, 255, 255, 255), (0, 255, 255, 255), (0, 255, 0, 255), (0, 0, 255, 255)]#blue was 0,0,255
COLORORDER = ('black', 'yellow', 'red', 'orange', 'white','lightblue', 'green', 'blue') #remove orange, white, lightblue, green
FONTSIZE = 14
BGCOLOR = [(204, 187, 154, 255),(156,148,0,255) ,(176,23,23,255) ,(140,99,24,255), (100,100,100,255), (41,135,135,255), (10,130,10,255), (115,120,245,255)] # blue bgcolor was (115,120,245,255)
BGTEXTCOLOR = [(255,255,255,0), (0,0,0,255),(0,0,0,0), # order = (1'black', 2'yellow', 3'red',
           (0,0,0,0), (0,0,0,0), (0,0,0,0), (0,10,0,0),(255, 255, 255, 0)]#4'orange', 5'white', 6'lightblue', 7'green', 8'blue')
TEXTPAD = (0,0)#(width, height)
BGTXTPAD = (1,1)  #(width, height)

def getBGColor(filename):
    for i,c in enumerate(COLORORDER):
        if c in filename:
            return BGCOLOR[i], c
    print ("color for file name '" + filename + "' not found, returning black color rgba")
    return BGCOLOR[0], COLORORDER[0]


def getCharName(char):
    if char == '\\':
        return 'back_slash'
    if char == '/':
        return 'forward_slash'
    if char == ':':
        return 'colon'
    if char == '*':
        return 'star'
    if char == '?':
        return 'question'
    if char == '"':
        return 'double-quotation'
    if char == '<':
        return 'greaterthan'
    if char == '>':
        return 'lessthan'
    if char == '|':
        return 'or'

def read_file_to_list(file_path):
    char_list = []
    with open(file_path, 'r', encoding='utf-8') as file:
        while True:
            char = file.read(1)
            if not char:  # End of file
                break
            if char != '\n':  # Exclude newline characters
                char_list.append(char)
    return char_list

def setGoodFontSize(char):
    width = FONTSIZE
    if unicodedata.east_asian_width(char) in ['Na', 'H']:
        width = math.ceil(FONTSIZE*0.7)
    if char in ('M', 'W'):
        width = math.ceil(FONTSIZE*1.02)
    elif char in ('%', '@', 'm', '#'):
        width = FONTSIZE
    elif char in ('N', 'O', 'Q','ぉ','ゃ','ゅ','ょ','ァ','ィ','ゥ','ェ','ォ','ャ','ュ','ョ', '&'):
        width = math.ceil(FONTSIZE*0.9)
    elif char in ('w', 'D','U','ぁ','ぃ','ぅ', 'ぇ','っ'):
        width = math.floor(FONTSIZE*0.9)
    elif char in ('d','e','k','y', 's','u'):
        width = math.floor(FONTSIZE*0.7)
    elif char in ('a','c','v', 'x','z'):
        width = math.floor(FONTSIZE*0.65)
    elif char in ('f', 'r','｝','｛','＾'):
        width = math.floor(FONTSIZE*0.6)
    elif char in ('1','t', 'J', 'I','"','(',')','[',']', '{','}','\\','_','-','、','。','「','」','*','/','~','”','^','`'):
        width = math.floor(FONTSIZE*0.5)
    elif char in (' ', 'i', '|','!', '　', '\'',':',';', 'l','j','’','（','）','：','；','.',',','|'):
        width = math.ceil(FONTSIZE*0.3)
    return width
# review :8217 8221

def create_images(chars_list, font_path, output_dir, colors):
    font = ImageFont.truetype(font_path, FONTSIZE)  # Load the font, size FONTSIZE
    
    for i, color in enumerate(colors):
        
        colorName = COLORORDER[i]
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        for char in chars_list:
            charName = colorName + '--' + str(ord(char))

            width = setGoodFontSize(char)

            image = Image.new('RGBA', (width + TEXTPAD[0], FONTSIZE+ TEXTPAD[1]), BGCOLOR[i])  # Create blank image
            # set top padding to transparrent if colour is black
            if colorName == 'black':
                pixels = image.load()
                for x in range(width):
                    for y in range(TEXTPAD[1]):  # Top rows
                        pixels[x, y] = (0, 0, 0, 0) 
            if(char in ["g","j","p","q"]):
                textPadActual = [TEXTPAD[0] + 0,TEXTPAD[1]-0]
            else:
                textPadActual = TEXTPAD
            draw = ImageDraw.Draw(image)
            #draw shade of character
            if colorName == 'yellow':
                draw.text((textPadActual[0] + BGTXTPAD[0], textPadActual[1]+BGTXTPAD[1]), char, font=font, fill=BGTEXTCOLOR[i])
            draw.text((textPadActual[0], textPadActual[1]), char, font=font, fill=color)  # Draw the character
            image_file_name = f'{charName}.png' 
            image.save(os.path.join(output_dir, image_file_name))  # Save the image

def list_image_names(out_dir_base):
    output_file_path = os.path.join(out_dir_base,'image_name_list.txt')

    # Open the output file in write mode
    with open(output_file_path, 'w') as file:
        # List all files in the directory
        for filename in os.listdir(out_dir_base):
            # Create the full path to the file
            full_path = os.path.join(out_dir_base, filename)
            # Check if it's a file and not a directory
            if os.path.isfile(full_path):
                # Write the filename to the file with a newline
                file.write(filename + '\n')

        


if __name__ == '__main__':
    print("enter")
    for i, lang in enumerate(LANG):
        print("{i} for {lang}")
    language = input("for the language you wish to generate character images:")
    file_path = "all_char_" + language + ".txt"
    if len(sys.argv) == 5:
        dirOrStringOption = sys.argv[1]
        if dirOrStringOption == 'd':
            file_path = sys.argv[2].replace('\\', '/')
            chars_list = read_file_to_list(file_path)

        font_path = sys.argv[3].replace('\\', '/')
        output_dir_base = sys.argv[4].replace('\\', '/')
        create_images(chars_list, font_path, output_dir_base, TEXTCOLOR)
        list_image_names(output_dir_base)
    else:
        print("Usage: python update_non_Alphabet_char.py d <charList_path> <font_path> <output_dir>")
        print("Usage2: python update_non_Alphabet_char.py s <string of char to process> <font_path> <output_dir>")
        sys.exit(1)