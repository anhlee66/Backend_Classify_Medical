import torch
from ultralytics import YOLO

# Load the YOLO model
model_path = "databases\\models\\yolov8-cls.pt"
model = YOLO(model_path)

# Extracting training details (if available)
model_data = model.info()  # This provides a summary of the model

# Accessing metadata (if available in the state_dict or attributes)
state_dict = torch.load(model_path)
training_info = {
    "epoch": state_dict.get('epoch', 'Not available'),
    "batch_size": state_dict.get('batch_size', 'Not available'),
    "classes": state_dict.get('nc', 'Not available'),  # Number of classes
    "accuracy": state_dict.get('accuracy', 'Not available')
}

# Displaying the information
print(f"Model Summary: \n{model_data}")
print(f"Training Information: \n{training_info}")
