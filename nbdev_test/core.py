"""Fill in a module description here"""

# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/00_core.ipynb.

# %% auto 0
__all__ = ['stdout_handler', 'formatter', 'root_logger', 'logger', 'force_log_output', 'ImageDataset', 'MNISTDataset', 'foo']

# %% ../nbs/00_core.ipynb 3
import torch
import torchvision
from torchvision.datasets import MNIST
from torchvision.transforms import transforms
from torch.utils.data import DataLoader, random_split, Dataset

from typing import List, Tuple, Union, Optional
import os
import logging
import sys

# logging.basicConfig(
#     level=logging.DEBUG,
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#     handlers=[
#         logging.StreamHandler(sys.stdout)  # Explicitly use stdout
#     ]
# )

# Create a custom handler that writes to stdout
stdout_handler = logging.StreamHandler(sys.stderr)
stdout_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
stdout_handler.setFormatter(formatter)

# Get the root logger and add the handler
root_logger = logging.getLogger()
root_logger.handlers.clear() 
root_logger.setLevel(logging.DEBUG)
root_logger.addHandler(stdout_handler)

# Now add handlers to your specific logger
logger = logging.getLogger(__name__)
root_logger.handlers.clear() 
logger.addHandler(stdout_handler)
logger.setLevel(logging.DEBUG)

# %% ../nbs/00_core.ipynb 4
# Create a diagnostic function that writes to multiple outputs
def force_log_output(message, level=logging.INFO):
    # Write to a file
    log_file = os.path.join(os.getcwd(), 'nbdev_diagnostic_log.txt')
    with open(log_file, 'a') as f:
        f.write(f"{level}: {message}\n")
    
    # Write to stdout
    print(f"FORCE_LOG: {message}")
    
    # Use standard logging
    logger = logging.getLogger(__name__)
    logger.log(level, message)

# Example usage
force_log_output("This is a diagnostic message")
force_log_output("This is a warning message", logging.WARNING)

# %% ../nbs/00_core.ipynb 5
class ImageDataset(Dataset):
    " Base class for image datasets providing visualization of (image, label) samples"

    def __init__(self):
        logger.info("ImageDataset: init")
        print("##### ImageDataset: init")
        super().__init__()

    def show_idx(self,
            index:int # Index of the (image,label) sample to visualize
        ):
        "display image from data point index of a image dataset"
        X, y = self.__getitem__(index)
        plt.figure(figsize = (1, 1))
        plt.imshow(X.numpy().reshape(28,28),cmap='gray')
        plt.title(f"Label: {int(y)}")
        plt.show()

    @staticmethod
    def show_grid(
            imgs: List[torch.Tensor], # python list of images dim (C,H,W)
            save_path=None, # path where image can be saved
            dims:Tuple[int,int] = (28,28)
        ):
        "display list of mnist-like images (C,H,W)"
        if not isinstance(imgs, list):
            imgs = [imgs]
        fig, axs = plt.subplots(ncols=len(imgs), squeeze=False)
        for i, img in enumerate(imgs):
            img = img.detach()
            axs[0, i].imshow(img.numpy().reshape(dims[0],dims[1]))
            axs[0, i].set(xticklabels=[], yticklabels=[], xticks=[], yticks=[])
        if save_path:
            plt.savefig(save_path)

    def show_random(
            self,
            n:int=3, # number of images to display
            dims:Tuple[int,int] = (28,28)
        ):
        "display grid of random images"
        indices = torch.randint(0,len(self), (n,))
        images = []
        for index in indices:
            X, y = self.__getitem__(index)
            X = X.reshape(dims[0],dims[1])
            images.append(X)
        self.show_grid(images)
        

# %% ../nbs/00_core.ipynb 6
class MNISTDataset(ImageDataset):
    "MNIST digit dataset"

    def __init__(
        self,
        data_dir:str='../data/image', # path where data is saved
        train:bool = True, # train or test dataset
        transform:torchvision.transforms.transforms=transforms.Compose([
                transforms.ToTensor(),
                transforms.Normalize((0.1307,), (0.3081,))
            ])
        # TODO: add noramlization?
        # torchvision.transforms.Compose([torchvision.transforms.ToTensor(), torchvision.transforms.Normalize(0.1307,), (0.3081,))])

    ):
        os.makedirs(data_dir, exist_ok=True)
        super().__init__()
        logger.info("MNISTDataset: init")
        try:
            self.ds = MNIST(
                data_dir,
                train = train,
                transform=transform, 
                download=True
            )
        except Exception as e:
            logger.error(f"Error loading MNIST dataset: {e}")


    def __len__(self) -> int: # length of dataset
        return len(self.ds)
    
    def __getitem__(self, idx # index into the dataset
                    ) -> tuple[torch.FloatTensor, int]: # Y image data, x digit number
        x = self.ds[idx][0]
        y = self.ds[idx][1]
        return x, y
    
    def train_dev_split(
            self,
            ratio:float, # percentage of train/dev split,
        ) -> tuple[torchvision.datasets.MNIST, torchvision.datasets.MNIST]: # train and set mnnist datasets

        train_set_size = int(len(self.ds) * ratio)
        valid_set_size = len(self.ds) - train_set_size

        # split the train set into two
        train_set, valid_set = data.random_split(self.ds, [train_set_size, valid_set_size])
        # TODO: cast to ImageDataset to allow for drawing
        # train_set, valid_set = Dataset(train_set),j Dataset(valid_set)
        return train_set, valid_set



# %% ../nbs/00_core.ipynb 9
def foo(): pass
