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

model = torch.load(
    r"E:\KGE\NewExperiment\Result\TransE\trained_model.pkl")

entity_representation_modules: List['pykeen.nn.Representation'] = model.entity_representations
relation_representation_modules: List['pykeen.nn.Representation'] = model.relation_representations

entity_embeddings: pykeen.nn.Embedding = entity_representation_modules[0]
relation_embeddings: pykeen.nn.Embedding = relation_representation_modules[0]

entity_embedding_tensor: torch.FloatTensor = entity_embeddings()
relation_embedding_tensor: torch.FloatTensor = relation_embeddings()

entity_embedding_tensor: torch.FloatTensor = entity_embeddings(indices=None)
relation_embedding_tensor: torch.FloatTensor = relation_embeddings(
    indices=None)

entity_embedding_tensor = entity_embedding_tensor.detach().cpu().numpy()
relation_embedding_tensor = relation_embedding_tensor.detach().cpu().numpy()
print(entity_embedding_tensor)

# Separate real and imaginary parts
entity_real = entity_embedding_tensor.real
entity_imag = entity_embedding_tensor.imag
relation_real = relation_embedding_tensor.real
relation_imag = relation_embedding_tensor.imag

# Concatenate real and imaginary parts to get 128-dimension embeddings
entity_embeddings_128 = np.concatenate([entity_real, entity_imag], axis=1)
relation_embeddings_128 = np.concatenate(
    [relation_real, relation_imag], axis=1)

# Save the 128-dimension embeddings to CSV
entity_embeddings_df = pd.DataFrame(entity_embeddings_128)
entity_embeddings_df.to_csv(
    'transELarge_entity_embeddings_128.csv', index=False)

relation_embeddings_df = pd.DataFrame(relation_embeddings_128)
relation_embeddings_df.to_csv(
    'transELarge_relation_embeddings_128.csv', index=False)

print("Entity and relation embeddings have been saved to CSV files with 128 dimensions.")
