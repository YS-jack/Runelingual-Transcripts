import os
from PIL import Image, ImageDraw, ImageFont
import unicodedata
import math
import common_func
import zipfile
from common_func import LANG

TEXTCOLOR = [(60, 60,60, 255), (255, 255, 0, 255), (255, 0, 0, 255)
                    , (255, 165, 0, 255), (255, 255, 255, 255), (0, 255, 255, 255), (0, 255, 0, 255), (0, 0, 255, 255)]#blue was 0,0,255
COLORORDER = ('black', 'yellow', 'red', 'orange', 'white','lightblue', 'green', 'blue') #remove orange, white, lightblue, green
FONTSIZE = 14
BGCOLOR = [(204, 187, 154, 255),(156,148,0,255) ,(176,23,23,255) ,(140,99,24,255), (100,100,100,255), (41,135,135,255), (10,130,10,255), (115,120,245,255)] # blue bgcolor was (115,120,245,255)
BGTEXTCOLOR = [(255,255,255,0), (0,0,0,255),(0,0,0,0), # order = (1'black', 2'yellow', 3'red',
           (0,0,0,0), (0,0,0,0), (0,0,0,0), (0,10,0,0),(255, 255, 255, 0)]#4'orange', 5'white', 6'lightblue', 7'green', 8'blue')
TEXTPAD = (0,0)#(width, height)
BGTXTPAD = (1,1)  #(width, height)

#the color to skip in function "make_image_opaque"
TXTCOLORSTOSKIP = ["black"]

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

def get_font_list():
    # Get the current directory
    current_directory = os.getcwd()
    
    # Construct the path to the "fonts" folder
    fonts_folder_path = os.path.join(current_directory, "fonts")
    
    # Check if the "fonts" folder exists
    if os.path.exists(fonts_folder_path) and os.path.isdir(fonts_folder_path):
        # Get a list of all files in the "fonts" folder ending with ".ttf"
        ttf_files = [os.path.join(fonts_folder_path,file) for file in os.listdir(fonts_folder_path) if file.endswith(".ttf")]
        return ttf_files
    else:
        print("The 'fonts' folder does not exist or is not a directory.")
        return []
        
def make_image_opaque(image_path):
    # Open the image
    img = Image.open(image_path)

    # Ensure the image has an alpha channel
    if img.mode != 'RGBA':
        img = img.convert('RGBA')

    # Load the data of the image
    data = img.getdata()
    bgColor, c = getBGColor(image_path) # in rgba
    #bgColor = (156,148,0,255)
    if not c in TXTCOLORSTOSKIP:
        '''for pixel in data:
            print("pixel color = " + str(pixel[0]) + ", " + str(pixel[1]) + ", " + str(pixel[2]) + ", " + str(pixel[3]))
            print("bgColor     = " + str(bgColor[0]) + ", " + str(bgColor[1]) + ", " + str(bgColor[2]) + ", " + str(bgColor[3]))
            print()]'''
        #print(bgColor)
        data = [(0, 0, 0, 0) \
                    if item[0] == bgColor[0] and item[1] == bgColor[1] and item[2] == bgColor[2] \
                    else item for item in data]
        # Create a new data array where all non-transparent pixels are made opaque

        threshold = 25 #transparency out of 255
        data = [(item[0], item[1], item[2], 255) if item[3] > threshold else item for item in data]
        new_data = [(item[0], item[1], item[2], 0) if item[3] <= threshold else item for item in data]

        # Update image data
        img.putdata(new_data)
        # Save the modified image
        img.save(image_path)
    else:
        threshold = 25 #transparency out of 255
        data = [(item[0], item[1], item[2], 255) if item[3] > threshold else item for item in data]
        new_data = [(item[0], item[1], item[2], 0) if item[3] <= threshold else item for item in data]

        # Update image data
        img.putdata(new_data)
        # Save the modified image
        img.save(image_path)

def process_directory_to_opaque(directory):
    for file in os.listdir(directory):
        if file.endswith('.png'):
            image_path = os.path.join(directory, file)
            make_image_opaque(image_path)

def zip_char_img(zip_file_name, target_folder_path):
    #zip_file_name = './repos/char.zip'
    #folder_path = './repos/char'
    with zipfile.ZipFile(zip_file_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(target_folder_path):
            for file in files:
                # Create a proper path for each file to be stored in the zip
                file_path = os.path.join(root, file)
                # Adding file to zip
                zipf.write(file_path, os.path.relpath(file_path, os.path.dirname(target_folder_path)))

if __name__ == '__main__':
    print("enter a number;")
    for i, lang in enumerate(LANG):
        print(f"{i} for {lang}")
    language_num = int(input("for the language you wish to generate character images: "))
    language = LANG[language_num]
    file_path = "char_lists/all_char_" + language + ".txt"
    chars_list = read_file_to_list(file_path)

    font_candidates = get_font_list()
    print("enter a number;")
    for i, f in enumerate(font_candidates):
        print(f"{i} for {f}")
    font_num = int(input("to select font for character images generated: "))
    font_path = font_candidates[font_num]

    output_dir_base = "../draft/" + language + "/char_" + language
    common_func.remove_existing_dir(directory_path="../draft/" + language,folder_name="char")
    common_func.create_directories_if_not_exist(output_dir_base=output_dir_base)


    create_images(chars_list, font_path, output_dir_base, TEXTCOLOR)
    process_directory_to_opaque(output_dir_base)
    zip_char_img(zip_file_name="../draft/" + language + "/char_"  + language + ".zip", target_folder_path=output_dir_base)
    #list_image_names(output_dir_base)