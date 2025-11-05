#!/bin/bash
#SBATCH --job-name=mimic2
#SBATCH --output=mimic_run
#SBATCH --gres=gpu:1

conda activate base

cd ..
python -u train.py --dname=mimic3 --epochs=800 --cuda=1 --num_labels=25 --num_nodes=7423 --num_labeled_data=12353 --All_num_layers 3 --lr 1e-3 --cuda=1 --feature_dim=128 --heads=4 --MLP_num_layers 2 --MLP_hidden 48 --model_lambda=0.01 --rand_seed=0 --vanilla --random_split
python -u train.py --dname=mimic3 --epochs=800 --cuda=1 --num_labels=25 --num_nodes=7423 --num_labeled_data=12353 --All_num_layers 3 --lr 1e-3 --cuda=1 --feature_dim=128 --heads=4 --MLP_num_layers 2 --MLP_hidden 48 --model_lambda=0.01 --rand_seed=1 --vanilla --random_split
python -u train.py --dname=mimic3 --epochs=800 --cuda=1 --num_labels=25 --num_nodes=7423 --num_labeled_data=12353 --All_num_layers 3 --lr 1e-3 --cuda=1 --feature_dim=128 --heads=4 --MLP_num_layers 2 --MLP_hidden 48 --model_lambda=0.01 --rand_seed=2 --vanilla --random_split
python -u train.py --dname=mimic3 --epochs=800 --cuda=1 --num_labels=25 --num_nodes=7423 --num_labeled_data=12353 --All_num_layers 3 --lr 1e-3 --cuda=1 --feature_dim=128 --heads=4 --MLP_num_layers 2 --MLP_hidden 48 --model_lambda=0.01 --rand_seed=3 --vanilla --random_split
python -u train.py --dname=mimic3 --epochs=800 --cuda=1 --num_labels=25 --num_nodes=7423 --num_labeled_data=12353 --All_num_layers 3 --lr 1e-3 --cuda=1 --feature_dim=128 --heads=4 --MLP_num_layers 2 --MLP_hidden 48 --model_lambda=0.01 --rand_seed=4 --vanilla --random_split
conda deactivate



