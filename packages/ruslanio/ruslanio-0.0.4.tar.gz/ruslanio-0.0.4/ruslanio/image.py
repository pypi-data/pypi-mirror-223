from pathlib import Path
import numpy as np
import cv2


def imread(path: Path | str) -> np.ndarray:
    img = cv2.imread(str(path))
    assert img is not None, f'Cannot read from {path}'
    return img[:, :, ::-1].copy()
