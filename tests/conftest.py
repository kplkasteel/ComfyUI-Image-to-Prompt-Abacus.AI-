import sys
import pytest
import numpy as np
from unittest.mock import Mock, MagicMock
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))


class MockTensor:
    """Wraps a numpy array to mimic a PyTorch tensor with .cpu().numpy() support."""

    def __init__(self, array: np.ndarray):
        self._array = array

    def __getitem__(self, idx):
        return MockTensor(self._array[idx])

    def cpu(self):
        return self

    def numpy(self):
        return self._array


@pytest.fixture
def mock_image_tensor():
    """Create a mock image tensor in ComfyUI format: [B, H, W, C] float32 [0, 1]"""
    array = np.ones((1, 64, 64, 3), dtype=np.float32)
    array[0, :, :, 0] = 1.0
    array[0, :, :, 1] = 0.0
    array[0, :, :, 2] = 0.0
    return MockTensor(array)


@pytest.fixture
def mock_small_image_tensor():
    """Create a small test image tensor for quick tests"""
    array = np.random.rand(1, 32, 32, 3).astype(np.float32)
    return MockTensor(array)


@pytest.fixture
def mock_openai_response():
    """Create a mock OpenAI API response"""
    mock_response = Mock()
    mock_response.choices = [Mock()]
    mock_response.choices[0].message = Mock()
    mock_response.choices[0].message.content = "A detailed description of the image as a Stable Diffusion prompt."
    return mock_response


@pytest.fixture
def mock_models_response():
    """Create a mock API response for fetching models"""
    return {
        "data": [
            {"id": "gpt-4o"},
            {"id": "gpt-4-vision-preview"},
            {"id": "claude-3-opus"}
        ]
    }
