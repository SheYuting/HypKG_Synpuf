from pykeen.triples import TriplesFactory
from pykeen.pipeline import pipeline
from pykeen.models import CompGCN
import pandas as pd

# Load triples from a file and ensure inverse triples are created
tf = TriplesFactory.from_path(
    r"/KGENewMethod/Data/finalData/filtered_final.tsv",
    create_inverse_triples=True  # Ensure inverse triples are created
)

# Split into training and testing sets
training, testing = tf.split()
result = pipeline(
    model='CompGCN',  # Provide the model name as a string
    training=training,
    testing=testing
)

# Save the result to a directory and print the hits@k metric
result.save_to_directory('doctests/CompGCN')
