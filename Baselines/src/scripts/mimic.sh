#!/bin/bash
#SBATCH --job-name=sklearn_aft0
#SBATCH --output=avgnode_aft0
#SBATCH --mem=256G

conda activate base
python -u train.py --dname mimic3 --num_labels 25 --num_nodes 7423 --node_feature avgnode --num_labeled_data 12353 --random_split --rand_seed=0 --xgboost=True
python -u train.py --dname mimic3 --num_labels 25 --num_nodes 7423 --node_feature avgnode --num_labeled_data 12353 --random_split --rand_seed=1 --xgboost=True
python -u train.py --dname mimic3 --num_labels 25 --num_nodes 7423 --node_feature avgnode --num_labeled_data 12353 --random_split --rand_seed=2 --xgboost=True
python -u train.py --dname mimic3 --num_labels 25 --num_nodes 7423 --node_feature avgnode --num_labeled_data 12353 --random_split --rand_seed=3 --xgboost=True
python -u train.py --dname mimic3 --num_labels 25 --num_nodes 7423 --node_feature avgnode --num_labeled_data 12353 --random_split --rand_seed=4 --xgboost=True
conda deactivate
