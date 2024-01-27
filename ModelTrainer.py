import torch
from torch import nn
from torch.utils.data import DataLoader
from torchvision import datasets
from torchvision.transforms import ToTensor
from ModelTorch import *

#region Variables

# Get cpu, gpu or mps device for training.
device = (
    "cuda"
    if torch.cuda.is_available()
    else "mps"
    if torch.backends.mps.is_available()
    else "cpu"
)

# Download training data from open datasets.
training_data = datasets.FashionMNIST(
    root="data",
    train=True,
    download=True,
    transform=ToTensor(),
)

# Download test data from open datasets.
test_data = datasets.FashionMNIST(
    root="data",
    train=False,
    download=True,
    transform=ToTensor(),
)

# How big the batch size
batch_size = 64
# Training epochs
epochs = 30

# Debug flags
debugCode = True;
debugEpochs = False;
debugAccuracy = True;
allowTraining = True;

#endregion

#region Methods



#endregion

#region Main 
        
# Create data loaders.
if (allowTraining):
    train_dataloader = DataLoader(training_data, batch_size=batch_size)
test_dataloader = DataLoader(test_data, batch_size=batch_size)
    
if (debugCode):
    print(f"Using {device} device")

if (debugCode):
    for X, y in test_dataloader:
        print(f"Shape of X [N, C, H, W]: {X.shape}")
        print(f"Shape of y: {y.shape} {y.dtype}")
        break

# Set NN in device
model = NeuralNetwork().to(device)
if (debugCode):
    print(model)

# set loss function and optimizer (stochastic gradient descent)
loss_fn = nn.CrossEntropyLoss()
optimizer = torch.optim.SGD(model.parameters(), lr=1e-3)

if (allowTraining):
    for t in range(epochs):
        if (debugEpochs):
            print(f"Epoch {t+1}\n-------------------------------")
        train(train_dataloader, model, loss_fn, optimizer, device, debugEpochs=debugEpochs)
        test(test_dataloader, model, loss_fn, device, debugAccuracy=debugAccuracy)
    print("Done!")
    # saving model after training
    torch.save(model.state_dict(), "model.pth")
    print("Saved PyTorch Model State to model.pth")



#endregion