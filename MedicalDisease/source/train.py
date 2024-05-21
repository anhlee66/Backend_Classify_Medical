from ultralytics.models import YOLO

data  = "E:\Development\Intern\Backend_Classify_Medical\MedicalDisease\source\data.yaml"
model = YOLO("yolov8-cls.pt")
model.train(task='classify',mode='train',data='datasets/medical',imgsz=480, epochs=10, batch=8)