#!/bin/bash

# port needs to be $SAGEMAKER_BIND_TO_PORT

python3 -m vllm.entrypoints.openai.api_server \
    --port $SAGEMAKER_BIND_TO_PORT \
    --trust-remote-code \
    --max-model-len 8192 \
    --model deepseek-ai/deepseek-coder-6.7b-instruct
