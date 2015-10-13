"""
thumbnail_image_list.py - Example of custom indexing from Chapter 1
"""


class Image:
    def __init__(self, path):
        self.path = path
        self.thumbnail = 'thumbnail for ' + path

    @property
    def full_size(self):
        return 'full size image for ' + self.path


class ImageList:
    def __init__(self, images):
        self.images = images
        self.index = -1

    def __iter__(self):
        return self

    def __next__(self):
        self.index += 1
        if self.index >= len(self.images):
            raise StopIteration
        return self.images[self.index].thumbnail

    def __getitem__(self, index):
        return self.images[index].full_size

paths = 'image1', 'image2', 'image3'
image_list = ImageList([Image(p) for p in paths])

for image in image_list:
    print(image)  # prints 'thumbnail for imageN'

print(image_list[1])  # prints 'full size image for image2'
