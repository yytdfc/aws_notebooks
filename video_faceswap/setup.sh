#! /bin/bash
# bash -c "$(curl -fsSL https://raw.githubusercontent.com/yytdfc/aws_notebooks/master/video_faceswap/setup.sh)"

cd /home/ec2-user/SageMaker
git clone https://github.com/yytdfc/aws_notebooks.git
cd aws_notebooks/video_faceswap
conda env create -f conda_env.yaml
# conda activate insightface
