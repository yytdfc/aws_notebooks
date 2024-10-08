#!/bin/bash

VLLM_VERSION=${VLLM_VERSION:-"v0.6.0"}
REPO_NAMESPACE=${REPO_NAMESPACE:-"sagemaker_endpoint/vllm"}

# Get the ACCOUNT and REGION defined in the current configuration (default to us-west-2 if none defined)

ACCOUNT=${ACCOUNT:-$(aws sts get-caller-identity --query Account --output text)}
REGION=${REGION:-$(aws configure get region)}

REPO_NAME="${ACCOUNT}.dkr.ecr.${REGION}.amazonaws.com/${REPO_NAMESPACE}:${VLLM_VERSION}"
echo ${REPO_NAME}

# If the repository doesn't exist in ECR, create it.
aws ecr describe-repositories --repository-names "${REPO_NAMESPACE}" > /dev/null 2>&1
if [ $? -ne 0 ]
then
echo "create repository:" "${REPO_NAMESPACE}"
aws ecr create-repository --repository-name "${REPO_NAMESPACE}" > /dev/null
fi

# Log into Docker
aws ecr get-login-password --region ${REGION} | docker login --username AWS --password-stdin ${ACCOUNT}.dkr.ecr.${REGION}.amazonaws.com

# Build docker
docker build --build-arg VLLM_VERSION=${VLLM_VERSION} -t ${REPO_NAMESPACE}:${VLLM_VERSION} .

# Push it
docker tag ${REPO_NAMESPACE}:${VLLM_VERSION} ${REPO_NAME}
docker push ${REPO_NAME}
