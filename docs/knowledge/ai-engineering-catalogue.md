# AI & Intelligence Engineering Knowledge Catalogue
**1,095 Canonical Topics Across 18 Artificial Intelligence Domains**  
*OpenClone Global Engineering Intelligence | Reference Standards for Applied AI Systems*

---

## 1. Overview & Learning Progression

The OpenClone AI Knowledge Catalogue consolidates 1,095 foundational and applied AI topics into 18 structured domains.
**Core Rule**: Category counts are thematic and hierarchical. Projects should selectively retrieve only the models, RAG strategies, and agent architectures justified by explicit functional requirements.

---

## 2. The 18 AI Engineering Domains

| Domain ID | Category | Scope & Core Topics Covered |
|---|---|---|
| **01** | **Foundations & Mathematics** | Linear algebra, matrix decompositions (SVD), multivariate calculus, probability distributions, information theory, entropy, optimization algorithms (SGD, AdamW). |
| **02** | **Machine Learning Core** | Supervised learning (Regression, Classification), Unsupervised (K-Means, PCA, t-SNE), Tree ensembles (XGBoost, LightGBM, Random Forest), Feature engineering. |
| **03** | **ML Engineering & MLOps** | Model registries (MLflow), Feature stores (Feast), Model drift detection, Data versioning (DVC), Pipeline orchestration (Kubeflow, Airflow), Reproducibility. |
| **04** | **Deep Learning Architectures** | Neural networks, Backpropagation, CNNs, RNNs, LSTMs, Transformers (Self-Attention, Cross-Attention, FlashAttention), Diffusion models, Mamba/State Space Models. |
| **05** | **Generative AI & LLM Fundamentals** | Pre-training, Tokenization (BPE, WordPiece, SentencePiece), Decoder-only architectures, Rotary Position Embedding (RoPE), KV-Cache, Scaling Laws. |
| **06** | **Training, Fine-Tuning & Quantization** | Full fine-tuning, LoRA, QLoRA, PEFT, RLHF (PPO, DPO, GRPO), Instruction tuning, Model quantization (AWQ, GPTQ, GGUF, FP8, INT4), Distillation. |
| **07** | **Prompt & Context Engineering** | Zero-shot, Few-shot, Chain-of-Thought (CoT), Tree-of-Thoughts (ToT), Directional stimulus prompting, Context window caching, Token budget optimization. |
| **08** | **RAG & Knowledge Retrieval** | Dense vs Sparse retrieval (BM25 + Cohere/BGE), Chunking strategies (Recursive, Semantic), Vector databases (Pinecone, Qdrant, Milvus, pgvector), Hybrid search, Re-ranking. |
| **09** | **Agentic Workflows & Multi-Agent** | ReAct loop, Plan-and-Solve, Autonomous reflection, Tool use / Function calling, Subagent delegation, Memory architectures, Supervisor vs Swarm coordination. |
| **10** | **Automation & Workflow Engines** | Deterministic state graphs (LangGraph), Task DAG execution, Event-driven agent pipelines, Human-in-the-loop pause/resume states, Idempotent execution. |
| **11** | **Protocols, MCP & Sandboxing** | Model Context Protocol (MCP 2024-11-05), Agent-to-Agent (A2A) protocol, JSON-RPC stdio/SSE gateways, Container sandboxing (gVisor/Docker), Tool allowlists. |
| **12** | **Multimodal AI Systems** | Vision-Language Models (VLM), Audio & Speech-to-Text (Whisper), Text-to-Speech (TTS), Video generation, Multimodal embeddings (CLIP), Spatial computing AI. |
| **13** | **Application Domains** | Code generation & refactoring, Automated QA, Customer support intelligence, Document analysis / OCR extraction, Medical diagnostic assistance, Financial analysis. |
| **14** | **Lifecycle, Serving & LLMOps** | High-throughput inference engines (vLLM, SGLang, TensorRT-LLM), PagedAttention, Continuous batching, Speculative decoding, Model serving latency benchmarks. |
| **15** | **Evaluation, Safety & Red Teaming** | Automated evaluation benchmarks (MMLU, HumanEval, SWE-bench), LLM-as-a-Judge, Prompt injection defenses, Jailbreak detection, Hallucination scoring (RAGAS). |
| **16** | **AI Product Engineering & SaaS** | Streaming responses via SSE, Structured outputs (JSON Schema / Pydantic guarantees), Token usage metering & billing, Graceful model degradation, Fallbacks. |
| **17** | **Emerging Research & Ecosystem** | Reasoning models (o1, o3, DeepSeek R1), Test-time compute scaling, Dynamic model routing, Compound AI systems, Small language models (SLMs: Gemma, Phi, Qwen). |
| **18** | **Advanced AI System Design** | Multi-tier prompt caching, End-to-end latency optimization (<50ms TTFT), Distributed model inference, Multi-tenant vector isolation, Sovereign local AI. |

---

## 3. Operational Implementation Guidelines

1. **Structured Outputs**: Never rely on free-form regex parsing for agent actions. Enforce JSON Schema schema-validation on every tool call and model completion.
2. **Context Window Optimization**: Apply progressive disclosure; load only the task-relevant domain slice rather than dumping large taxonomies into the model prompt.
3. **Safety & Injection Defense**: Treat all user inputs and third-party web content as untrusted data.
