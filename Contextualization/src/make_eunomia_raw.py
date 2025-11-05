import numpy as np
import pandas as pd
from pathlib import Path

# Adjust paths as needed (relative to Contextualization/src)
HG_DIR   = Path("../../Baselines/data/eunomia_hypergraph")   # from your prep notebook
OMOP_DIR = Path("../../Baselines/data/eunomia")         # original Eunomia OMOP CSVs
OUT_DIR  = Path("../../Contextualization/data/raw_data/eunomia")    # where raw files for eunomia go
OUT_DIR.mkdir(parents=True, exist_ok=True)

# 1) Load hypergraph artifacts ----------
nodes      = pd.read_csv(HG_DIR / "nodes.csv")
hyperedges = pd.read_csv(HG_DIR / "hyperedges.csv")
incidence  = pd.read_csv(HG_DIR / "incidence.csv")

nodes.columns      = [c.lower() for c in nodes.columns]
hyperedges.columns = [c.lower() for c in hyperedges.columns]
incidence.columns  = [c.lower() for c in incidence.columns]

# Map concept_id -> node index
concept_ids    = nodes["concept_id"].astype(int).tolist()
concept_to_idx = {cid: i for i, cid in enumerate(concept_ids)}
V = len(concept_ids)

# Assume hyperedge_id is 0..E-1
E = int(hyperedges["hyperedge_id"].max()) + 1

print(f"V (nodes) = {V}, E (hyperedges) = {E}")

# 2) Build hyperedges-eunomia.txt ----------
he_to_nodes = [[] for _ in range(E)]
for _, row in incidence.iterrows():
    e   = int(row["hyperedge_id"])
    cid = int(row["concept_id"])
    if cid in concept_to_idx:
        he_to_nodes[e].append(concept_to_idx[cid])

# Deduplicate & sort
for e in range(E):
    he_to_nodes[e] = sorted(set(he_to_nodes[e]))

hyperedges_txt = OUT_DIR / "hyperedges-eunomia.txt"
with open(hyperedges_txt, "w") as f:
    for edge_nodes in he_to_nodes:
        line = ",".join(str(i) for i in edge_nodes)
        f.write(line + "\n")

print("Wrote:", hyperedges_txt)

# 3) Build edge-labels-eunomia.txt ----------
# Example: one binary label for "hypertension" (replace with your concept IDs)
condition = pd.read_csv(OMOP_DIR / "condition_occurrence.csv")
condition.columns = [c.lower() for c in condition.columns]

# Replace this with your chosen SNOMED IDs
HYPERTENSION_IDS = {38341003}  # example hypertension concept

he_map = hyperedges.set_index("visit_occurrence_id")["hyperedge_id"]

cond_ht = condition[condition["condition_concept_id"].isin(HYPERTENSION_IDS)]
visits_with_ht = cond_ht["visit_occurrence_id"].unique()

Y = np.zeros((E, 1), dtype=np.int64)
for v_id in visits_with_ht:
    if v_id in he_map.index:
        e = int(he_map.loc[v_id])
        Y[e, 0] = 1

print("Label distribution [0,1]:", np.bincount(Y[:,0]))

edge_labels_txt = OUT_DIR / "edge-labels-eunomia.txt"
# Save as CSV with no header, comma-separated (like mimic/cradle/promote)
np.savetxt(edge_labels_txt, Y, fmt="%d", delimiter=",")
print("Wrote:", edge_labels_txt)

# 4) Build node-embeddings-eunomia ----------
# Minimal version: random embeddings, but in the same TEXT format:
# first line: "num_nodes embedding_dim"
# following lines: "<node_index> <v1> <v2> ... <vd>"

embedding_dim = 128
features = np.random.randn(V, embedding_dim).astype(np.float32)

node_emb_path = OUT_DIR / "node-embeddings-eunomia"
with open(node_emb_path, "w") as f:
    f.write(f"{V} {embedding_dim}\n")
    for idx in range(V):
        vals = " ".join(str(x) for x in features[idx])
        f.write(f"{idx} {vals}\n")

print("Wrote node embeddings to:", node_emb_path)
