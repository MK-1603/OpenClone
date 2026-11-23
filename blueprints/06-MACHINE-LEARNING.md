# Blueprint 06: Machine Learning Engineering

**Project Family:** `machine_learning`  
**Primary Project Type:** `classical_ml_pipeline`, `deep_learning_cv_nlp`  
**Maturity Status:** `IMPLEMENTED`  
**Complexity Level:** `MEDIUM` to `LARGE`  
**Default Delivery Targets:** `containers_cloud`, `edge_devices`

---

## 1. Goals & Scope
- Predictive modeling on tabular, image, audio, or text data utilizing supervised/unsupervised learning or deep neural networks.
- Enforces strict data provenance, reproducible train/validation/test splits, feature store consistency, baseline comparison, and model drift monitoring.

## 2. Classification Rules
- Matched when predictive models (scikit-learn, XGBoost, PyTorch, TensorFlow) are trained on datasets to perform classification, regression, clustering, or generation.
- Never confuse standard LLM prompting with trained ML models.

## 3. Intake Questions & Required Information
1. Target variable and evaluation metric (e.g. F1-score, ROC-AUC, RMSE, MAE).
2. Data sources, volume, and label quality.
3. Baseline model to beat (heuristic rule or linear model).
4. Inference latency budget and deployment target (batch job or real-time API).
5. Drift monitoring strategy (data drift vs. concept drift).

## 4. Domain & Capability Mapping
- **Mandatory Domains:** `01-SPECIFICATION`, `02-ARCHITECTURE`, `03-DATA-INTEGRITY`, `10-TESTING-AND-QA`, `14-PERFORMANCE-ENGINEERING`, `29-AI-GOVERNANCE`.
- **Mandatory Engines:** `E-001`, `E-002`, `E-003`, `E-010`, `E-014`, `E-029`.

## 5. Specialist Workforce
- `ml-engineer`: Feature transformation, model training loops, and hyperparameter tuning.
- `ml-research-engineer`: Architecture design and loss function optimization.
- `eval-engineer`: Out-of-fold validation, data leakage prevention, and slice metrics.

## 6. Verification & Delivery Artifacts
- Model card detailing training data, evaluation metrics, and failure modes.
- Reproducible training pipeline script with fixed random seed.
- Serialized model artifact (ONNX / TorchScript) with latency benchmark evidence.
