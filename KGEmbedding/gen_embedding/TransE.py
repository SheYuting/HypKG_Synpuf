from pykeen.triples import TriplesFactory
from pykeen.pipeline import pipeline
from pykeen.datasets.nations import NATIONS_TRAIN_PATH
import pandas as pd

tf = TriplesFactory.from_path(
    r"KGENewMethod/Data/finalData/filtered_final4.tsv")
training, testing = tf.split()

result = pipeline(
    model='TransE',
    training=training,
    testing=testing,
    training_kwargs=dict(
        num_epochs=20,
        batch_size=512,
    ),
    model_kwargs=dict(
        embedding_dim=128,

    )
)

result.save_to_directory('doctests/TransESmall')
print(result.get_metric('hits_at_k'))
