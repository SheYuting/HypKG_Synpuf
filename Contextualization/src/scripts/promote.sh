#!/bin/bash
#SBATCH --job-name=cache_ran
#SBATCH --output=cache_ran
#SBATCH --gres=gpu:1

conda activate base

# promote
cd ..
python -u train.py --dname=promote --epochs=800 --cuda=1 --num_labels=1 --num_nodes=2604 --num_labeled_data=all --All_num_layers 3 --cuda=1 --feature_dim=128 --heads=4 --MLP_num_layers 2 --MLP_hidden 48 --model_lambda=0.01 --rand_seed=0 --vanilla --random_split --lr=1e-4

conda deactivate



