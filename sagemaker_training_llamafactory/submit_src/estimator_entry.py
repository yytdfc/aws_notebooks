import os
import json

if __name__ == "__main__":
    os.system('cd LLaMA-Factory && pip install -e ".[torch,metrics]"')
    os.system("pip install flash-attn --no-build-isolation")
    
    hosts = json.loads(os.environ['SM_HOSTS'])
    current_host = os.environ['SM_CURRENT_HOST']
    host_rank = hosts.index(current_host)
    
    os.environ['FI_PROVIDER'] = 'efa'    
    os.system("wandb disabled")
    
    # Copy model and datasetfrom s3 to GPU instance
    os.system('chmod +x ./s5cmd')
    model_s3_path = os.environ['MODEL_ID_OR_S3_PATH']
    dataset_s3_path = os.environ['DATASET_S3_PATH']
    os.system(f'./s5cmd cp {model_s3_path} /tmp/initial-model-path/')
    os.system(f'./s5cmd cp {dataset_s3_path} /tmp/finetune_dataset/')

    os.system(f'''FORCE_TORCHRUN=1 NNODES={len(hosts)} NODE_RANK={host_rank} MASTER_ADDR={hosts[0]} MASTER_PORT=7777 llamafactory-cli train {os.environ['CONF_YAML_NAME']}''')


    # Copy model from 1 GPU instance (if "stage3_gather_16bit_weights_on_model_save": true)
    trained_s3_uri = os.environ['MODEL_SAVE_PATH_S3']
    if 0 == host_rank:
        os.system(f'./s5cmd cp /tmp/tuned-model-path/ {trained_s3_uri}')
