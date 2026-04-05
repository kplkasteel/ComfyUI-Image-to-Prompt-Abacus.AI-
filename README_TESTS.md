# Image to Prompt Tests

This directory contains comprehensive tests for the Image to Prompt (Abacus.AI) node.

## Setup

### Install test dependencies:
```bash
pip install -r requirements-dev.txt
```

## Running Tests

### Run all tests:
```bash
pytest
```

### Run with verbose output:
```bash
pytest -v
```

### Run with coverage report:
```bash
pytest --cov=./node --cov-report=html
```

### Run specific test class:
```bash
pytest tests/test_node.py::TestTensorToBase64
```

### Run specific test:
```bash
pytest tests/test_node.py::TestImageToPromptAbacusConvert::test_convert_returns_string_tuple
```

### Run with markers:
```bash
pytest -m unit
pytest -m integration
```

## Test Coverage

The test suite includes:

- **TestTensorToBase64**: Tests for image tensor to base64 conversion
  - Valid tensor conversion
  - Different image dimensions (32x32, 64x64, 128x128)
  - Value range handling (float [0, 1] to uint8 [0, 255])
  - Grayscale image handling

- **TestFetchAvailableModels**: Tests for API model fetching
  - Successful model fetching
  - Fallback on network failure
  - Empty response handling
  - Timeout handling

- **TestImageToPromptAbacusInputTypes**: Tests for node configuration
  - Input types structure validation
  - Return types validation
  - Node properties validation
  - Default values validation

- **TestImageToPromptAbacusConvert**: Tests for the main convert method
  - Returns correct tuple format
  - Custom instructions are passed to API
  - Correct model selection
  - API key usage
  - Error handling
  - Different model options
  - Image to base64 processing

- **TestIntegration**: End-to-end pipeline tests
  - Full pipeline from model fetching to conversion

## Fixtures

Located in `conftest.py`:

- `mock_image_tensor`: 64x64 RGB image tensor in ComfyUI format
- `mock_small_image_tensor`: 32x32 random image for quick tests
- `mock_openai_response`: Mock OpenAI API response
- `mock_models_response`: Mock model list API response

## Mocking

Tests use `unittest.mock` to mock:
- External API calls (requests, OpenAI)
- Preventing actual API calls during testing
- Allowing controlled testing of error scenarios

## Notes

- Tests use mocking to avoid external API calls
- No real API keys are used
- All tests are isolated and can run in any order
- Test data uses realistic ComfyUI tensor formats
