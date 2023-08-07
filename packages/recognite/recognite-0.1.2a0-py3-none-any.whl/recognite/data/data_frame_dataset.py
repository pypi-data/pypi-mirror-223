from typing import Dict, Callable, Optional

import pandas as pd
from PIL import Image
from torch.utils.data import Dataset


class DataFrameDataset(Dataset):
    """A dataset based on a pandas DataFrame.

    The provided DataFrame contains the path of each image and the
    corresponding label.

    Args:
        df: The DataFrame containing the image paths and labels.
        label_key: The column in the DataFrame that contains the label of each
            image.
        image_key: The column in the DataFrame that contains the image path of
            each image.
        label_to_int: A dictionary that maps the label to a unique integer.
        transform: A transform to apply to the image before returning it.

    Attributes:
        df: The DataFrame with the image paths and labels.
        label_key: The column in the DataFrame that contains the label of each
            image.
        image_key: The column in the DataFrame that contains the image path of
            each image.
        label_to_int: The dictionary that maps the label to a unique integer.
        transform: The transform applied to each image before returning it.
        unique_labels: The unique labels present in this dataset.
    """
    def __init__(
        self,
        df: pd.DataFrame,
        label_key: str,
        image_key: str,
        label_to_int: Dict[str, int],
        transform: Optional[Callable] = None,
    ):
        self.df = df
        self.transform = transform
        self.label_key = label_key
        self.image_key = image_key
        self.label_to_int = label_to_int
        self.unique_labels = set(self.label_to_int.keys())

    def __len__(self):
        return len(self.df)

    def __getitem__(self, idx):
        row = self.df.iloc[idx]
        im = Image.open(row[self.image_key])
        label = self.label_to_int[row[self.label_key]]

        if self.transform is not None:
            im = self.transform(im)

        return im, label
