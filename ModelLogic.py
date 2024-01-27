import torch
from ModelTorch import *
from ModelLoader import *
from ModelEvaluator import *

#region Variables

batch_size=64

# Get cpu, gpu or mps device for training.
device = (
    "cuda"
    if torch.cuda.is_available()
    else "mps"
    if torch.backends.mps.is_available()
    else "cpu"
)

#endregion

#region Main

# Load model
model = LoadModel(device, "model.pth")

# Evaluate model
EvaluateModel(model, device, classes, test_data)

#endregion