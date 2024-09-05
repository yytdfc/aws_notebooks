# SageMaker Invoke Rerank Sample

This is the java version of invoke rerank model on SageMaker.
[Python version](https://github.com/cohere-ai/cohere-aws/blob/main/notebooks/sagemaker/rerank_v3_notebooks/Deploy%20rerank%20multilingual%20v3.0%20model.ipynb)

```bash
export AWS_ACCESS_KEY_ID="xxxxxxxxxxxxxxxxx"
export AWS_SECRET_ACCESS_KEY="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

mvn compile
mvn exec:java -Dexec.mainClass="org.example.App"
```
