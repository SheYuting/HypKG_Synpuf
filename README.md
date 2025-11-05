# SynPUF-Based Knowledge Graph Model for Precision Healthcare

This repository implements and analyses a **hypergraph-based patient similarity model** inspired by recent advances in **knowledge graph learning** for medical data integration.  
It reproduces and extends key ideas from the referenced papers, adapting them to the **SynPUF1K synthetic OMOP dataset** to demonstrate how structured patient relationships can support **precision healthcare analytics**.

---

This work draws upon the following :

**Zheng et al., 2023 — “Hypergraph-Based Patient Representation Learning for Precision Medicine”** 

---

## 🧠 Model Overview

### 1. Hypergraph Construction
- **Vertices:** Individual patients in the SynPUF dataset.  
- **Hyperedges:** Shared medical concepts (conditions, drug exposures, procedures).  
- Each hyperedge connects all patients who share the same OMOP concept ID, forming a many-to-many relationship structure.

### 2. Feature Representation
- Each patient node is initialized with a **multi-hot vector** of concept features.  
- Concept embeddings are learned jointly with patient embeddings through message passing.

### 3. Learning Framework
The model employs a **Hypergraph Neural Network (HGNN)**:
\[
H = \text{softmax}(D_v^{-1/2} H W D_e^{-1/2})
\]
where \( H \) is the incidence matrix, \( D_v, D_e \) are vertex and hyperedge degree matrices, and \( W \) is a learnable weight matrix.

Loss is defined as:
\[
\mathcal{L} = \mathcal{L}_{\text{reconstruction}} + \lambda \mathcal{L}_{\text{regularization}}
\]
for unsupervised structure reconstruction or auxiliary clinical prediction tasks.

---

## 🧬 Dataset: SynPUF1K

**SynPUF (Synthetic Public Use Files)** is a **synthetic, privacy-preserving dataset** generated from the OMOP Common Data Model (CDM).  
Key properties:

- 1,000 synthetic patients (`SynPUF1K`)  
- Tables include: `person`, `condition_occurrence`, `drug_exposure`, `procedure_occurrence`  
- Fully de-identified and safe for open experimentation  
- Preserves statistical patterns and table relationships found in real EHR data

### Why SynPUF is Important
- Enables **public, reproducible testing** of healthcare AI pipelines without legal/ethical restrictions.
- Serves as a **benchmark** for validating medical graph learning models before applying to real clinical data.
- Facilitates **model interpretability** and **debugging** of hypergraph-based pipelines due to small, structured size.

---

## ⚙️ Repository Structure
├── data/
│ ├── synpuf1k/ # OMOP-format synthetic data
│ ├── processed/ # Preprocessed incidence & feature matrices
│
├── src/
│ ├── build_hypergraph.py # Construct patient-hyperedge incidence matrix
│ ├── model_hypkg.py # Hypergraph-based embedding model
│ ├── train.py # Training and evaluation scripts
│ └── visualize_results.py # Plot metrics and embeddings
│
├── results/
│ ├── mimicIII_results.png
│ ├── promote_results.png
│ ├── synpuf1k_results.png
│ └── comparison_table.csv
│
└── README.md
