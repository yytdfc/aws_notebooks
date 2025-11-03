# AWS Notebooks

本仓库包含一系列 AWS 服务的示例代码和 Jupyter Notebook，涵盖 Amazon Bedrock、Amazon SageMaker 等服务的实践案例。

[English Documentation](README.md)

## 📚 目录结构

### Amazon Bedrock

#### `bedrock_invoke_restful_java/`
基于 Spring Boot 的 AWS Bedrock 客户端，支持调用 Claude 模型并处理流式响应。
- 使用 Spring WebFlux 实现非阻塞请求
- AWS Signature V4 身份验证
- 响应式编程实现

#### `bedrock_invoke_restful_python/`
Python 实现的 Bedrock API 调用示例
- `bedrock_invoke_stream.py`: 流式调用示例
- `bedrock_converse_stream.py`: Converse API 流式调用
- `bedrock_converse_apikey.py`: 使用 API Key 认证

#### `bedrock_nova_image_grounding/`
Amazon Bedrock Nova 模型的图像定位（Image Grounding）功能示例
- Jupyter Notebook 交互式演示
- Python 脚本版本

### Amazon SageMaker

#### `sagemaker_vllm/`
在 SageMaker 上部署 vLLM（Vector Language Model）端点
- Docker 镜像构建配置
- 部署和测试 Notebook

#### `sagemaker_byoc/`
SageMaker Bring Your Own Container (BYOC) 示例
- 同步和异步端点部署
- 自定义容器部署指南

#### `sagemaker_lmi/`
SageMaker Large Model Inference (LMI) 示例
- `bge-reranker-v2-gemma.ipynb`: BGE Reranker Gemma 模型
- `bge-reranker-v2-m3.ipynb`: BGE Reranker M3 模型

#### `sagemaker_endpoint_DeepSeek-R1-671b_dynamic-quants/`
DeepSeek-R1-671B 模型在 SageMaker 上的部署，使用动态量化

#### `sagemaker_endpoint_hunyuan3d-2/`
腾讯混元 3D-2 模型部署示例
- BYOS (Bring Your Own Script) 方式
- BYOC (Bring Your Own Container) 方式

#### `sagemaker_training_llamafactory/`
使用 LLaMA Factory 在 SageMaker 上进行模型训练

### 其他工具和示例

#### `invoke_rerank_javacode/`
Java 实现的 Rerank 模型调用示例

#### `video_faceswap/`
视频换脸工具和示例

#### `whisper/`
OpenAI Whisper 语音识别速度测试

#### `webm_writer/`
WebM 格式视频处理工具

#### `translate_html/`
HTML 翻译工具

#### `code_filling/`
代码填充（Code Infilling）示例

#### `dataset_codeinfill/`
代码填充数据集生成工具
- `code_splitter.py`: 代码分割器
- `code_analyzer.py`: 代码分析器
- `generate_dataset.ipynb`: 数据集生成 Notebook

#### `src/`
通用工具类
- `display_utils.py`: 显示工具函数

## 🚀 快速开始

### 环境要求

- **Python**: 3.8+
- **Java**: 17+ (针对 Java 项目)
- **AWS CLI**: 已配置 AWS 凭证
- **Jupyter**: 用于运行 `.ipynb` 文件

### AWS 凭证配置

确保已配置 AWS 凭证：

```bash
aws configure
```

或设置环境变量：

```bash
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_DEFAULT_REGION=your_region
```

### Python 环境设置

建议使用虚拟环境：

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows

pip install -r requirements.txt  # 如果有的话
```

### 运行 Jupyter Notebook

```bash
jupyter notebook
```

## 📖 使用指南

每个子目录通常包含自己的 README.md 或详细的 Notebook 说明。建议按以下步骤进行：

1. 查看对应目录的 README 或 Notebook
2. 确保已配置相关 AWS 服务的访问权限
3. 根据示例代码修改配置参数
4. 运行代码或 Notebook

## 📝 注意事项

- 运行这些示例可能会产生 AWS 费用，请注意成本控制
- 某些服务（如 Bedrock）可能需要申请访问权限
- SageMaker 端点部署后记得及时删除，避免持续计费
- 敏感信息（如 AWS 密钥）不要提交到代码仓库

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

请根据实际情况添加适当的许可证信息。

## 🔗 相关资源

- [AWS Bedrock 文档](https://docs.aws.amazon.com/bedrock/)
- [Amazon SageMaker 文档](https://docs.aws.amazon.com/sagemaker/)
- [AWS SDK for Python (Boto3)](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
- [AWS SDK for Java](https://aws.amazon.com/sdk-for-java/)
