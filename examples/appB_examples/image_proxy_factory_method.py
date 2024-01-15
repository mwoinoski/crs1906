from PIL import Image as PILImage, ImageTk as PILImageTk
import tkinter as tk
import sys
from abc import ABC, abstractmethod


class Image(ABC):
    @abstractmethod
    def get_content(self, path):
        pass


class ConcreteImage(Image):
    def __init__(self, path):
        print('ConcreteImage.__init__("{}")'.format(path))
        # load image immediately
        pil_image = PILImage.open(path)
        self.image_content = PILImageTk.PhotoImage(pil_image) 
        
    def get_content(self):
        return self.image_content

    def __repr__(self):
        return 'ConcreteImage("{}")'.format(self.path)


class LazyLoadingImage(Image):
    def __init__(self, path):  # don't load image yet
        print('LazyLoadingImage.__init__("{}")'.format(path))
        self.path = path
        self.concrete_image = None
        
    def get_content(self):  
        # delegate image loaded to ConcreteImage
        if not self.concrete_image:
            self.concrete_image = ConcreteImage(self.path) # loads image
        return self.concrete_image.get_content()  

    def __repr__(self):
        return 'LazyLoadingImage("{}")'.format(self.path)


class ImageClient:
    root = tk.Tk()
    
    def __init__(self, image):
        print('ImageClient.__init__({})'.format(image))
        self.image = image
        
    def display_image(self):
        content = self.image.get_content()  # proxy now loads image content
        label = tk.Label(ImageClient.root, image=content, bg='white')
        label.pack(padx=5, pady=5)
        ImageClient.root.mainloop()

    def __repr__(self):
        return 'ImageClient({})'.format(self.image)


class ObjectFactory:
    class_map = {}
    
    @classmethod
    def register(cls, type, replacement_type):
        cls.class_map[type] = replacement_type
    
    @classmethod
    def get_instance(cls, type, *args, **kwargs):
        returned_type = cls.class_map.get(type, type)
        return returned_type(*args, **kwargs)


def main(show_it):
    ObjectFactory.register(ConcreteImage, LazyLoadingImage)

    print('Getting instance of ConcreteImage')    
    image = ObjectFactory.get_instance(ConcreteImage,
                                      'LargeMagellanicCloud.jpg')
    
    print('Getting instance of ImageClient')    
    client = ObjectFactory.get_instance(ImageClient, image)

    if show_it:
        client.display_image()


if __name__ == '__main__':
    main(len(sys.argv) > 1 and sys.argv[1] == '--display-image')
