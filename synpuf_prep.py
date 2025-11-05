# %% [markdown]
# # SynPUF 1k → Patient Hypergraph via DuckDB
#
# - Raw data: tab-delimited, no-header OMOP-like CSVs (SynPUF 1k)
# - Hyperedge = patient (person_id)
# - Node = clinical concept (condition / drug / procedure / device / measurement / observation)
# - Incidence = which concepts each patient has
# - Label = 1 if patient appears in death.csv, else 0
#
# Output:
#   Baselines/data/synpuf1k_hypergraph/{nodes.csv, hyperedges.csv, incidence.csv}
#   Contextualization/data/raw_data/synpuf1k/edge-labels-synpuf1k.txt


# %%
import duckdb
from pathlib import Path
import pandas as pd
import numpy as np

# Adjust this to where your SynPUF TSV files live
BASE_DIR = Path("Baselines/data/synpuf1k")

HG_OUT_DIR    = Path("Baselines/data/synpuf1k_hypergraph")
RAW_LABEL_DIR = Path("Contextualization/data/raw_data/synpuf1k")
HG_OUT_DIR.mkdir(parents=True, exist_ok=True)
RAW_LABEL_DIR.mkdir(parents=True, exist_ok=True)

print("BASE_DIR:", BASE_DIR.resolve())
print("HG_OUT_DIR:", HG_OUT_DIR.resolve())
print("RAW_LABEL_DIR:", RAW_LABEL_DIR.resolve())


# %% [markdown]
# ## 1. Create DuckDB views over raw TSVs (no header, tab-delimited)


# %%
def create_view_from_tsv_auto(view_name: str, file_name: str):
    """
    Create a DuckDB view from a tab-delimited, no-header CSV.
    Columns will be named column0, column1, ... automatically.
    """
    path = str((BASE_DIR / file_name).resolve())
    duckdb.sql(f"""
        CREATE OR REPLACE VIEW {view_name} AS
        SELECT *
        FROM read_csv(
            '{path}',
            delim='\t',
            header=FALSE,
            auto_detect=TRUE
        );
    """)
    print(f"Created view {view_name} from {file_name}")

# Core OMOP tables
create_view_from_tsv_auto("person_raw",              "person.csv")
create_view_from_tsv_auto("observation_period_raw",  "observation_period.csv")
create_view_from_tsv_auto("visit_occurrence_raw",    "visit_occurrence.csv")
create_view_from_tsv_auto("condition_occurrence_raw","condition_occurrence.csv")
create_view_from_tsv_auto("drug_exposure_raw",       "drug_exposure.csv")
create_view_from_tsv_auto("procedure_occurrence_raw","procedure_occurrence.csv")
create_view_from_tsv_auto("device_exposure_raw",     "device_exposure.csv")
create_view_from_tsv_auto("measurement_raw",         "measurement.csv")
create_view_from_tsv_auto("observation_raw",         "observation.csv")
create_view_from_tsv_auto("death_raw",               "death.csv")


# %% [markdown]
# (Optional) Inspect a few rows to confirm column indices.
# If needed, run and eyeball where person_id, concept_id, visit_occurrence_id are.


# %%
# Uncomment to inspect if you want to verify positions
# duckdb.sql("SELECT * FROM person_raw LIMIT 5").df()
# duckdb.sql("SELECT * FROM visit_occurrence_raw LIMIT 5").df()
# duckdb.sql("SELECT * FROM condition_occurrence_raw LIMIT 5").df()
# duckdb.sql("SELECT * FROM drug_exposure_raw LIMIT 5").df()
# duckdb.sql("SELECT * FROM procedure_occurrence_raw LIMIT 5").df()
# duckdb.sql("SELECT * FROM death_raw LIMIT 5").df()


# %% [markdown]
# ## 2. Create cleaned OMOP tables with proper column names
#
# These `columnN` positions follow typical SynPUF OMOP layouts.
# If your preview shows different positions, just tweak the columnN indices here.


# %%
duckdb.sql("""
    CREATE OR REPLACE TABLE person AS
    SELECT
        column00::BIGINT AS person_id,
        column01::INT    AS gender_concept_id,
        column02::INT    AS year_of_birth,
        column03::INT    AS month_of_birth,
        column04::INT    AS day_of_birth
    FROM person_raw;
""")

duckdb.sql("""
    CREATE OR REPLACE TABLE visit_occurrence AS
    SELECT
        column00::BIGINT AS visit_occurrence_id,
        column01::BIGINT AS person_id,
        column02::INT    AS visit_concept_id,
        column03::DATE   AS visit_start_date
    FROM visit_occurrence_raw;
""")

duckdb.sql("""
    CREATE OR REPLACE TABLE condition_occurrence AS
    SELECT
        column00::BIGINT  AS condition_occurrence_id,
        column01::BIGINT  AS person_id,
        column02::INT     AS condition_concept_id,
        column10::BIGINT AS visit_occurrence_id
    FROM condition_occurrence_raw;
""")

duckdb.sql("""
    CREATE OR REPLACE TABLE drug_exposure AS
    SELECT
        column00::BIGINT  AS drug_exposure_id,
        column01::BIGINT  AS person_id,
        column02::INT     AS drug_concept_id,
        column17::BIGINT AS visit_occurrence_id
    FROM drug_exposure_raw;
""")

duckdb.sql("""
    CREATE OR REPLACE TABLE procedure_occurrence AS
    SELECT
        column00::BIGINT  AS procedure_occurrence_id,
        column01::BIGINT  AS person_id,
        column02::INT     AS procedure_concept_id,
        column09::BIGINT  AS visit_occurrence_id
    FROM procedure_occurrence_raw;
""")

duckdb.sql("""
    CREATE OR REPLACE TABLE device_exposure AS
    SELECT
        column00::BIGINT  AS device_exposure_id,
        column01::BIGINT  AS person_id,
        column02::INT     AS device_concept_id,
        column09::BIGINT  AS visit_occurrence_id
    FROM device_exposure_raw;
""")

duckdb.sql("""
    CREATE OR REPLACE TABLE measurement AS
    SELECT
        column00::BIGINT  AS measurement_id,
        column01::BIGINT  AS person_id,
        column02::INT     AS measurement_concept_id,
        column09::BIGINT  AS visit_occurrence_id
    FROM measurement_raw;
""")

duckdb.sql("""
    CREATE OR REPLACE TABLE observation AS
    SELECT
        column00::BIGINT  AS observation_id,
        column01::BIGINT  AS person_id,
        column02::INT     AS observation_concept_id,
        column09::BIGINT  AS visit_occurrence_id
    FROM observation_raw;
""")

duckdb.sql("""
    CREATE OR REPLACE TABLE death AS
    SELECT
        column0::BIGINT AS person_id,
        column1::DATE   AS death_date,
        column3::INT    AS death_type_concept_id
    FROM death_raw;
""")

# Sanity check: row counts
for t in [
    "person", "visit_occurrence", "condition_occurrence",
    "drug_exposure", "procedure_occurrence",
    "device_exposure", "measurement", "observation", "death"
]:
    n = duckdb.sql(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
    print(f"{t:22s} rows: {n}")


# %%
# 3.1 Union all concept domains
duckdb.sql("""
    CREATE OR REPLACE TABLE concept_events AS
    SELECT person_id, condition_concept_id AS concept_id
    FROM condition_occurrence
    WHERE condition_concept_id IS NOT NULL AND condition_concept_id > 0

    UNION ALL
    SELECT person_id, drug_concept_id AS concept_id
    FROM drug_exposure
    WHERE drug_concept_id IS NOT NULL AND drug_concept_id > 0

    UNION ALL
    SELECT person_id, procedure_concept_id AS concept_id
    FROM procedure_occurrence
    WHERE procedure_concept_id IS NOT NULL AND procedure_concept_id > 0

    UNION ALL
    SELECT person_id, device_concept_id AS concept_id
    FROM device_exposure
    WHERE device_concept_id IS NOT NULL AND device_concept_id > 0

    UNION ALL
    SELECT person_id, measurement_concept_id AS concept_id
    FROM measurement
    WHERE measurement_concept_id IS NOT NULL AND measurement_concept_id > 0

    UNION ALL
    SELECT person_id, observation_concept_id AS concept_id
    FROM observation
    WHERE observation_concept_id IS NOT NULL AND observation_concept_id > 0
;
""")

# 3.2 Deduplicate person–concept
duckdb.sql("""
    CREATE OR REPLACE TABLE concept_events_clean AS
    SELECT person_id, concept_id
    FROM concept_events
    GROUP BY person_id, concept_id;
""")

# 3.3 Hyperedges: one per person
duckdb.sql("""
    CREATE OR REPLACE TABLE hyperedges AS
    SELECT
        row_number() OVER (ORDER BY person_id) - 1 AS hyperedge_id,
        person_id
    FROM (
        SELECT DISTINCT person_id
        FROM concept_events_clean
    ) t
    ORDER BY person_id;
""")

# 3.4 Nodes: unique concepts
duckdb.sql("""
    CREATE OR REPLACE TABLE nodes AS
    SELECT DISTINCT concept_id
    FROM concept_events_clean
    ORDER BY concept_id;
""")

# 3.5 Incidence: hyperedge_id–concept_id
duckdb.sql("""
    CREATE OR REPLACE TABLE incidence AS
    SELECT
        h.hyperedge_id,
        c.concept_id
    FROM concept_events_clean c
    JOIN hyperedges h
      ON c.person_id = h.person_id
    ORDER BY h.hyperedge_id, c.concept_id;
""")

# 3.6 Labels: death or not per hyperedge
duckdb.sql("""
    CREATE OR REPLACE TABLE labels AS
    SELECT
        h.hyperedge_id,
        CASE WHEN d.person_id IS NULL THEN 0 ELSE 1 END AS label
    FROM hyperedges h
    LEFT JOIN death d
      ON h.person_id = d.person_id
    ORDER BY h.hyperedge_id;
""")


# %%
hyperedges_df = duckdb.sql("SELECT * FROM hyperedges").df()
nodes_df      = duckdb.sql("SELECT concept_id AS node_id FROM nodes").df()
incidence_df  = duckdb.sql("SELECT * FROM incidence").df()
labels_df     = duckdb.sql("SELECT label FROM labels").df()

print("hyperedges_df:", hyperedges_df.shape)
print("nodes_df:", nodes_df.shape)
print("incidence_df:", incidence_df.shape)
print("labels_df:", labels_df.shape)

num_pos = int(labels_df["label"].sum())
num_neg = len(labels_df) - num_pos
print("Death positives:", num_pos)
print("Death negatives:", num_neg)

hyperedges_df.head(), nodes_df.head(), incidence_df.head(), labels_df.head()


# %%
# nodes.csv: one row per node (node_id = concept_id)
nodes_df.to_csv(HG_OUT_DIR / "nodes.csv", index=False)

# hyperedges.csv: hyperedge_id + person_id
hyperedges_df.to_csv(HG_OUT_DIR / "hyperedges.csv", index=False)

# incidence.csv: hyperedge_id, concept_id
incidence_df.to_csv(HG_OUT_DIR / "incidence.csv", index=False)

# edge-labels-synpuf1k.txt: E x 1 labels, comma-separated
Y = labels_df["label"].to_numpy().reshape(-1, 1).astype(int)
np.savetxt(RAW_LABEL_DIR / "edge-labels-synpuf1k.txt", Y, fmt="%d", delimiter=",")

print("Saved:")
print("  ", HG_OUT_DIR / "nodes.csv")
print("  ", HG_OUT_DIR / "hyperedges.csv")
print("  ", HG_OUT_DIR / "incidence.csv")
print("  ", RAW_LABEL_DIR / "edge-labels-synpuf1k.txt")

# %%
num_nodes  = len(nodes_df)
num_labels = 1

print("num_nodes:", num_nodes)
print("num_labels:", num_labels)

# %% Build HypKG-style raw files for synpuf1k

# 1. Make sure we have contiguous node indices 0..num_nodes-1
nodes_df = nodes_df.sort_values("node_id").reset_index(drop=True)
nodes_df["idx"] = np.arange(len(nodes_df), dtype=int)

concept_to_idx = dict(zip(nodes_df["node_id"], nodes_df["idx"]))

num_nodes = len(nodes_df)
print("num_nodes:", num_nodes)

# 2. Build hyperedges-synpuf1k.txt
RAW_DIR = Path("Contextualization/data/raw_data/synpuf1k")
RAW_DIR.mkdir(parents=True, exist_ok=True)

hyperedges_txt_path = RAW_DIR / "hyperedges-synpuf1k.txt"

with open(hyperedges_txt_path, "w") as f:
    for hid, group in incidence_df.groupby("hyperedge_id"):
        node_idx_list = (
            group["concept_id"]
            .map(concept_to_idx)
            .dropna()
            .astype(int)
            .tolist()
        )
        if not node_idx_list:
            # if a patient has no concepts at all, write an empty line
            f.write("\n")
        else:
            node_idx_list = sorted(node_idx_list)
            f.write(",".join(str(i) for i in node_idx_list) + "\n")

print("Wrote hyperedges to:", hyperedges_txt_path)

# 3. Save labels as edge-labels-synpuf1k.txt (you may already have this; overwrite is fine)
labels_txt_path = RAW_DIR / "edge-labels-synpuf1k.txt"
Y = labels_df["label"].to_numpy().reshape(-1, 1).astype(int)
np.savetxt(labels_txt_path, Y, fmt="%d", delimiter=",")
print("Wrote labels to:", labels_txt_path)

# 4. Generate random node embeddings (128-dim)
feature_dim = 128
emb = np.random.randn(num_nodes, feature_dim).astype(np.float32)

emb_path = RAW_DIR / "node-embeddings-synpuf1k"
with open(emb_path, "w") as f:
    f.write(f"{num_nodes} {feature_dim}\n")
    for idx in range(num_nodes):
        vec = emb[idx]
        f.write(str(idx) + " " + " ".join(str(x) for x in vec) + "\n")

print("Wrote node embeddings to:", emb_path)

# %%
