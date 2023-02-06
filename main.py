from kivy.app import App
from kivy.uix.camera import Camera
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.filechooser import FileChooserIconView,FileChooserListView
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window  import Window
import time
import cv2
import numpy as np
from android import loadingscreen
from android.permissions import request_permissions, Permission

from kivy.graphics import Rotate, PushMatrix, PopMatrix




class MainScreen(Screen,FloatLayout):
    def __init__(self, **kwargs):
        super(MainScreen,self).__init__(**kwargs)
        self.btn = Button(text ="Take a Picture",on_press = self.cam,size_hint=[0.35,0.05],pos_hint={"x":0.35,"top":0.4})
        self.add_widget(self.btn)
        self.btn2 = Button(text ="Choose Existing", on_press=self.switch_screen,size_hint=[0.35,0.05],pos_hint={"x":0.35,"top":0.5})
        self.add_widget(self.btn2)
        self.dev_mode = Button(text = "Dev Mode",size_hint=[0.35,0.05],pos_hint={"x":0.10,"top":0.07})
        self.dev_mode.bind(on_press = self.switch_to_dev_screen)
        self.add_widget(self.dev_mode)
        
    def switch_screen(self, *args):
        self.manager.current = "another"
    def switch_to_dev_screen(self, *args):
        self.manager.current = "dev"

    
    def cam(self,*args):
        self.remove_widget(self.btn)
        self.remove_widget(self.btn2)
        self.camera = Camera(resolution=(640, 480))
        with self.camera.canvas.before:
             PushMatrix()
             Rotate(angle=-90,origin=self.center)
        with self.camera.canvas.after:
            PopMatrix()
        self.camera.play = True
        self.image=Image()
        self.take_picture_button = Button(text = "Take Picture",size_hint=[0.35,0.05],pos_hint={"x":0.55,"top":0.07})
        self.take_picture_button.bind(on_press = self.take_picture)
        self.switch_to_choose = Button(text = "Choose existing instead",size_hint=[0.35,0.05],pos_hint={"x":0.10,"top":0.07})
        self.switch_to_choose.bind(on_press = self.switch_screen)
        self.add_widget(self.camera)
        self.add_widget(self.take_picture_button)
        self.add_widget(self.switch_to_choose)


        
    
    def take_picture(self, *args):
        timestr = time.strftime("%Y%m%d_%H%M%S")
        self.camera.export_to_png("IMG_{}.png".format(timestr))
        self.camera.play = False
        self.remove_widget(self.camera)
        self.remove_widget(self.take_picture_button)
        self.image.source = str("IMG_{}.png".format(timestr))
        self.add_widget(self.image)
        self.confirm=Label(text = "Use this image?",pos_hint={"y":0.43})
        self.add_widget(self.confirm)
        self.use_image = Button(text = "Confirm",size_hint=[0.35,0.05],pos_hint={"x":0.55,"top":0.07})

        #bind to image processing
        self.use_image.bind(on_press = lambda *args:DeveloperScreen.image_process(self=DeveloperScreen,filename=self.image.source,isdev=False))
        self.add_widget(self.use_image)
        self.take_another = Button(text = "Retry",size_hint=[0.35,0.05],pos_hint={"x":0.10,"top":0.07})
        self.take_another.bind(on_press = self.check)
        self.add_widget(self.take_another)

        

    def check(self,*args):
            self.remove_widget(self.take_another)
            self.remove_widget(self.use_image)
            self.cam()

class DeveloperScreen(Screen,FloatLayout):
    def __init__(self, **kwargs):
        super(DeveloperScreen,self).__init__(**kwargs)
        print(self)
        print(type(self))
        self.confirm=Label(text = "Developer mode is a setting where you can see the process of how your image \nis determined whether it has Gingivitis or not",pos_hint={"y":0.43})
        self.add_widget(self.confirm)
        self.btn = Button(text ="Take a Picture",on_press = self.cam,size_hint=[0.35,0.05],pos_hint={"x":0.35,"top":0.4})
        self.add_widget(self.btn)
        self.btn2 = Button(text ="Choose Existing", on_press=self.switch_to_dev_gallery,size_hint=[0.35,0.05],pos_hint={"x":0.35,"top":0.5})
        self.add_widget(self.btn2)
        self.image = Image()

    def switch_to_dev_gallery(self, *args):
        self.manager.current = "devgall"
    
    def cam(self,*args):

        self.remove_widget(self.btn)
        self.remove_widget(self.btn2)
        self.camera = Camera(resolution=(640, 480))
        with self.camera.canvas.before:
             PushMatrix()
             Rotate(angle=-90,origin=self.center)
        with self.camera.canvas.after:
            PopMatrix()
        self.camera.play = True
        self.image=Image()
        self.take_picture_button = Button(text = "Take Picture",size_hint=[0.35,0.05],pos_hint={"x":0.55,"top":0.07})
        self.take_picture_button.bind(on_press = self.take_picture)
        self.switch_to_choose = Button(text = "Choose existing instead",size_hint=[0.35,0.05],pos_hint={"x":0.10,"top":0.07})
        self.switch_to_choose.bind(on_press = self.switch_screen)
        self.add_widget(self.camera)
        self.add_widget(self.take_picture_button)
        self.add_widget(self.switch_to_choose)

    def take_picture(self, *args):
        self.remove_widget(self.confirm)
        timestr = time.strftime("%Y%m%d_%H%M%S")
        self.camera.export_to_png("IMG_{}.png".format(timestr))
        self.camera.play = False
        self.remove_widget(self.camera)
        self.remove_widget(self.take_picture_button)
        self.image.source = str("IMG_{}.png".format(timestr))
        self.add_widget(self.image)
        self.confirm=Label(text = "Use this image?",pos_hint={"y":0.43})
        self.add_widget(self.confirm)
        self.use_image = Button(text = "Confirm",size_hint=[0.35,0.05],pos_hint={"x":0.55,"top":0.07})
        
        #bind to image processing
        self.use_image.bind(on_press = lambda *args:self.image_process(filename=self.image.source,isdev=True))
        self.add_widget(self.use_image)
        self.take_another = Button(text = "Retry",size_hint=[0.35,0.05],pos_hint={"x":0.10,"top":0.07})
        self.take_another.bind(on_press = self.check)
        self.add_widget(self.take_another)

    def switch_screen(self, *args):
        self.manager.current = "another"

class AnotherScreen(Screen):
    def __init__(self, **kwargs):
        super(AnotherScreen,self).__init__(**kwargs)
        self.gallery()

    def switch_screen(self, *args):
        self.manager.current = "main"

    def check(self,*args):
            self.remove_widget(self.take_another)
            self.remove_widget(self.image)
            self.remove_widget(self.confirm)
            self.gallery()

    def gallery(self,*args):
        self.image = Image()
        self.filechooser = FileChooserListView(size_hint=(1,0.8),pos_hint={"top":0.9})
        self.filechooser.bind(on_selection=lambda x: self.selected(self.filechooser.selection))
 
        self.open_btn = Button(text='open', size_hint=(0.35,0.05),pos_hint={"x":0.10,"top":0.07})
        self.open_btn.bind(on_release=lambda x: self.open(self.filechooser.path, self.filechooser.selection))
        self.back_to_main=Button(text='Back to main menu', size_hint=[0.35,0.05],pos_hint={"x":0.55,"top":0.07})
        self.back_to_main.bind(on_press=self.switch_screen)

        self.add_widget(self.back_to_main)
        self.add_widget(self.filechooser)
        self.add_widget(self.open_btn)
    
    def open(self, path, filename):
        self.image.source = str(filename[0])
        self.add_widget(self.image)
        self.confirm=Label(text = "Use this image?",pos_hint={"y":0.43})
        self.add_widget(self.confirm)
        self.remove_widget(self.filechooser)
        self.remove_widget(self.open_btn)
        self.remove_widget(self.back_to_main)
        self.use_image = Button(text = "Confirm",size_hint=[0.35,0.05],pos_hint={"x":0.55,"top":0.07})

        #bind to image processing
        self.use_image.bind(on_press =lambda *args: DeveloperScreen.image_process(self=DeveloperScreen,filename=self.image.source,isdev=False))
        self.add_widget(self.use_image)
        self.take_another = Button(text = "Retry",size_hint=[0.35,0.05],pos_hint={"x":0.10,"top":0.07})
        self.take_another.bind(on_press = self.check)
        self.add_widget(self.take_another)

class Main(App):
    def build(self):
        
        request_permissions([
            Permission.CAMERA,
            Permission.WRITE_EXTERNAL_STORAGE,
            Permission.READ_EXTERNAL_STORAGE
        ])
        loadingscreen.hide_loading_screen()
        self.screen_manager = ScreenManager()
        self.main_screen = MainScreen(name="main")
        self.another_screen = AnotherScreen(name="another")
        self.dev_mode_screen = DeveloperScreen(name="dev")
        self.dev_mode_gallery = DevGalleryScreen(name="devgall")
        self.screen_manager.add_widget(self.main_screen)
        self.screen_manager.add_widget(self.another_screen)
        self.screen_manager.add_widget(self.dev_mode_screen)
        self.screen_manager.add_widget(self.dev_mode_gallery)
        return self.screen_manager

if __name__ == '__main__':
    Main().run()