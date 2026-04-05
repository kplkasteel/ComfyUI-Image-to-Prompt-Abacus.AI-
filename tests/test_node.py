import sys
import pytest
import numpy as np
import base64
from unittest.mock import patch, Mock, MagicMock
from pathlib import Path
from io import BytesIO

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from node import tensor_to_base64, fetch_available_models, ImageToPromptAbacus, FALLBACK_MODELS


class TestTensorToBase64:
    """Test tensor to base64 conversion"""

    def test_converts_valid_tensor_to_base64(self, mock_image_tensor):
        """Test basic tensor to base64 conversion"""
        result = tensor_to_base64(mock_image_tensor)
        assert isinstance(result, str)
        assert len(result) > 0
        # Should be valid base64
        try:
            decoded = base64.b64decode(result)
            assert len(decoded) > 0
        except Exception as e:
            pytest.fail(f"Invalid base64 output: {e}")

    def test_handles_different_dimensions(self):
        """Test with different image dimensions"""
        for height, width in [(32, 32), (64, 64), (128, 128)]:
            tensor = np.random.rand(1, height, width, 3).astype(np.float32)
            result = tensor_to_base64(tensor)
            assert isinstance(result, str)
            assert len(result) > 0

    def test_handles_value_range(self):
        """Test that values in [0, 1] are properly converted to [0, 255]"""
        tensor = np.zeros((1, 10, 10, 3), dtype=np.float32)
        tensor[0, :, :, 0] = 1.0  # Max red
        tensor[0, :, :, 1] = 0.5  # Mid green
        tensor[0, :, :, 2] = 0.0  # Min blue
        
        result = tensor_to_base64(tensor)
        assert isinstance(result, str)
        decoded = base64.b64decode(result)
        assert len(decoded) > 0

    def test_handles_grayscale(self):
        """Test with grayscale-like image (all channels same)"""
        tensor = np.ones((1, 32, 32, 3), dtype=np.float32) * 0.5
        result = tensor_to_base64(tensor)
        assert isinstance(result, str)
        assert len(result) > 0


class TestFetchAvailableModels:
    """Test model fetching functionality"""

    @patch('node.requests.get')
    def test_fetches_models_successfully(self, mock_get, mock_models_response):
        """Test successful model fetching"""
        mock_response = Mock()
        mock_response.json.return_value = mock_models_response
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        models = fetch_available_models()
        assert models == ["gpt-4o", "gpt-4-vision-preview", "claude-3-opus"]
        mock_get.assert_called_once()

    @patch('node.requests.get')
    def test_returns_fallback_on_failure(self, mock_get):
        """Test fallback when API fails"""
        mock_get.side_effect = Exception("Connection failed")
        
        models = fetch_available_models()
        assert models == FALLBACK_MODELS

    @patch('node.requests.get')
    def test_returns_fallback_on_empty_response(self, mock_get):
        """Test fallback when response has no data"""
        mock_response = Mock()
        mock_response.json.return_value = {"data": []}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        models = fetch_available_models()
        assert models == FALLBACK_MODELS

    @patch('node.requests.get')
    def test_handles_timeout(self, mock_get):
        """Test timeout handling"""
        mock_get.side_effect = Exception("Request timeout")
        
        models = fetch_available_models()
        assert models == FALLBACK_MODELS


class TestImageToPromptAbacusInputTypes:
    """Test node input/output types configuration"""

    def test_input_types_structure(self):
        """Test INPUT_TYPES returns correct structure"""
        input_types = ImageToPromptAbacus.INPUT_TYPES()
        assert "required" in input_types
        assert "image" in input_types["required"]
        assert "instructions" in input_types["required"]
        assert "model" in input_types["required"]
        assert "api_key" in input_types["required"]

    def test_return_types(self):
        """Test node return types"""
        assert ImageToPromptAbacus.RETURN_TYPES == ("STRING",)
        assert ImageToPromptAbacus.RETURN_NAMES == ("text",)

    def test_node_properties(self):
        """Test node properties"""
        assert ImageToPromptAbacus.FUNCTION == "convert"
        assert ImageToPromptAbacus.CATEGORY == "Abacus.AI"
        assert ImageToPromptAbacus.OUTPUT_NODE == False

    def test_default_values(self):
        """Test that default values are set"""
        input_types = ImageToPromptAbacus.INPUT_TYPES()
        instructions_config = input_types["required"]["instructions"]
        assert instructions_config[1]["default"] != ""
        
        api_key_config = input_types["required"]["api_key"]
        assert api_key_config[1]["default"] == ""


class TestImageToPromptAbacusConvert:
    """Test the convert method"""

    @patch('node.OpenAI')
    def test_convert_returns_string_tuple(self, mock_openai_class, mock_image_tensor, mock_openai_response):
        """Test that convert returns a tuple with string"""
        mock_client_instance = Mock()
        mock_client_instance.chat.completions.create.return_value = mock_openai_response
        mock_openai_class.return_value = mock_client_instance

        node = ImageToPromptAbacus()
        result = node.convert(
            image=mock_image_tensor,
            instructions="Describe this image",
            model="gpt-4o",
            api_key="test-key"
        )

        assert isinstance(result, tuple)
        assert len(result) == 1
        assert isinstance(result[0], str)
        assert "detailed description" in result[0]

    @patch('node.OpenAI')
    def test_convert_with_custom_instructions(self, mock_openai_class, mock_image_tensor, mock_openai_response):
        """Test convert with custom instructions"""
        mock_client_instance = Mock()
        mock_client_instance.chat.completions.create.return_value = mock_openai_response
        mock_openai_class.return_value = mock_client_instance

        node = ImageToPromptAbacus()
        custom_instructions = "Generate a prompt for a 3D rendering engine"
        
        node.convert(
            image=mock_image_tensor,
            instructions=custom_instructions,
            model="gpt-4o",
            api_key="test-key"
        )

        # Verify the custom instructions were passed to the API
        call_args = mock_client_instance.chat.completions.create.call_args
        messages = call_args.kwargs["messages"]
        assert custom_instructions in str(messages)

    @patch('node.OpenAI')
    def test_convert_uses_correct_model(self, mock_openai_class, mock_image_tensor, mock_openai_response):
        """Test that convert uses the specified model"""
        mock_client_instance = Mock()
        mock_client_instance.chat.completions.create.return_value = mock_openai_response
        mock_openai_class.return_value = mock_client_instance

        node = ImageToPromptAbacus()
        model_name = "gpt-4-vision-preview"
        
        node.convert(
            image=mock_image_tensor,
            instructions="Test",
            model=model_name,
            api_key="test-key"
        )

        call_args = mock_client_instance.chat.completions.create.call_args
        assert call_args.kwargs["model"] == model_name

    @patch('node.OpenAI')
    def test_convert_uses_correct_api_key(self, mock_openai_class, mock_image_tensor, mock_openai_response):
        """Test that convert uses the provided API key"""
        mock_client_instance = Mock()
        mock_client_instance.chat.completions.create.return_value = mock_openai_response
        mock_openai_class.return_value = mock_client_instance
        
        node = ImageToPromptAbacus()
        test_api_key = "sk-test-123456"
        
        node.convert(
            image=mock_image_tensor,
            instructions="Test",
            model="gpt-4o",
            api_key=test_api_key
        )

        # Verify OpenAI was initialized with the correct API key
        call_args = mock_openai_class.call_args
        assert call_args.kwargs["api_key"] == test_api_key

    @patch('node.OpenAI')
    def test_convert_handles_api_error(self, mock_openai_class, mock_image_tensor):
        """Test error handling for API failures"""
        mock_client_instance = Mock()
        mock_client_instance.chat.completions.create.side_effect = Exception("API Error")
        mock_openai_class.return_value = mock_client_instance

        node = ImageToPromptAbacus()
        
        with pytest.raises(Exception):
            node.convert(
                image=mock_image_tensor,
                instructions="Test",
                model="gpt-4o",
                api_key="test-key"
            )

    @patch('node.OpenAI')
    def test_convert_with_different_models(self, mock_openai_class, mock_image_tensor, mock_openai_response):
        """Test convert with different model options"""
        mock_client_instance = Mock()
        mock_client_instance.chat.completions.create.return_value = mock_openai_response
        mock_openai_class.return_value = mock_client_instance

        node = ImageToPromptAbacus()
        
        for model in ["gpt-4o", "gpt-4-vision-preview", "claude-3-opus"]:
            result = node.convert(
                image=mock_image_tensor,
                instructions="Test",
                model=model,
                api_key="test-key"
            )
            assert isinstance(result, tuple)
            assert isinstance(result[0], str)

    @patch('node.OpenAI')
    def test_convert_processes_image_to_base64(self, mock_openai_class, mock_small_image_tensor, mock_openai_response):
        """Test that image is properly converted to base64"""
        mock_client_instance = Mock()
        mock_client_instance.chat.completions.create.return_value = mock_openai_response
        mock_openai_class.return_value = mock_client_instance

        node = ImageToPromptAbacus()
        
        node.convert(
            image=mock_small_image_tensor,
            instructions="Test",
            model="gpt-4o",
            api_key="test-key"
        )

        # Verify image was sent as base64
        call_args = mock_client_instance.chat.completions.create.call_args
        messages = call_args.kwargs["messages"]
        content = messages[0]["content"]
        
        # Check for base64 image URL
        image_content = [c for c in content if c.get("type") == "image_url"]
        assert len(image_content) > 0
        assert "data:image/png;base64," in image_content[0]["image_url"]["url"]


class TestIntegration:
    """Integration tests"""

    @patch('node.requests.get')
    @patch('node.OpenAI')
    def test_full_pipeline(self, mock_openai_class, mock_get, mock_image_tensor, mock_models_response, mock_openai_response):
        """Test complete pipeline from model fetching to conversion"""
        # Mock model fetching
        mock_response = Mock()
        mock_response.json.return_value = mock_models_response
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        # Mock OpenAI response
        mock_client_instance = Mock()
        mock_client_instance.chat.completions.create.return_value = mock_openai_response
        mock_openai_class.return_value = mock_client_instance

        # Get available models
        models = fetch_available_models()
        assert len(models) > 0

        # Use first model
        node = ImageToPromptAbacus()
        result = node.convert(
            image=mock_image_tensor,
            instructions="Test",
            model=models[0],
            api_key="test-key"
        )

        assert isinstance(result, tuple)
        assert isinstance(result[0], str)
