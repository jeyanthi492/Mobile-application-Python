__version__ = '1.0'

import kivy
from camera import AndroidCamera
from android.permissions import request_permissions, Permission
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, StringProperty
import base64

class MyCamera(AndroidCamera):
    pass

class BoxLayoutW(BoxLayout):
    my_camera = ObjectProperty(None)
    image_path = StringProperty('/sdcard/my_test_photo.png')

    def __init__(self, **kwargs):
        super(BoxLayoutW, self).__init__()
        self.my_camera = MyCamera()

    def take_shot(self):
        self.my_camera._take_picture(self.on_success_shot, self.image_path)

    def on_success_shot(self, loaded_image_path):
        image_str = self.image_convert_base64()
        return True

    def image_convert_base64(self):
        try:
            with open(self.image_path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read())
            return encoded_string.decode('utf-8')
        except Exception as e:
            print(f"Error converting image to base64: {e}")
            return ''

if __name__ == '__main__':
    request_permissions([
        Permission.CAMERA,
        Permission.WRITE_EXTERNAL_STORAGE,
        Permission.READ_EXTERNAL_STORAGE
    ])

    class CameraApp(App):
        def build(self):
            main_window = BoxLayoutW()
            return main_window

    CameraApp().run()
