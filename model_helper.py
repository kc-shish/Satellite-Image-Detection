import torch
from torch import nn
from torchvision import models, transforms
from PIL import Image

trained_model = None

class_names = ['Airport',
 'BareLand',
 'BaseballField',
 'Beach',
 'Bridge',
 'Center',
 'Church',
 'Commercial',
 'DenseResidential',
 'Desert',
 'Farmland',
 'Forest',
 'Industrial',
 'Meadow',
 'MediumResidential',
 'Mountain',
 'Park',
 'Parking',
 'Playground',
 'Pond',
 'Port',
 'RailwayStation',
 'Resort',
 'River',
 'School',
 'SparseResidential',
 'Square',
 'Stadium',
 'StorageTanks',
 'Viaduct']

class satellite_img_classifier_with_Resnet(nn.Module):
    def __init__(self, num_classes, dropout_rate):
        super().__init__()

        self.model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)

        # Freeze backbone
        for param in self.model.parameters():
            param.requires_grad = False

        #Unfreeze layer4 
        for param in self.model.layer4.parameters():
            param.requires_grad = True

        # Replace FC layer (NOT classifier)
        in_features = self.model.fc.in_features
        
        self.model.fc = nn.Sequential(
           nn.Dropout(dropout_rate),
           nn.Linear(in_features, 1000),
           nn.ReLU(),
           nn.Dropout(dropout_rate),
           nn.Linear(1000, 256),
           nn.ReLU(),
           nn.Dropout(dropout_rate),
           nn.Linear(256, 128),
           nn.ReLU(),
           nn.Dropout(dropout_rate),
           nn.Linear(128, num_classes)
        )

    def forward(self, x):
        return self.model(x)
        
def predict(image_path):
    image = Image.open(image_path).convert("RGB")
    transform = transforms.Compose([
        transforms.Resize((224,224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485,0.456,0.406], std=[0.229,0.224,0.225])
        ])

    image_tensor = transform(image).unsqueeze(0) # (64, 3, 224, 224) --> (1, 3, 224, 224)
        
    global trained_model
    if trained_model is None:
        trained_model = trained_model = satellite_img_classifier_with_Resnet(num_classes=30, dropout_rate=0.38)   
        trained_model.load_state_dict(torch.load("model/saved_model_new.pth",map_location="cpu"))
        trained_model.eval()

    with torch.no_grad():
        output = trained_model(image_tensor)
        _, predicted = torch.max(output,1)
        return class_names[predicted.item()]



