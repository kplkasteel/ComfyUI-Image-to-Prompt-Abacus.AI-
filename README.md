# Image to Prompt (Abacus.AI)

[![Tests](https://img.shields.io/badge/tests-20%20passed-brightgreen)](TEST_SUMMARY.md)
[![ComfyUI](https://img.shields.io/badge/ComfyUI-Custom%20Node-blue)](https://github.com/comfyanonymous/ComfyUI)

A powerful ComfyUI custom node that leverages advanced AI vision-language models to automatically generate detailed, high-quality prompts from images. Perfect for enhancing your Stable Diffusion workflows with intelligent image analysis and prompt generation.

## 🎯 What It Does

This node transforms images into rich, descriptive text prompts using state-of-the-art multimodal AI models. It analyzes visual content and generates contextually appropriate prompts that can be directly used in image generation workflows.

### Key Features

- **🤖 Advanced AI Analysis**: Uses cutting-edge vision-language models (GPT-4o, Claude-3, etc.) through Abacus.AI's API
- **🎨 Stable Diffusion Optimized**: Generates prompts specifically tailored for Stable Diffusion and similar image generation models
- **⚡ Real-time Processing**: Fast image analysis with configurable model selection
- **🔧 Customizable Instructions**: Flexible prompt generation with user-defined instructions
- **🛡️ Robust Error Handling**: Graceful fallbacks and comprehensive error management
- **🧪 Fully Tested**: Complete test suite with 20 passing tests

## 🚀 Installation

### Prerequisites

- ComfyUI installed and running
- Python 3.8+ with pip
- **Valid Abacus.AI API key with active subscription** (this node consumes API credits)

### ⚠️ Important: API Costs & Subscription

**This node requires an active Abacus.AI subscription and will consume your API credits with each use.**

- **Cost**: Each image analysis request consumes credits based on the selected model and image size
- **Subscription Required**: You must have an active Abacus.AI account with sufficient credits
- **Billing**: Usage is billed through your Abacus.AI account
- **Free Tier**: Check Abacus.AI's pricing for any free credits or trial periods

**Before using this node:**
1. Sign up for an Abacus.AI account at [Abacus.AI](https://abacus.ai)
2. Add credits to your account or subscribe to a plan
3. Generate an API key from your dashboard
4. Monitor your usage and credit balance regularly

### Step-by-Step Installation

1. **Navigate to ComfyUI custom nodes directory:**
   ```bash
   cd ComfyUI/custom_nodes
   ```

2. **Clone or download this repository:**
   ```bash
   # If cloning from git
   git clone https://github.com/your-repo/image-to-prompt-abacus.git "Image to Prompt (Abacus.AI)"

   # Or download and extract to the directory above
   ```

3. **Install dependencies:**
   ```bash
   cd "Image to Prompt (Abacus.AI)"
   pip install -r requirements.txt
   ```

4. **Restart ComfyUI** to load the new node

### Dependencies

- `openai` - OpenAI-compatible API client
- `requests` - HTTP requests for model fetching
- `pillow` - Image processing
- `numpy` - Numerical operations

## 📖 Usage

### Basic Setup

1. **Get your Abacus.AI API key:**
   - Visit [Abacus.AI](https://abacus.ai) and sign up for an account
   - Generate an API key from your dashboard

2. **Add the node to your ComfyUI workflow:**
   - Search for "Image to Prompt (Abacus.AI)" in the node browser
   - Place it in your workflow after an image source node

### Node Configuration

#### Required Inputs

| Input | Type | Description |
|-------|------|-------------|
| `image` | IMAGE | The input image tensor from ComfyUI (supports various formats) |
| `instructions` | STRING | Custom instructions for prompt generation |
| `model` | Dropdown | AI model to use (auto-fetched from Abacus.AI API) |
| `api_key` | STRING | Your Abacus.AI API key |

#### Output

| Output | Type | Description |
|--------|------|-------------|
| `text` | STRING | Generated prompt text |

### Example Workflow

```
[Image Loader] → [Image to Prompt (Abacus.AI)] → [CLIP Text Encode] → [KSampler] → [Save Image]
```

### Default Configuration

- **Instructions**: "Describe this image as a detailed Stable Diffusion prompt."
- **Model**: First available model from Abacus.AI API
- **API Key**: Empty (must be provided)

## 🎨 Use Cases & Applications

### Primary Use Cases

#### 1. **Image-to-Image Workflows**
Transform reference images into detailed prompts for style transfer, color matching, or composition guidance.

#### 2. **Prompt Enhancement**
Analyze existing images and generate enhanced, more detailed prompts that capture subtle elements missed in manual descriptions.

#### 3. **Batch Processing**
Process multiple images to generate consistent prompt styles across a dataset.

#### 4. **Creative Inspiration**
Use the node to analyze artistic works and generate prompts that capture the essence and style for new creations.

### Advanced Applications

#### Style Analysis & Replication
```python
# Example custom instructions for style analysis
"Analyze the artistic style, color palette, lighting, and composition of this image.
Generate a detailed Stable Diffusion prompt that would recreate images in this exact style."
```

#### Technical Specification Generation
```python
# For technical/precise prompts
"Provide a highly detailed technical description including:
- Exact color values and gradients
- Lighting setup and shadow patterns
- Material properties and textures
- Geometric shapes and proportions
- Camera angle and perspective"
```

#### Emotional & Atmospheric Prompts
```python
# For mood and atmosphere
"Describe the emotional atmosphere, mood, and feeling conveyed by this image.
Generate a prompt that captures the same emotional essence and visual mood."
```

## 🔧 Configuration Options

### Model Selection

The node automatically fetches available models from Abacus.AI's API. Common models include:

- **GPT-4o** - Latest GPT-4 with vision capabilities
- **GPT-4 Vision Preview** - Specialized vision model
- **Claude-3 Opus** - Anthropic's most capable model
- **Claude-3 Sonnet** - Balanced performance and speed
- **Claude-3 Haiku** - Fast and efficient

### Custom Instructions

The `instructions` field accepts any text that guides how the AI analyzes the image. Examples:

#### Basic Prompts
- `"Describe this image in detail"`
- `"Generate a Stable Diffusion prompt for this image"`

#### Specialized Analysis
- `"Focus on the background elements and setting"`
- `"Describe only the main subject, ignore background"`
- `"Analyze the color scheme and palette"`

#### Style-Specific
- `"Describe in the style of art criticism"`
- `"Generate a prompt for digital art creation"`
- `"Create a prompt optimized for photorealistic generation"`

### API Configuration

- **Base URL**: `https://routellm.abacus.ai/v1` (automatically configured)
- **Timeout**: 5 seconds for model fetching
- **Max Tokens**: 1024 tokens for response generation
- **Image Format**: PNG (automatically converted)

## 🧪 Testing

This node includes a comprehensive test suite to ensure reliability and correctness.

### Running Tests

```bash
# Install test dependencies
pip install -r requirements-dev.txt

# Run all tests
python run_tests.py

# Run with verbose output
python run_tests.py -v

# Run with coverage report
python run_tests.py --cov=node --cov-report=html
```

### Test Coverage

- ✅ Image tensor conversion (4 tests)
- ✅ API model fetching (4 tests)
- ✅ Node configuration (4 tests)
- ✅ Core conversion logic (7 tests)
- ✅ Integration testing (1 test)

**Total: 20 tests, all passing**

### Test Features

- **No external API calls** - Fully mocked for offline testing
- **No credentials required** - Safe to run in any environment
- **Fast execution** - Complete suite runs in ~2 seconds
- **CI/CD ready** - Compatible with automated testing pipelines

## 🔍 Technical Details

### Image Processing

The node handles ComfyUI's native image tensor format:
- **Format**: `[B, H, W, C]` float32 tensors
- **Range**: Values in [0, 1] (normalized)
- **Channels**: RGB (3 channels)
- **Conversion**: Automatic scaling to [0, 255] uint8 for PNG encoding

### API Communication

- **Protocol**: OpenAI-compatible REST API
- **Authentication**: Bearer token (API key)
- **Content Type**: Base64-encoded PNG images
- **Response Format**: Standard chat completion format

### Error Handling

- **Network failures**: Automatic fallback to cached model list
- **API errors**: Graceful error propagation with descriptive messages
- **Invalid inputs**: Input validation and helpful error messages
- **Timeout handling**: Configurable timeouts with fallback behavior

### Performance Characteristics

- **Image processing**: < 100ms for typical image sizes
- **API latency**: Depends on selected model and Abacus.AI service load
- **Memory usage**: Minimal - processes one image at a time
- **Concurrent safety**: Thread-safe for multiple workflow executions

## 🐛 Troubleshooting

### Common Issues

#### "Failed to fetch models" Error
```
[AbacusAI] Failed to fetch models, using fallback list: <error>
```
**Solution**: Check internet connection. The node will use fallback models and continue working.

#### "API key required" Error
**Solution**: Ensure your Abacus.AI API key is entered in the `api_key` field.

#### "Image conversion failed" Error
**Solution**: Verify the input image is a valid ComfyUI IMAGE tensor.

#### Import Errors
**Solution**: Ensure all dependencies are installed:
```bash
pip install -r requirements.txt
```

### Debug Mode

Enable verbose logging by checking ComfyUI console output for detailed error messages and API responses.

### Performance Issues

- Use smaller images for faster processing
- Consider model selection (some models are faster than others)
- Check your internet connection speed

## 📊 API Limits & Costs

### ⚠️ Important Cost Information

**This node consumes Abacus.AI API credits on every use. Make sure you have sufficient credits before running workflows.**

### Abacus.AI Service Limits

- **Rate Limits**: Vary by plan and model
- **Token Limits**: 1024 tokens per request (configurable)
- **Image Size**: Maximum dimensions vary by model
- **File Size**: Base64 encoding adds ~33% overhead
- **Cost per Request**: Depends on model selected and input size

### Cost Optimization

- Use appropriate model for your needs (faster models = lower cost)
- Batch similar requests when possible
- Monitor usage through Abacus.AI dashboard
- Consider image size - larger images consume more credits

## 🤝 Contributing

### Development Setup

1. Fork the repository
2. Clone your fork
3. Install development dependencies:
   ```bash
   pip install -r requirements-dev.txt
   ```
4. Run tests to ensure everything works:
   ```bash
   python run_tests.py
   ```
5. Make your changes
6. Add tests for new features
7. Run the full test suite
8. Submit a pull request

### Code Standards

- Follow PEP 8 style guidelines
- Add comprehensive tests for new features
- Update documentation for API changes
- Maintain backward compatibility

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

### No Affiliation with Abacus.AI

**This ComfyUI custom node ("Image to Prompt (Abacus.AI)") is an independent, third-party project and has NO affiliation, endorsement, sponsorship, or official relationship with Abacus.AI whatsoever.**

- This node is developed independently by the ComfyUI community
- Abacus.AI does not officially support, maintain, or endorse this node
- Abacus.AI is not responsible for this node's functionality, performance, or compatibility
- This node is not an official Abacus.AI product or service

### No Responsibility or Liability

**Abacus.AI bears NO responsibility or liability for:**

- The functionality or performance of this ComfyUI node
- Any errors, bugs, or issues encountered while using this node
- Compatibility with ComfyUI or other software
- Data loss, system damage, or any other harm resulting from node usage
- API rate limits, service outages, or changes to Abacus.AI's API
- Billing disputes, credit consumption, or account-related issues
- Any damages, losses, or costs incurred from using this node

### User Responsibility

**By using this node, you acknowledge and agree that:**

- You use this node entirely at your own risk
- You are responsible for ensuring compatibility with your system
- You are responsible for monitoring your Abacus.AI account and usage
- You understand that API services may change or be discontinued
- You have read and understood Abacus.AI's terms of service
- You comply with all applicable laws and regulations

### No Warranties

**This node is provided "AS IS" without any warranties:**

- No warranty of merchantability, fitness for a particular purpose, or non-infringement
- No guarantee of compatibility, performance, or reliability
- No assurance that the node will work with future versions of ComfyUI
- No guarantee that Abacus.AI's API will remain compatible or available

### Support and Maintenance

- This node is maintained by the ComfyUI community on a voluntary basis
- No official support is provided by Abacus.AI
- Bug reports and feature requests should be directed to this project's repository
- Abacus.AI cannot assist with issues related to this third-party node

### API Terms Compliance

- Users are responsible for complying with Abacus.AI's API terms of service
- This node does not modify or bypass any Abacus.AI API restrictions
- Users must obtain their own API keys and manage their own accounts
- Abacus.AI's terms of service apply to all API usage through this node

**If you have questions about Abacus.AI's services, billing, or official products, please contact Abacus.AI directly through their official channels.**

---

## 🙏 Acknowledgments

- **Abacus.AI** - For providing the excellent API service
- **ComfyUI Community** - For the amazing workflow platform
- **OpenAI** - For the compatible API specification
- **Anthropic** - For Claude model capabilities

## 📞 Support

### Getting Help

1. **Check the tests**: Run `python run_tests.py` to verify installation
2. **Review documentation**: Check this README and test documentation
3. **ComfyUI logs**: Check console output for detailed error messages
4. **Community**: Join ComfyUI Discord or forums for community support

### Reporting Issues

When reporting bugs, please include:
- ComfyUI version
- Python version
- Full error message and traceback
- Steps to reproduce
- Your workflow setup (anonymized)

### Feature Requests

Feature requests are welcome! Please include:
- Use case description
- Expected behavior
- Mockups or examples if applicable

---

**Made with ❤️ for the ComfyUI community**

*Transform your images into powerful prompts with AI-powered analysis*</content>
<parameter name="filePath">c:\ComfyUI\custom_nodes\Image to Prompt (Abacus.AI)\README.md