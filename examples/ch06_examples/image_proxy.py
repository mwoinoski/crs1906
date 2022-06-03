from PIL import Image as PILImage, ImageTk as PILImageTk
import tkinter as tk
import sys
from abc import ABCMeta, abstractmethod


class Image(metaclass=ABCMeta):
    def __init__(self, path):
        self.path = path

    @abstractmethod
    def get_content(self):
        """Loads the image from the given path"""


class ConcreteImage(Image):
    def __init__(self, path):
        print(f'ConcreteImage.__init__("{path}")')
        super().__init__(path)
        # load image immediately
        pil_image = PILImage.open(path)
        self.image_content = PILImageTk.PhotoImage(pil_image) 
        
    def get_content(self):
        return self.image_content

    def __repr__(self):
        return f'ConcreteImage("{self.path}")'


class LazyLoadingImage(Image):
    def __init__(self, path):  # don't load image yet
        print(f'LazyLoadingImage.__init__("{path}")')
        super().__init__(path)
        self.concrete_image = None
        
    def get_content(self):  
        # delegate image loaded to ConcreteImage
        if not self.concrete_image:
            self.concrete_image = ConcreteImage(self.path)  # loads image
        return self.concrete_image.get_content()  

    def __repr__(self):
        return f'LazyLoadingImage("{self.path}")'


class ImageClient:
    root = tk.Tk()
    
    def __init__(self, image):
        print(f'ImageClient.__init__({image})')
        self.image = image
        
    def display_image(self):
        content = self.image.get_content()  # proxy now loads image content
        label = tk.Label(ImageClient.root, image=content, bg='white')
        label.pack(padx=5, pady=5)
        ImageClient.root.mainloop()

    def __repr__(self):
        return f'ImageClient({self.image})'


def main():
    proxy = LazyLoadingImage('LargeMagellanicCloud.jpg')
    client = ImageClient(proxy)

    if len(sys.argv) > 1 and sys.argv[1] == '--display-image':
        client.display_image()

    # better: use the standard argparse module to handle command-line arguments


if __name__ == '__main__':
    main()
