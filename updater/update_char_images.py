import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw, ImageFont
import unicodedata
import math
import common_func
import zipfile
from common_func import LANG
import update_hash

font_size_lang = {'ja':12, 'ru':10} # add more languages as needed

TEXTCOLOR = [(33, 33,33, 255), (255, 255, 0, 255), (255, 0, 0, 255)
                    , (255, 165, 0, 255), (255, 255, 255, 255), (0, 255, 255, 255), (0, 255, 0, 255), (0, 0, 255, 255)]#blue was 0,0,255
COLORORDER = ('black', 'yellow', 'red', 'orange', 'white','lightblue', 'green', 'blue') #remove orange, white, lightblue, green
FONTSIZE = 12

BGCOLOR = [(130,130,130, 255),(156,148,0,255) ,(176,23,23,255) ,(140,99,24,255), (100,100,100,255), (41,135,135,255), (10,130,10,255), (115,120,245,255)] # blue bgcolor was (115,120,245,255)
BGTEXTCOLOR = [(255,255,255,0), (0,0,0,255),(0,0,0,0), # order = (1'black', 2'yellow', 3'red',
           (0,0,0,0), (0,0,0,0), (0,0,0,0), (0,10,0,0),(255, 255, 255, 0)]#4'orange', 5'white', 6'lightblue', 7'green', 8'blue')
TEXTPAD = (0,0)#(width, height)
BGTXTPAD = (1,1)  #(width, height)

#the color to skip in function "make_image_opaque"
TXTCOLORSTOSKIP = []#["black"]

def setFontSize(lang):
    if lang in font_size_lang:
        return font_size_lang[lang]
    else:
        return font_size_lang['ja']

def getBGColor(filename):
    for i,c in enumerate(COLORORDER):
        if c in filename:
            return BGCOLOR[i], c
    print ("color for file name '" + filename + "' not found, returning black color rgba")
    return BGCOLOR[0], COLORORDER[0]


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

def setGoodFontSize(char, lang):
    if lang == 'ja':
        return setJaFontSize(char)
    elif lang == 'ru':
        return setRuFontSize(char)
    else:
        return FONTSIZE
    

def setRuFontSize(char):
    # set width of character so none are too wide and have spaces on their sides
    # see setJaFontSize for example
    return FONTSIZE

def setJaFontSize(char):
    width = FONTSIZE
    if unicodedata.east_asian_width(char) in ['Na', 'H']: # I dont remember what this means, but it's for japanese characters
        width = math.ceil(FONTSIZE*0.7)
    if char in ('M', 'W'): # these characters wider than normal, so set their width to be wider
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
    elif char in ('1','t', 'J', 'I','"','(',')','[',']', '{','}','\\','_','-','、','。','「','」','*','/','~','”','^','`','・'):
        width = math.floor(FONTSIZE*0.5)
    elif char in (' ', 'i', '|','!', '　', '\'',':',';', 'l','j','’','（','）','：','；','.',',','|','…'): # these are some of the narrowest characters, so set their width to be narrow
        width = math.ceil(FONTSIZE*0.3)
    return width


def create_images(chars_list, font_path, output_dir, colors, lang):
    font = ImageFont.truetype(font_path, FONTSIZE)  # Load the font, size FONTSIZE
    
    for i, color in enumerate(colors):
        
        colorName = COLORORDER[i]
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        for char in chars_list:
            charName = colorName + '--' + str(ord(char))

            width = setGoodFontSize(char, lang)

            image = Image.new('RGBA', (width + TEXTPAD[0], FONTSIZE+ TEXTPAD[1]), BGCOLOR[i])  # Create blank image
            # set top padding to transparrent if colour is black
            if colorName == 'black':
                pixels = image.load()
                for x in range(width):
                    for y in range(TEXTPAD[1]):  # Top rows
                        pixels[x, y] = (0, 0, 0, 0) 
            
            textPadActual = TEXTPAD
            if(char in ["g","j","p","q"]):
                textPadActual = [TEXTPAD[0] + 0,TEXTPAD[1]-0]
                
            draw = ImageDraw.Draw(image)
            #draw shade of character for yellow only, because overhead texts look strange without it
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

def get_font_list(lang):
    # Get the current directory
    current_directory = os.getcwd()
    
    # Construct the path to the "fonts" folder
    fonts_folder_path = os.path.join(current_directory, "fonts")
    fonts_folder_path = os.path.join(fonts_folder_path, lang)
    
    # Check if the "fonts" folder exists
    if os.path.exists(fonts_folder_path) and os.path.isdir(fonts_folder_path):
        # Get a list of all files in the "fonts" folder ending with ".ttf"
        ttf_files = [os.path.join(fonts_folder_path,file) for file in os.listdir(fonts_folder_path) if file.endswith(".ttf")]
        return ttf_files
    else:
        print(f"The 'fonts/'{lang} folder does not exist or is not a directory.")
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

    setFontSize(language)
    font_candidates = get_font_list(language)
    print("enter a number;")
    for i, f in enumerate(font_candidates):
        print(f"{i} for {f}")
    font_num = int(input("to select font for character images generated: "))
    font_path = font_candidates[font_num]

    output_dir_base = "../draft/" + language + "/char_" + language
    common_func.remove_existing_dir(directory_path="../draft/" + language,folder_name="char")
    common_func.create_directories_if_not_exist(output_dir_base=output_dir_base)


    create_images(chars_list, font_path, output_dir_base, TEXTCOLOR, language)
    process_directory_to_opaque(output_dir_base)
    zip_char_img(zip_file_name="../draft/" + language + "/char_"  + language + ".zip", target_folder_path=output_dir_base)
    #list_image_names(output_dir_base)

    print('\nupdating hash files for all languages')
    update_hash.main()