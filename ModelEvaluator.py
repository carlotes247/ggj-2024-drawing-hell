import torch
import pygame as pg
import numpy as np
import matplotlib.pyplot as plt
from torchvision import datasets
from torchvision.transforms import ToTensor
from torchvision import transforms
import torch.nn.functional as F # for downscaling an image

#region Constants

# Classes in dataset
classes = [
    "T-shirt/top",
    "Trouser",
    "Pullover",
    "Dress",
    "Coat",
    "Sandal",
    "Shirt",
    "Sneaker",
    "Bag",
    "Ankle boot",
]

#endregion

#region Variables

# Download test data from open datasets.
test_data = datasets.FashionMNIST(
    root="data",
    train=False,
    download=True,
    transform=ToTensor(),
)

#endregion

#region Methods

def EvaluateModel(model, device, classes, test_data):
    # set model in eval mode
    model.eval()
    x, y = test_data[0][0], test_data[0][1]
    with torch.no_grad():
        x = x.to(device)
        pred = model(x)
        predicted, actual = classes[pred[0].argmax(0)], classes[y]
        print(f'Predicted: "{predicted}", Actual: "{actual}"')

def Classify(model, device, classes, test_data, imageToClassify):
    # set model in eval mode
    model.eval()
    x, y = test_data[0][0], test_data[0][1]
    myImg = pg.surfarray.pixels3d(imageToClassify)
    nonNegativeImg = myImg.copy()
    tensorImg = torch.tensor(nonNegativeImg)
    tensorImg = tensorImg.permute((1, 0 , 2))
    
    # Greyscaling the image
    # The weights for each channel when summing to get grayscale image
    # These weights are standard for RGB to grayscale conversion
    weights = torch.tensor([0.2989, 0.5870, 0.1140]).view(3, 1, 1)
    # Use torch.sum to sum the weighted channels
    tensorImgColourChannelFirst = tensorImg.permute(2, 0, 1)
    grayscale_img = torch.sum(weights * tensorImgColourChannelFirst, dim=0, keepdim=True)
    
    # Normalize the image tensor
    normalized_img = (grayscale_img - grayscale_img.min()) / (grayscale_img.max() - grayscale_img.min())

    # Invert the colors by subtracting the image tensor from 1
    inverted_img = 1 - normalized_img
    # Square image by filling in the borders
    square_img = fill_borders(inverted_img)
    #plt.imshow(square_img.squeeze(), cmap="gray")    

    # Create a transform
    resize = transforms.Resize((28,28))
    # Apply the transform to the image tensor
    downscaled_img = resize(square_img)

    plt.imshow(downscaled_img.squeeze(), cmap="gray")    
    #plt.imshow(x.squeeze(), cmap="gray")
    #plt.show()
    with torch.no_grad():
        #x = x.to(device)
        downscaled_img = downscaled_img.to(device)
        #pred = model(x)
        pred = model(downscaled_img)
        predicted = classes[pred[0].argmax(0)]
        print(f'Predicted: "{predicted}"')
    return predicted


def fill_borders(img_tensor):
    # Get the shape of the tensor
    c, h, w = img_tensor.shape

    # Calculate the maximum dimension
    max_dim = max(h, w)

    # Create a black tensor of size (c, max_dim, max_dim)
    black_tensor = torch.zeros((c, max_dim, max_dim))

    # Calculate the start indices for height and width
    start_h = (max_dim - h) // 2
    start_w = (max_dim - w) // 2

    # Fill the black tensor with the image tensor
    black_tensor[:, start_h:start_h+h, start_w:start_w+w] = img_tensor

    return black_tensor
#endregion
        