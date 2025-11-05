import pykeen
from pykeen.triples import TriplesFactory
from pykeen.pipeline import pipeline
from pykeen.datasets.nations import NATIONS_TRAIN_PATH
import pandas as pd
import torch
from torch.optim import Adam
from pykeen.training import SLCWATrainingLoop
from pykeen import predict
from typing import List
from pykeen.datasets import Nations
import pykeen.nn
from pykeen.pipeline import pipeline
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import numpy as np
# Load the trained model
model = torch.load(
    r"E:\KGE\NewExperiment\Result\CompGCN\trained_model.pkl")

# Get entity and relation representations
entity_representation_modules: List['pykeen.nn.Representation'] = model.entity_representations
relation_representation_modules: List['pykeen.nn.Representation'] = model.relation_representations

# Extract embeddings
entity_embeddings: pykeen.nn.Embedding = entity_representation_modules[0]
relation_embeddings: pykeen.nn.Embedding = relation_representation_modules[0]

# Get embedding tensors (real values only)
entity_embedding_tensor: torch.FloatTensor = entity_embeddings(indices=None)
relation_embedding_tensor: torch.FloatTensor = relation_embeddings(
    indices=None)

# Detach from computational graph and move to CPU if necessary
entity_embedding_tensor = entity_embedding_tensor.detach().cpu().numpy()
relation_embedding_tensor = relation_embedding_tensor.detach().cpu().numpy()

# Confirm the shape of the embeddings
print(f"Entity Embedding Shape: {entity_embedding_tensor.shape}")
print(f"Relation Embedding Shape: {relation_embedding_tensor.shape}")

# Since the embeddings are real, there's no need to separate real/imaginary parts
# Save the real embeddings (assuming they are already 128 dimensions)
entity_embeddings_df = pd.DataFrame(entity_embedding_tensor)
entity_embeddings_df.to_csv(
    'transELarge_entity_embeddings_128.csv', index=False)

relation_embeddings_df = pd.DataFrame(relation_embedding_tensor)
relation_embeddings_df.to_csv(
    'compGCN_relation_embeddings_128.csv', index=False)

print("Entity and relation embeddings have been saved to CSV files with 128 dimensions.")
