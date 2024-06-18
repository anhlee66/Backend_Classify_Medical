from ultralytics.models import YOLO
import torch
def check():
    print(torch.cuda.is_available())
    print(torch.version.cuda)
    print(torch.backends.cudnn.version)
def train():
    model = YOLO("databases\\models\\best10.pt")
    dataset = "E:/Development/Intern/Dataset/Dermatology"
    model.train(data=dataset, imgsz=224, epochs=10, batch=32, workers=8,)

if __name__ == "__main__":
    train()
    # check()