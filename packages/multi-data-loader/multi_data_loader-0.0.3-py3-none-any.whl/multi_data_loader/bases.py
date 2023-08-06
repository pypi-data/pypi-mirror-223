
class ObjectDetector(object):

    def predict(self, *args, **kwargs):
        raise NotImplementedError

    def destroy_model(self, *args, **kwargs):
        pass

class DataLoader(object):
    def __init__(self, images: list, mode: str) -> None:
        self.images = images
        self.img_size = len(images)
        self.mode = mode
        self.type = None

    def __len__(self):
        return self.img_size

    def __iter__(self):
        self.count = 0
        return self

    def __next__(self):
        raise NotImplementedError

    def release(self):
        self.images = None
        self.img_size = None
        self.mode = None
