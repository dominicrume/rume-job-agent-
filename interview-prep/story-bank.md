# RUME DOMINIC — STAR+R STORY BANK
# Accumulated across all evaluations. Managed by /career-ops stories.
# Last updated: 2026-04-07

---

## Production RAG Pipeline — Tax Intelligence OCR Engine
**Archetype(s):** AI Platform / LLMOps, Agentic / Automation
**Competencies:** Technical delivery, production deployment, AI architecture
**JD Keywords:** RAG, production AI, LLMs, data extraction, GCP, cloud deployment, accuracy, governance

**Situation:** A business was manually processing unstructured, low-quality bank statement images to extract tax-relevant data. The process was slow, error-prone, and unscalable. No automated solution existed.

**Task:** As Lead AI/ML Engineer, my responsibility was to design, build, and deploy an automated AI solution end-to-end — from problem definition through to production.

**Action:** I engineered a custom AI-enhanced OCR analyzer using Google Gemini API and a RAG-powered retrieval architecture. I designed the pipeline to handle image degradation, built anomaly detection logic for data validation, and deployed the entire system to Google Cloud Platform via Cloud Run for serverless scale.

**Result:** The system moved to production and automated data extraction, anomaly detection, and tax categorisation — eliminating manual processing and delivering measurable improvements in data governance precision.

**Reflection:** The key insight was treating OCR not as a single-model problem but as a pipeline with distinct retrieval, extraction, and validation stages. If I did it again, I'd build a feedback loop into the anomaly detection layer to improve precision over time.

---

## Hallucination Guardrails — Enterprise LLM Deployment
**Archetype(s):** AI Platform / LLMOps, AI Transformation
**Competencies:** Technical governance, responsible AI, enterprise reliability
**JD Keywords:** hallucination mitigation, prompt engineering, LLM guardrails, enterprise AI, production safety

**Situation:** An enterprise was deploying large language models for automated business strategy tooling. The risk of hallucinated outputs in a compliance-sensitive context was significant — wrong outputs could have real business consequences.

**Task:** As Lead AI/ML Engineer, I was responsible for implementing guardrails to ensure enterprise-safe outputs from LLM workflows.

**Action:** I designed a custom prompt guardrail architecture — combining few-shot prompting, output validation layers, and structured response schemas. I tested adversarial edge cases systematically before each production release and documented the Responsible AI standards for cross-functional stakeholders.

**Result:** Successfully delivered Generative AI use cases into production with enterprise-safe outputs. Hallucination incidents were measured and consistently below threshold. The guardrail patterns became the standard deployment template for subsequent AI use cases.

**Reflection:** I learned that prompt guardrails alone are insufficient without output validation at the application layer. The combination of upstream prompt design and downstream format enforcement is what makes LLMs reliable in enterprise contexts.

---

## AIOps Platform — 91+ Performance Score at Micki Solutions
**Archetype(s):** AI Platform / LLMOps
**Competencies:** System reliability, AIOps, technical leadership
**JD Keywords:** AIOps, system reliability, performance, production-grade, AI platform, monitoring

**Situation:** Micki Solutions needed a production-grade AI platform that met strict performance and accessibility standards. The existing infrastructure had gaps in reliability monitoring and automated operations.

**Task:** As Senior AI/ML Engineer, I was tasked with designing and implementing the AIOps platform from the ground up, with measurable performance targets.

**Action:** I designed the AI platform architecture with AIOps practices baked in — automated health checks, performance monitoring, accessibility compliance testing, and reliability scoring built into the CI/CD pipeline. I also authored the AI requirements and security documentation to ensure Responsible AI standards were embedded in every workflow.

**Result:** Achieved 91+ performance scores in system reliability and accessibility. The security documentation became the governance baseline for all subsequent automated workflows.

**Reflection:** The 91+ score was achievable because we defined the measurement criteria before building, not after. Governance-first design is faster in the long run — retrofitting compliance is expensive.

---

## Autonomous Marketing Daemon — Digital Sovereign Agent
**Archetype(s):** Agentic / Automation
**Competencies:** Autonomous agent design, agentic systems, production deployment, technical innovation
**JD Keywords:** autonomous agents, agentic workflows, multi-step LLM, orchestration, headless automation, cron, scheduling

**Situation:** Content creation and multi-channel social media distribution was a major manual overhead for creators and brands — consuming hours daily with no scalable path.

**Task:** Design and ship an autonomous AI system that eliminates this overhead entirely — no human input required post-deployment.

**Action:** I engineered a 24/7 headless daemon with three core modules: a psychological narrative engine (Simera Brain) that shifts messaging from feature-selling to pain-solving, a Studio Director generating multimedia production briefs, and a Social Dispatcher with API connectors for X, LinkedIn, and Instagram. Triggered daily at 06:00 AM via cron — fully autonomous.

**Result:** The system runs without human intervention, generating daily marketing packets and deploying across channels. Engagement metrics increased and manual content overhead was eliminated.

**Reflection:** The hardest part wasn't the automation — it was teaching the LLM to write in a specific brand voice consistently. GPT-4o's tone control via system prompting is powerful, but the real reliability comes from tightly scoped output schemas, not just good prompts.

---

## Cross-Functional AI Literacy — Enterprise Capability Uplift
**Archetype(s):** AI Transformation, Technical AI PM
**Competencies:** Cross-functional leadership, change management, AI adoption, stakeholder communication
**JD Keywords:** AI literacy, organisational change, technology adoption, cross-functional, stakeholders

**Situation:** Teams within an enterprise environment had limited understanding of AI's practical capabilities — creating a gap between what AI could deliver and what stakeholders were requesting or approving.

**Task:** As Lead AI/ML Engineer, I was responsible for increasing AI literacy and capability across teams while maintaining focus on long-term maintainability of delivered systems.

**Action:** I designed deployment patterns for automated business strategy tools that were intentionally transparent and explainable — not black boxes. I ran working sessions with cross-functional stakeholders, used real outputs to demonstrate capability, and built documentation that non-technical teams could actually use. I also embedded Responsible AI standards into every workflow so governance was part of the product, not a checkbox.

**Result:** Teams moved from passive AI consumers to active collaborators on AI use cases. AI literacy measurably increased — stakeholders began bringing problem statements rather than waiting to be educated.

**Reflection:** AI transformation is a trust problem before it's a technology problem. The turning point was when I stopped explaining AI and started showing it working on their actual data.

---

*Add new stories: `/career-ops stories add`*
*Find stories for a role: `/career-ops stories find [keyword]`*
