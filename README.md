# AWS Notebooks

A collection of example code and Jupyter Notebooks for AWS services, covering practical use cases for Amazon Bedrock, Amazon SageMaker, and more.

[中文文档](README_CN.md)

## 📚 Project Structure

### Amazon Bedrock

#### `bedrock_invoke_restful_java/`
Spring Boot-based AWS Bedrock client that supports calling Claude models with streaming responses.
- Non-blocking requests using Spring WebFlux
- AWS Signature V4 authentication
- Reactive programming implementation

#### `bedrock_invoke_restful_python/`
Python implementation examples for Bedrock API calls
- `bedrock_invoke_stream.py`: Streaming invocation example
- `bedrock_converse_stream.py`: Converse API streaming calls
- `bedrock_converse_apikey.py`: API Key authentication

#### `bedrock_nova_image_grounding/`
Image grounding examples using Amazon Bedrock Nova models
- Interactive Jupyter Notebook demo
- Python script version

### Amazon SageMaker

#### `sagemaker_vllm/`
Deploy vLLM (Vector Language Model) endpoints on SageMaker
- Docker image build configuration
- Deployment and testing notebook

#### `sagemaker_byoc/`
SageMaker Bring Your Own Container (BYOC) examples
- Synchronous and asynchronous endpoint deployment
- Custom container deployment guide

#### `sagemaker_lmi/`
SageMaker Large Model Inference (LMI) examples
- `bge-reranker-v2-gemma.ipynb`: BGE Reranker Gemma model
- `bge-reranker-v2-m3.ipynb`: BGE Reranker M3 model

#### `sagemaker_endpoint_DeepSeek-R1-671b_dynamic-quants/`
DeepSeek-R1-671B model deployment on SageMaker with dynamic quantization

#### `sagemaker_endpoint_hunyuan3d-2/`
Tencent Hunyuan 3D-2 model deployment examples
- BYOS (Bring Your Own Script) approach
- BYOC (Bring Your Own Container) approach

#### `sagemaker_training_llamafactory/`
Model training on SageMaker using LLaMA Factory

### Other Tools and Examples

#### `invoke_rerank_javacode/`
Java implementation for invoking Rerank models

#### `video_faceswap/`
Video face swap tools and examples

#### `whisper/`
OpenAI Whisper speech recognition speed test

#### `webm_writer/`
WebM format video processing tools

#### `translate_html/`
HTML translation tools

#### `code_filling/`
Code infilling examples

#### `dataset_codeinfill/`
Code infilling dataset generation tools
- `code_splitter.py`: Code splitter
- `code_analyzer.py`: Code analyzer
- `generate_dataset.ipynb`: Dataset generation notebook

#### `src/`
Common utility classes
- `display_utils.py`: Display utility functions

## 🚀 Getting Started

### Prerequisites

- **Python**: 3.8+
- **Java**: 17+ (for Java projects)
- **AWS CLI**: Configured with AWS credentials
- **Jupyter**: For running `.ipynb` files

### AWS Credentials Configuration

Ensure AWS credentials are configured:

```bash
aws configure
```

Or set environment variables:

```bash
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_DEFAULT_REGION=your_region
```

### Python Environment Setup

Using a virtual environment is recommended:

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

pip install -r requirements.txt  # if available
```

### Running Jupyter Notebooks

```bash
jupyter notebook
```

## 📖 Usage Guide

Each subdirectory typically contains its own README.md or detailed Notebook instructions. Follow these steps:

1. Review the README or Notebook in the corresponding directory
2. Ensure you have access permissions for the relevant AWS services
3. Modify configuration parameters according to the example code
4. Run the code or Notebook

## 📝 Important Notes

- Running these examples may incur AWS charges - please monitor costs
- Some services (like Bedrock) may require requesting access permissions
- Remember to delete SageMaker endpoints after deployment to avoid ongoing charges
- Never commit sensitive information (like AWS keys) to the repository

## 🤝 Contributing

Issues and Pull Requests are welcome!

## 📄 License

Please add appropriate license information as needed.

## 🔗 Resources

- [AWS Bedrock Documentation](https://docs.aws.amazon.com/bedrock/)
- [Amazon SageMaker Documentation](https://docs.aws.amazon.com/sagemaker/)
- [AWS SDK for Python (Boto3)](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
- [AWS SDK for Java](https://aws.amazon.com/sdk-for-java/)
