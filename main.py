from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.button import Button
import os
import re
import math
import cv2
import random

__version__ = "3.0.0"
HeightOfGridField = 0
WidthOfGridField = 0
NumPhotosInRow = 5

def make_tiles_for_grid():
    global HeightOfGridField
    global WidthOfGridField
    global NumPhotosInRow
    img = cv2.imread('image1.jpg')
    heigth, width = img.shape[:2]
    newpath = r'./game_images'   
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    source_dir = os.listdir('./game_images')
    for file in source_dir:
        os.remove("./game_images/"+file)
    counter = 0
    HeightOfGridField = math.floor(heigth/NumPhotosInRow)
    WidthOfGridField = math.floor(width/NumPhotosInRow)
    for r in range(0,heigth, math.floor(heigth/NumPhotosInRow)):
        if r+heigth/NumPhotosInRow<=heigth:
            for c in range(0,width,math.floor(width/NumPhotosInRow)):
                if c+width/NumPhotosInRow<=width:            
                    counter = counter+1
                    cv2.imwrite(f"./game_images/img{counter}.png",img[r:r+math.floor(heigth/NumPhotosInRow), c:c+math.floor(width/NumPhotosInRow),:])


def sort_image_list(image_list):
    return sorted(image_list, key=lambda x: int(x.split('.')[0][3:]))
class GameGrid(GridLayout):
    popupButton = Button(text='Continue?')
    popup = Popup(title='You win',content=popupButton,size_hint=(None, None), size=(400, 400))
    image_list = []
    def __init__(self, **kwargs):
        global NumPhotosInRow
        super(GameGrid, self).__init__(**kwargs)
        self.cols = NumPhotosInRow
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
        #self.randomize()
        #self.popupButton.bind(onpress=self.on_popup_button_press)
                     
    
    def on_image_touch_down(self, instance, touch):
            if instance.collide_point(*touch.pos):
                index = self.get_index_of_instance(instance)
                self.move_image(index, instance)
                #self.swap_images(instance, self.image_list[1])

                print('Label touched:', self.is_completed())
                if(self.is_completed()):
                    self.popupButton.bind(on_press=self.on_popup_button_press)
                    self.popup.open()

    def move_image(self, index, instance):
            global NumPhotosInRow
            if index>NumPhotosInRow*NumPhotosInRow-1 | index<0:
                return
            if index>NumPhotosInRow-1 : 
                if self.image_list[index-NumPhotosInRow].source == "":
                    self.swap_images(instance, self.image_list[index-NumPhotosInRow])
            if index<NumPhotosInRow*NumPhotosInRow-NumPhotosInRow:
                if self.image_list[index+NumPhotosInRow].source == "":
                    self.swap_images(instance, self.image_list[index+NumPhotosInRow])
            if (index)%NumPhotosInRow>0:
                if self.image_list[index-1].source == "":
                    self.swap_images(instance, self.image_list[index-1])
            if (index)%NumPhotosInRow<NumPhotosInRow-1:
                if self.image_list[index+1].source == "":
                    self.swap_images(instance, self.image_list[index+1])

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

    def on_popup_button_press(self, instance):
        self.randomize()
        self.popup.dismiss()

    def randomize(self):
        arr = [+1, -1, 0+NumPhotosInRow, 0-NumPhotosInRow]
        i = 0
        print("ne randomiziram\n")
        while i<100:
            print("randomiziram",i,"\n")
            idx_in_arr = random.randint(0, 3)
            idx = self.get_index_of_empty_field()+arr[idx_in_arr]
            if idx>NumPhotosInRow*NumPhotosInRow-1 or idx<0:
                print("index is not valid:", idx)
                continue            
            print("image index:", idx )
            for image in self.image_list:
                if self.get_index_of_instance(image) == idx: 
                    instance = image

            self.move_image(idx, instance)
            i = i + 1

    def get_index_of_empty_field(self):
        i = 0
        for image in self.image_list:
            if image.source == "":
                print("i:", i)
                return i
            i = i + 1

    def get_index_of_instance(self, instance):
        i = 0
        for image in self.image_list:
            if(image.source == instance.source): 
                return i 
            #print("i:", i)
            i = i + 1
    #

class MyApp(App):

    def build(self):
        make_tiles_for_grid()
        return GameGrid()


if __name__ == '__main__':
    MyApp().run()