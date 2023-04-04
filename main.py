from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
import os
import re
import math
import cv2
import random

__version__ = "3.0.0"
HeightOfGridField = 0
WidthOfGridField = 0

def make_tiles_for_grid():
    global HeightOfGridField
    global WidthOfGridField
    img = cv2.imread('image.jpg')
    heigth, width = img.shape[:2]
    newpath = r'./game_images'   
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    source_dir = os.listdir('./game_images')
    for file in source_dir:
        os.remove("./game_images/"+file)
    counter = 0
    HeightOfGridField = math.floor(heigth/3)
    WidthOfGridField = math.floor(width/3)
    for r in range(0,heigth, math.floor(heigth/3)):
        for c in range(0,width,math.floor(width/3)):
            if c+math.floor(width/3)<width:            
                counter = counter+1
                cv2.imwrite(f"./game_images/img{counter}.png",img[r:r+math.floor(heigth/3), c:c+math.floor(width/3),:])


def sort_image_list(image_list):
    return sorted(image_list, key=lambda x: int(x.split('.')[0][3:]))
class GameGrid(GridLayout):
    image_list = []
    def __init__(self, **kwargs):
        
        super(GameGrid, self).__init__(**kwargs)
        self.cols = 3
        source_dir = os.listdir('./game_images')
        print("files:")
        print(source_dir)
        source_dir = sort_image_list(source_dir)
        os.remove("./game_images/"+source_dir.pop())
        print (source_dir)
        for file in source_dir:
            if re.match(r"img[0-9]+\.png", file) :
                image = Image(source="./game_images/"+file, allow_stretch=True, keep_ratio=False)
                self.add_widget(image)
                image.bind(on_touch_down=self.on_image_touch_down)
                self.image_list.append(image)
                print ("new entry: ",self.image_list[-1].source)
        last_image = Image(source="", allow_stretch=True, keep_ratio=False)
        self.add_widget(last_image)
        last_image.bind(on_touch_down=self.on_image_touch_down)
        self.image_list.append(last_image)
        self.randomize()
                     
    
    def on_image_touch_down(self, instance, touch):
            if instance.collide_point(*touch.pos):
                index = self.get_index_of_instance(instance)
                if index>2 : 
                    if self.image_list[index-3].source == "":
                        self.swap_images(instance, self.image_list[index-3])
                if index<6:
                    if self.image_list[index+3].source == "":
                        self.swap_images(instance, self.image_list[index+3])
                if (index)%3>0:
                    if self.image_list[index-1].source == "":
                        self.swap_images(instance, self.image_list[index-1])
                if (index)%3<2:
                    if self.image_list[index+1].source == "":
                        self.swap_images(instance, self.image_list[index+1])
                #self.swap_images(instance, self.image_list[1])

                print('Label touched:', self.is_completed())
    
    def is_completed(self):
        i=0
        completed = True
        num = 0
        for image in self.image_list:
            i=i+1
            tmp = image.source
            if len(self.image_list) != i:
                if image.source!="":
                    num = int(tmp.replace("./game_images/img", '').replace(".png", ''))
                if  num != i:
                    completed = False
                    return completed
            else:
                if tmp == "" : completed = True
        return completed 
        
    def swap_images(self, Image1, Image2):
        Image_tmp = Image1.source
        Image1.source = Image2.source
        Image2.source = Image_tmp

    def randomize(self):
        for Image in self.image_list:
            self.swap_images(Image, self.image_list[random.randint(0,len(self.image_list)-1)])

    def get_index_of_instance(self, instance):
        i = 0
        for image in self.image_list:
            if(image.source == instance.source): return i 
            i = i + 1
    #

class MyApp(App):

    def build(self):
        make_tiles_for_grid()
        return GameGrid()


if __name__ == '__main__':
    MyApp().run()