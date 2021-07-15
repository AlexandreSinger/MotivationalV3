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
def createMotivationalWhiteCloud(inputImg, motivationalText):
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

# function that draws centered text at a given height (centered to center of screen)
def drawCenteredText(img, text, height, textColor):
    # Draw the text onto the cloud
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("data/BreeSerif-Regular.ttf", 48) # <-- font size
    textLines = textwrap.wrap(text, width=48) # <--- "width" of line, essentially the number of characters per line

    totalHeight = (len(textLines)-1)*15
    for line in textLines:
        totalHeight += font.getsize(line)[1]
    offset = height+(207/2) - (totalHeight/2)

    for line in textLines:
        lineSize = draw.textsize(line, font=font)
        draw.text(((imageWidth - lineSize[0])/2, offset), line, font=font, fill=textColor)
        offset += font.getsize(line)[1] + 10
    return img

# function that draws left justified text at a given x and y position (approximate)
def drawLeftJustifiedText(img, text, x, y, textColor):
    # Draw the text onto the cloud
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("data/BreeSerif-Regular.ttf", 24) # <-- font size
    textLines = textwrap.wrap(text, width=36) # <--- "width" of line, essentially the number of characters per line

    totalHeight = (len(textLines)-1)*15
    for line in textLines:
        totalHeight += font.getsize(line)[1]
    offset = y+(207/2) - (totalHeight/2)

    for line in textLines:
        lineSize = draw.textsize(line, font=font)
        draw.text((x, offset), line, font=font, fill=textColor)
        offset += font.getsize(line)[1] + 10
    return img

black_background_828 = Image.open("data/black_background_828.jpg")
def createMotivationalBlackBox(inputImg, motivationalText):
    # create base black RGBA image
    baseImage = Image.new('RGBA', black_background_828.size)
    baseImage.paste(black_background_828)

    # paste the input image onto the background
    baseImage.paste(inputImg)

    # draw text onto image
    # args: img, text, height of text, color of text          [V change this number]
    baseImage = drawCenteredText(baseImage, motivationalText, 628, "white")

    # convert image to RGB and returen new image
    with Image.new('RGB', baseImage.size) as new_image:
        new_image.paste(baseImage)
        return new_image

white_background_828 = Image.open("data/white_background_828.jpg")
def createMotivationalWhiteBox(inputImg, motivationalText):
    # create base white RGBA image
    baseImage = Image.new('RGBA', white_background_828.size)
    baseImage.paste(white_background_828)

    # paste the input image onto the background
    baseImage.paste(inputImg)

    # draw text onto image
    # args: img, text, height of text, color of text          [V change this number]
    baseImage = drawCenteredText(baseImage, motivationalText, 628, "black")

    # convert image to RGB and returen new image
    with Image.new('RGB', baseImage.size) as new_image:
        new_image.paste(baseImage)
        return new_image

white_horizontal_line = Image.open("data/white_horizontal_line.jpg")
def createMotivationalLeftSideBlack(inputImg, motivationalText, title):
    # create base black RGBA image
    baseImage = Image.new('RGBA', black_background_828.size)
    baseImage.paste(black_background_828)

    # paste the input image onto the background
    inputImgWidth, inputImgHeight = inputImg.size
    # resize the input image such that it is smaller
    scale = 5/8 # scale that will change the size of the image
    resizedImg = inputImg.resize((int(scale*inputImgWidth), int(scale*inputImgHeight)), Image.ANTIALIAS)
    # paste the image at this (x,y) position
    baseImage.paste(resizedImg, (0, 250))

    # paste white horizontal line at this (x,y) position
    baseImage.paste(white_horizontal_line, (0, 200))

    # paste title
    draw = ImageDraw.Draw(baseImage)
    font = ImageFont.truetype("data/BreeSerif-Regular.ttf", 48) # <-- font size
    # draw the text at this approximate (x,y) position
    draw.text((550, 170), title, font=font, fill="white")

    # past motivational text
    #                                                               V    V  (x and y)
    baseImage = drawLeftJustifiedText(baseImage, motivationalText, 760, 300, "white")

    # convert image to RGB and returen new image
    with Image.new('RGB', baseImage.size) as new_image:
        new_image.paste(baseImage)
        return new_image

black_horizontal_line = Image.open("data/black_horizontal_line.jpg")
def createMotivationalLeftSideWhite(inputImg, motivationalText, title):
    # create base black RGBA image
    baseImage = Image.new('RGBA', white_background_828.size)
    baseImage.paste(white_background_828)

    # paste the input image onto the background
    inputImgWidth, inputImgHeight = inputImg.size
    # resize the input image such that it is smaller
    scale = 5/8 # scale that will change the size of the image
    resizedImg = inputImg.resize((int(scale*inputImgWidth), int(scale*inputImgHeight)), Image.ANTIALIAS)
    # paste the image at this (x,y) position
    baseImage.paste(resizedImg, (0, 250))

    # paste black horizontal line at this (x,y) position
    baseImage.paste(black_horizontal_line, (0, 200))

    # paste title
    draw = ImageDraw.Draw(baseImage)
    font = ImageFont.truetype("data/BreeSerif-Regular.ttf", 48) # <-- font size
    # draw the text at this approximate (x,y) position
    draw.text((550, 170), title, font=font, fill="black")

    # past motivational text
    #                                                               V    V  (x and y)
    baseImage = drawLeftJustifiedText(baseImage, motivationalText, 760, 300, "black")

    # convert image to RGB and returen new image
    with Image.new('RGB', baseImage.size) as new_image:
        new_image.paste(baseImage)
        return new_image


start = time.time()

def removeOutputFiles(folderLocation):
    outputFiles = os.listdir(folderLocation)
    for file in outputFiles:
        if file != ".DS_Store":
            os.remove(folderLocation + file)
removeOutputFiles('output/white_cloud/')
removeOutputFiles('output/black_box/')
removeOutputFiles('output/white_box/')
removeOutputFiles('output/left_side_black/')
removeOutputFiles('output/left_side_white/')
removeOutputFiles('output/no_text/')


with open("input.csv", 'r') as inputFile:
    csvReader = csv.reader(inputFile, delimiter=',')
    next(csvReader, None)
    for row in csvReader:
        if row[1] != '':
            print("Creating Motivational: " + row[1])
            with Image.open("input/" + row[1]) as img:
                # no change
                img.save("output/no_text/" + os.path.splitext(os.path.split(row[1])[1])[0] + ".jpg")
                # white cloud
                createMotivationalWhiteCloud(img, row[0]).save("output/white_cloud/" + os.path.splitext(os.path.split(row[1])[1])[0] + ".jpg")
                # black box
                createMotivationalBlackBox(img, row[0]).save("output/black_box/" + os.path.splitext(os.path.split(row[1])[1])[0] + ".jpg")
                # white box
                createMotivationalWhiteBox(img, row[0]).save("output/white_box/" + os.path.splitext(os.path.split(row[1])[1])[0] + ".jpg")
                # left side black
                createMotivationalLeftSideBlack(img, row[0], row[2]).save("output/left_side_black/" + os.path.splitext(os.path.split(row[1])[1])[0] + ".jpg")
                # left side white
                createMotivationalLeftSideWhite(img, row[0], row[2]).save("output/left_side_white/" + os.path.splitext(os.path.split(row[1])[1])[0] + ".jpg")

print("Completed in "+ str(round(time.time() - start, 2))+ " seconds")

