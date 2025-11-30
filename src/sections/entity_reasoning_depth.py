# dataset_generator/sections/entity_reasoning_depth.py

from __future__ import annotations

from typing import Any, Dict, List

from .base import SectionBuilder
from ..utils import make_metadata


class EntityReasoningDepthTrainingBuilder(SectionBuilder):
    """
    Section 10: Entity Reasoning Depth

    Teaches the model to:
    - Take ONE entity (product, policy, person, project)
    - Explain it across multiple dimensions (timeline, responsibilities, risks, KPIs)
    - Provide deeper, layered reasoning
    """

    @property
    def file_name(self) -> str:
        return "entity_reasoning_depth_training.json"

    def build_examples(self) -> List[Dict[str, Any]]:
        cfg = self.config
        # Increased to 200 to account for high deduplication rate (~80%)
        n = 200
        examples: List[Dict[str, Any]] = []

        for idx in range(1, n + 1):
            # Use prime multipliers to create better distribution across products
            product = cfg.primary_products[(idx * 7) % len(cfg.primary_products)]

            # Vary system prompts
            system_prompts = [
                (
                    f"You are {cfg.agent_name}, specialized in deep entity reasoning. "
                    "When asked about an entity, provide a structured, multi-paragraph analysis: "
                    "purpose, components, lifecycle, risks, and KPI impact."
                ),
                (
                    f"You are {cfg.agent_name}, an expert in entity analysis. "
                    "Deliver comprehensive breakdowns covering purpose, architecture, operations, "
                    "challenges, and measurable outcomes."
                ),
                (
                    f"You are {cfg.agent_name}, focused on thorough entity evaluation. "
                    "Provide detailed insights into function, dependencies, maintenance, "
                    "risk factors, and performance metrics."
                ),
                (
                    f"You are {cfg.agent_name}, a deep reasoning specialist. "
                    "Analyze entities across multiple dimensions: objectives, technical details, "
                    "lifecycle stages, mitigation strategies, and KPI contributions."
                ),
            ]
            system = system_prompts[(idx * 3) % len(system_prompts)]

            # Vary instruction templates
            instruction_templates = [
                f"Explain the role of {product} in depth.",
                f"Provide a comprehensive analysis of {product}.",
                f"Detail the purpose and impact of {product}.",
                f"Describe {product} across all key dimensions.",
                f"Give an in-depth overview of {product}.",
                f"Analyze {product} from a strategic perspective.",
                f"Break down the functionality and value of {product}.",
                f"Elaborate on how {product} operates within our ecosystem.",
            ]
            instruction = instruction_templates[(idx * 5) % len(instruction_templates)]

            # Provide a variation of multi-paragraph explanation
            output_templates = [
                (
                    f"{product} is a core component in {cfg.company_name}'s {cfg.domain_name} stack.\n\n"
                    "1. **Purpose**\n"
                    f"- Acts as the intelligence or indexing layer for {cfg.domain_name}.\n"
                    "- Normalizes data from multiple systems and exposes it consistently.\n\n"
                    "2. **Key Responsibilities**\n"
                    "- Ingest data from upstream systems.\n"
                    "- Build and maintain entity relationships.\n"
                    "- Provide consistent APIs for downstream consumers.\n\n"
                    "3. **Lifecycle**\n"
                    "- Initial configuration and schema mapping.\n"
                    "- Continuous ingestion and re-indexing.\n"
                    "- Monitoring, drift detection, and policy updates.\n\n"
                    "4. **Risks & Controls**\n"
                    "- Data quality issues → mitigated via validation and observability.\n"
                    "- Schema evolution → controlled via versioning and migration plans.\n\n"
                    "5. **KPI Impact**\n"
                    "- Reduces manual analysis effort.\n"
                    "- Improves time-to-answer for key business questions.\n"
                    "- Enables better governance and compliance reporting."
                ),
                (
                    f"Within {cfg.company_name}'s {cfg.domain_name} stack, {product} serves as the nexus for indexing and reasoning.\n\n"
                    "**Purpose**: It consolidates disparate data sources and offers a consistent view across systems.\n\n"
                    "**Responsibilities**: Beyond ingestion, it models relationships, maintains schemas and exposes them via APIs.\n\n"
                    "**Lifecycle**: From initial setup through continuous ingestion and periodic re-indexing, it remains a live component that adapts to schema changes.\n\n"
                    "**Risks**: Poor data quality or schema drift are mitigated with robust validation and controlled versioning.\n\n"
                    "**KPI Impact**: By automating data aggregation and reasoning, it shortens analysis time, improves compliance reporting and reduces manual work."
                ),
                (
                    f"**Overview of {product}**\n\n"
                    f"{product} functions as a central intelligence platform within {cfg.company_name}'s {cfg.domain_name} infrastructure.\n\n"
                    "**Core Purpose**\n"
                    "The system aggregates and harmonizes data from disparate sources, creating a unified information layer.\n\n"
                    "**Primary Functions**\n"
                    "- Data acquisition from multiple upstream dependencies\n"
                    "- Relationship mapping between entities and attributes\n"
                    "- API provisioning for downstream applications\n\n"
                    "**Operational Lifecycle**\n"
                    "Begins with initial deployment and schema configuration, transitions to steady-state ingestion with periodic reindexing, and includes continuous monitoring for anomalies.\n\n"
                    "**Risk Management**\n"
                    "Quality assurance through validation pipelines; schema versioning to handle evolution gracefully.\n\n"
                    "**Performance Metrics**\n"
                    "Demonstrates value through reduced manual effort, faster query response times, and enhanced compliance capabilities."
                ),
                (
                    f"# Deep Dive: {product}\n\n"
                    f"In the context of {cfg.company_name}'s {cfg.domain_name} operations, {product} represents a critical architectural component.\n\n"
                    "## Strategic Purpose\n"
                    f"{product} bridges the gap between raw data sources and business intelligence consumers, providing a semantic layer that understands {cfg.domain_name} concepts.\n\n"
                    "## Responsibilities\n"
                    "1. Continuous data ingestion from source systems\n"
                    "2. Entity resolution and relationship construction\n"
                    "3. Query interface for downstream analytics\n\n"
                    "## Lifecycle Management\n"
                    "The platform requires initial bootstrapping with schema definitions, followed by incremental updates and periodic full reindexing to maintain data freshness.\n\n"
                    "## Risk Profile\n"
                    "Primary concerns include data quality degradation and schema drift; both are addressed through automated validation and controlled change management.\n\n"
                    "## Business Impact\n"
                    "Measurable improvements in operational efficiency, reduced time-to-insight, and stronger audit trails for compliance purposes."
                ),
                (
                    f"Let me analyze {product} comprehensively:\n\n"
                    f"**Purpose**: {product} serves as the data intelligence backbone for {cfg.company_name}'s {cfg.domain_name} platform, transforming fragmented information into coherent knowledge.\n\n"
                    "**Architecture**: Built on a multi-layer design where ingestion pipelines feed into a graph-based entity store, which then exposes structured APIs for consumption.\n\n"
                    "**Operations**: Runs continuously with scheduled reindexing jobs, real-time event processing, and proactive monitoring for data quality and system health.\n\n"
                    "**Challenges**: Must handle diverse data formats, evolving schemas, and scale to accommodate growing data volumes while maintaining query performance.\n\n"
                    "**Value Delivery**: Quantifiable through reduced manual data wrangling, faster decision cycles, improved accuracy in reporting, and streamlined compliance workflows."
                ),
                (
                    f"## Entity Analysis: {product}\n\n"
                    f"### Functional Role\n"
                    f"{product} operates as a centralized data fabric within {cfg.company_name}, specifically tailored for {cfg.domain_name}.\n\n"
                    "### Technical Implementation\n"
                    "Combines vector embeddings for semantic search with graph structures for relationship traversal, supported by batch and stream processing pipelines.\n\n"
                    "### Evolution Path\n"
                    "Initial deployment focuses on core entity types and relationships. Subsequent phases add more sophisticated reasoning, expanded source coverage, and enhanced query capabilities.\n\n"
                    "### Control Mechanisms\n"
                    "Employs data validation at ingestion, schema governance through version control, and observability tools for anomaly detection.\n\n"
                    "### Success Indicators\n"
                    "Tracks query latency, data freshness, coverage metrics, user adoption rates, and downstream impact on business processes."
                ),
                (
                    f"**Detailed Breakdown of {product}**\n\n"
                    f"*Role*: {product} acts as the foundational data layer for {cfg.domain_name} at {cfg.company_name}.\n\n"
                    "*Capabilities*: Ingests structured and unstructured data, extracts entities and relationships, maintains temporal history, and serves queries via REST and GraphQL interfaces.\n\n"
                    "*Deployment*: Follows a phased approach starting with pilot datasets, expanding to full production with redundancy and failover mechanisms.\n\n"
                    "*Vulnerabilities*: Susceptible to upstream data quality issues and schema incompatibilities; addressed through defensive ingestion strategies and schema validation.\n\n"
                    "*Outcomes*: Drives measurable improvements in data accessibility, analysis speed, regulatory compliance, and overall operational intelligence."
                ),
                (
                    f"### Comprehensive View: {product}\n\n"
                    f"**Mission**: To serve as the authoritative data intelligence platform for {cfg.domain_name} within {cfg.company_name}.\n\n"
                    "**Components**: Ingestion layer (connectors to source systems), transformation layer (entity extraction and enrichment), storage layer (vector + graph databases), and API layer (query interfaces).\n\n"
                    "**Timeline**: Initialization → Data onboarding → Continuous operation → Periodic optimization → Ongoing enhancement.\n\n"
                    "**Threat Model**: Data corruption, schema conflicts, performance degradation under load; mitigated through checksums, validation rules, and capacity planning.\n\n"
                    "**Impact Assessment**: Positive effects on query response time, data-driven decision quality, compliance posture, and reduction in manual data tasks."
                ),
            ]
            output = output_templates[(idx * 11) % len(output_templates)]

            metadata = make_metadata(
                section="entity_reasoning_depth",
                index=idx,
                complexity="high",
                tags=["entity_reasoning", "deep_explanation", "kpi"],
                reasoning_mode="multi_paragraph",
                entity=product,
            )

            examples.append({
                "system": system,
                "instruction": instruction,
                "input": "",
                "output": output,
                "metadata": metadata,
            })

        return examples
