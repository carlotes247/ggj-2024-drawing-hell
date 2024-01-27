import torch
from ModelTorch import NeuralNetwork

#region Methods

def LoadModel(device, path):
    # Load model to test
    model = NeuralNetwork().to(device)
    model.load_state_dict(torch.load(path))
    return model

#endregion
        