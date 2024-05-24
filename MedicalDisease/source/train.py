from ultralytics.models import YOLO
if __name__ == '__main__':
    model = YOLO('yolov8n-cls.pt')

    model.train(data='datasets/medical6',imgsz=480, epochs=10, batch=16,workers=6)