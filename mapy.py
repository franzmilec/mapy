import os
from PIL import Image, ImageFilter, ImageEnhance
import PIL.ImageOps
import urllib, cStringIO
from moviepy.editor import *

frameArray = []
cities = ["Bratislava","Budapest","Praha"] # add your own cities


for add in range(0,len(cities)):

    for i in range(7,20):
        angle = 'https://maps.googleapis.com/maps/api/staticmap?center=' + cities[add] + '&size=640x640&maptype=satellite&key=YOUR-API-KEY&zoom=' + str(i) #add your own key
        file = cStringIO.StringIO(urllib.urlopen(angle).read()) # manages URL
        image_file = Image.open(file)
        image_file_scaled = image_file;
        print('image ' + str(i) + ' downloaded')
        filename = '/YOUR-MAPY-FOLDER/' + cities[add] + str((i-7)*8) + '.png'
        image_file.save(filename, 'PNG')
        frameArray.append(filename)


        for x in range(1,8):
            image_file_scaled = image_file.resize((640+x*80, 640+x*80)) # resizes n+.25 times
            image_file_scaled = image_file_scaled.crop((x*40, x*40, 640+x*40, 640+x*40)) # crops back to 640 by 640

            filename = '/YOUR-MAPY-FOLDER/' + cities[add] + str((i-7)*8+x) + '.png'
            image_file_scaled.save(filename, 'PNG')
            frameArray.append(filename)

        if i == 7 and add > 0:
            for x in range(0,7):
                filename_orig = '/YOUR-MAPY-FOLDER/' + cities[add-1] + str(97+x) + '.png'
                background = Image.open(filename_orig)
                background = background.convert('RGBA')
                background = background.filter(ImageFilter.GaussianBlur(radius=x))
                filename = '/YOUR-MAPY-FOLDER/' + cities[add] + str(0+x) + '.png'
                image_file_scaled = Image.open(filename)
                image_file_scaled = image_file_scaled.convert('RGBA')
                #image_file_scaled = image_file_scaled.filter(ImageFilter.GaussianBlur(radius=7-x))
                trans = (x+1) * 0.125
                image_file_scaled = Image.blend(background, image_file_scaled, trans)
                filename = '/YOUR-MAPY-FOLDER/' + cities[add] + str((i-7)*8+x) + '.png'
                image_file_scaled.save(filename, 'PNG')
                os.remove(filename_orig)
                frameArray.remove(filename_orig)

result = ImageSequenceClip(frameArray, fps=25)
result = result.to_videofile('/YOUR-MAPY-FOLDER/video.mp4', fps=25) # many options available
