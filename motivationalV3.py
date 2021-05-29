from PIL import Image, ImageFont, ImageDraw
import textwrap
import smartcrop
import time
import csv
import os

cropperResolution = 200
cropper = smartcrop.SmartCrop()
def smartCropImage(fileName, width, height):
    with Image.open(fileName) as image:
        if image.mode != 'RGB':
            #display.print_message(fileName + " convert from mode=" + str(image.mode) + " to mode='RGB'", "continuing with converted file...")
            with Image.new('RGB', image.size) as new_image:
                new_image.paste(image)
                image = new_image
        result = cropper.crop(image, width=cropperResolution, height=int(height/width*cropperResolution))
        box = (
            result['top_crop']['x'],
            result['top_crop']['y'],
            result['top_crop']['width'] + result['top_crop']['x'],
            result['top_crop']['height'] + result['top_crop']['y']
        )
        with image.crop(box).resize((width, height), Image.ANTIALIAS) as out:
            return out
            #out.save("output/" + fileName)
    #display.print()

imageWidth = 1200
imageHeight = 628
cloudImage = Image.open("data/new-cloud.png")
cloudImage = cloudImage.resize((imageWidth, 307), Image.ANTIALIAS)
def createMotivational(inputImg, motivationalText):
    # Create a base RGBA image
    baseImage = Image.new('RGBA', (imageWidth, imageHeight))

    # Paste input image on top of the base as the background
    baseImage.paste(inputImg)

    # Paste the cloud texture
    baseImage.paste(cloudImage, (0, 321), cloudImage)

    # Draw the text onto the cloud
    draw = ImageDraw.Draw(baseImage)
    font = ImageFont.truetype("data/helvetica.ttf", 48)
    textLines = textwrap.wrap(motivationalText, width=48)

    totalHeight = (len(textLines)-1)*15
    for line in textLines:
        totalHeight += font.getsize(line)[1]
    offset = 378+(207/2) - (totalHeight/2)

    for line in textLines:
        lineSize = draw.textsize(line, font=font)
        draw.text(((imageWidth - lineSize[0])/2, offset), line, font=font, fill="black")
        offset += font.getsize(line)[1] + 15

    # Convert image to RGB and return the new image
    with Image.new('RGB', baseImage.size) as new_image:
        new_image.paste(baseImage)
        return new_image

start = time.time()

outputFiles = os.listdir('output/')
for file in outputFiles:
    if file != ".DS_Store":
        os.remove('output/' + file)

with open("input.csv", 'r') as inputFile:
    csvReader = csv.reader(inputFile, delimiter=',')
    next(csvReader, None)
    for row in csvReader:
        if row[1] != '':
            print("Creating Motivational: " + row[1])
            createMotivational(smartCropImage("input/" + row[1], imageWidth, imageHeight), row[0]).save("output/" + os.path.splitext(os.path.split(row[1])[1])[0] + ".jpg")

print("Completed in "+ str(round(time.time() - start, 2))+ " seconds")

