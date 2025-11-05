from pykeen.triples import TriplesFactory
from pykeen.pipeline import pipeline
from pykeen.datasets.nations import NATIONS_TRAIN_PATH
import pandas as pd
import torch

if torch.cuda.is_available():
    print(f"CUDA is available. Using GPU: {torch.cuda.get_device_name(0)}")
else:
    print("CUDA is not available. Using CPU.")

tf = TriplesFactory.from_path(
    r"KGENewMethod/Data/finalData/filtered_final.tsv")

training, testing = tf.split()

result = pipeline(
    model='ComplEx',
    training=training,
    testing=testing,
    training_kwargs=dict(
        num_epochs=80,
        batch_size=512,
    ),
    model_kwargs=dict(
        embedding_dim=64,
    ),
    optimizer_kwargs=dict(
        lr=0.01,
    ),
    regularizer_kwargs=dict(
        weight=0.001,
    ),
)
result.save_to_directory('doctests/ComplExSmall')
print(result.get_metric('hits_at_k'))
