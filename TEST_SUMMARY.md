# Test Suite Summary

**Status**: ✅ All 40 tests passing

## Quick Start

### Run tests from project root
```bash
python run_tests.py
```

### Run tests with verbose output  
```bash
python run_tests.py -v
```

### Run tests with coverage report
```bash
python run_tests.py --cov=node --cov-report=html
```

### Run specific test
```bash
python run_tests.py tests/test_node.py::TestTensorToBase64::test_converts_valid_tensor_to_base64 -v
```

## Test Coverage

**Total Tests:** 40 ✅

### Test Categories

1. **Image Tensor Conversion (4 tests)**
   - `TestTensorToBase64::test_converts_valid_tensor_to_base64`
   - `TestTensorToBase64::test_handles_different_dimensions`
   - `TestTensorToBase64::test_handles_value_range`
   - `TestTensorToBase64::test_handles_grayscale`

2. **API Model Fetching (4 tests)**
   - `TestFetchAvailableModels::test_fetches_models_successfully`
   - `TestFetchAvailableModels::test_returns_fallback_on_failure`
   - `TestFetchAvailableModels::test_returns_fallback_on_empty_response`
   - `TestFetchAvailableModels::test_handles_timeout`

3. **Node Configuration (8 tests)**
   - `TestImageToPromptAbacusInputTypes::test_input_types_structure`
   - `TestImageToPromptAbacusInputTypes::test_return_types`
   - `TestImageToPromptAbacusInputTypes::test_node_properties`
   - `TestImageToPromptAbacusInputTypes::test_default_values`
   - (×2 for test_node_standalone.py)

4. **Core Conversion Logic (11 tests)**
   - `TestImageToPromptAbacusConvert::test_convert_returns_string_tuple`
   - `TestImageToPromptAbacusConvert::test_convert_with_custom_instructions`
   - `TestImageToPromptAbacusConvert::test_convert_uses_correct_model`
   - `TestImageToPromptAbacusConvert::test_convert_uses_correct_api_key`
   - `TestImageToPromptAbacusConvert::test_convert_handles_api_error`
   - `TestImageToPromptAbacusConvert::test_convert_with_different_models`
   - `TestImageToPromptAbacusConvert::test_convert_processes_image_to_base64`
   - (×1 for integration, ×2 for test_node_standalone.py)

5. **Integration Tests (2 tests)**
   - `TestIntegration::test_full_pipeline` (both files)

## Installation

1. Install test dependencies:
```bash
pip install -r requirements-dev.txt
```

2. Install core dependencies (if not already installed):
```bash
pip install -r requirements.txt
```

## Test Files

- [tests/conftest.py](tests/conftest.py) - Pytest configuration and fixtures
- [tests/test_node.py](tests/test_node.py) - Main test suite (20 tests)
- [conftest.py](conftest.py) - Root conftest for pytest collection
- [pytest.ini](pytest.ini) - Pytest configuration
- [run_tests.py](run_tests.py) - Test runner script

## What's Tested

### ✅ Image Processing
- Tensor format conversions (numpy and PyTorch compatible)
- Image dimension handling (32×32, 64×64, 128×128)
- Value range conversion (float [0,1] to uint8 [0,255])
- Base64 encoding

### ✅ API Integration
- Model list fetching with fallback
- Error handling and timeouts
- API key usage
- Custom instructions passing
- Different model selection

### ✅ Node Configuration
- Input/output types structure
- Return type validation
- Node properties (function name, category, etc.)
- Default values

### ✅ Error Handling
- API failures
- Network timeouts
- Invalid responses

## Mocking Strategy

Tests use `unittest.mock` to:
- Mock external HTTP requests
- Mock OpenAI API responses
- Prevent actual API calls during testing
- Simulate error conditions

## Key Features

- **No external API calls**: All tests use mocks, safe to run offline
- **No credentials needed**: Tests don't require real API keys
- **Fast execution**: Full suite runs in ~2 seconds
- **Isolated tests**: Tests can run in any order
- **Realistic fixtures**: Uses actual ComfyUI tensor formats

## Continuous Integration

Tests can be integrated into CI/CD pipelines:

```bash
# Basic CI run
python run_tests.py --tb=short

# With coverage
python run_tests.py --cov=node --cov-report=term-missing

# JUnit XML output
python run_tests.py --junit-xml=test-results.xml
```

## Troubleshooting

### Missing dependencies
```bash
pip install -r requirements-dev.txt
pip install -r requirements.txt
```

### Tests slow to run
- First run builds pytest cache (.pytest_cache)
- Subsequent runs are faster
- Cache is safe to delete

### Import errors
- Ensure you're running from project root
- Use `python run_tests.py` instead of `pytest` directly

## Local Development

When making changes to `node.py`:
1. Run tests to verify functionality
2. Add new tests for new features
3. Keep fixtures in conftest.py
4. Use mocking for external dependencies
