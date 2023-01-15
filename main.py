from kivy.app import App
from kivy.uix.camera import Camera
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.filechooser import FileChooserIconView

class GalleryApp(App):
    def build(self):
        self.choose_image_button = Button(text="Choose Image", on_press=self.open_gallery)
        self.image = Image()
        return self.choose_image_button
    
    def open_gallery(self, *args):
        file_chooser = FileChooserIconView()
        file_chooser.bind(on_submit=self.load_image)
        file_chooser.open()
    
    def load_image(self, *args):
        self.image.source = args[1][0]
        self.remove_widget(self.choose_image_button)
        self.add_widget(self.image)

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Button(text='Go to Another screen', on_press=self.switch_screen))
    def switch_screen(self, *args):
        self.manager.current = "another"

class AnotherScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Button(text='Go to Main screen', on_press=self.switch_screen))
    def switch_screen(self, *args):
        self.manager.current = "main"

class ScreenManagementApp(App):
    def build(self):
        self.screen_manager = ScreenManager()
        self.main_screen = MainScreen(name="main")
        self.another_screen = AnotherScreen(name="another")
        self.screen_manager.add_widget(self.main_screen)
        self.screen_manager.add_widget(self.another_screen)
        return self.screen_manager

class TakePictureApp(App):
    def build(self):
        self.camera = Camera(resolution=(640, 480))
        self.camera.play = True
        self.take_picture_button = Button(text = "Take Picture")
        self.take_picture_button.bind(on_press = self.take_picture)
        return self.camera
    
    def take_picture(self, *args):
        self.camera.export_to_png("picture.png")

class Main(App):
    def build(self):
        return Grid()

class Grid(GridLayout):
    def __init__(self,**kwargs):
        super(Grid,self).__init__(**kwargs)
        self.rows=2
        self.btn = Button(text ="Take a Picture")
        self.add_widget(self.btn)
        #self.btn.bind(on_press = TakePictureApp().build())
        self.btn2 = Button(text ="Choose Existing")
        self.add_widget(self.btn2)



if __name__ == '__main__':
    Main().run()