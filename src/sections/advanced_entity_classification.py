# dataset_generator/sections/advanced_entity_classification.py

from __future__ import annotations

import json
from typing import Any, Dict, List

from .base import SectionBuilder
from ..utils import make_metadata


class AdvancedEntityClassificationTrainingBuilder(SectionBuilder):
    """
    Section 12: Advanced Entity Classification

    - Multi-label classification
    - Overlapping categories (e.g., Vendor + ServiceProvider)
    - Confidence per label
    """

    @property
    def file_name(self) -> str:
        return "advanced_entity_classification_training.json"

    def build_examples(self) -> List[Dict[str, Any]]:
        cfg = self.config
        # Increased from 100 to 150 to account for deduplication
        n = 150
        examples: List[Dict[str, Any]] = []

        sample_entities = [
            ("ACME Cabs Pvt Ltd", ["Vendor", "ServiceProvider"]),
            ("Corporate Travel Policy 2025", ["ExpensePolicy", "Document"]),
            ("GL Account 5400 – Travel", ["GLAccount", "CostCenter"]),
            ("ACME Software FZ-LLC", ["Vendor", "TechnologyPartner"]),
            ("ACME Logistics LLC", ["Vendor", "Logistics"]),
            ("Project Phoenix 2024", ["Project", "ExpensePolicy"]),
            ("Vendor: Beta Travel Inc", ["Vendor", "ServiceProvider"]),
            ("GL Account 6200 – Marketing", ["GLAccount", "CostCenter"]),
            ("Enterprise SaaS License Agreement", ["ExpensePolicy", "Document", "Contract"]),
            ("Delta Consulting Group", ["Vendor", "ServiceProvider", "Consultant"]),
            ("Employee Travel Reimbursement Policy", ["ExpensePolicy", "Document"]),
            ("GL Account 7100 – R&D", ["GLAccount", "CostCenter", "Project"]),
            ("Omega Cloud Services Inc", ["Vendor", "TechnologyPartner", "CloudProvider"]),
            ("Project Atlas 2025", ["Project", "ExpensePolicy", "Initiative"]),
            ("Sigma Transportation Ltd", ["Vendor", "ServiceProvider", "Logistics"]),
            ("GL Account 5500 – Meals & Entertainment", ["GLAccount", "CostCenter"]),
            ("Corporate Card Usage Policy", ["ExpensePolicy", "Document", "FinancePolicy"]),
            ("Gamma Analytics Platform", ["Vendor", "TechnologyPartner", "SaaS"]),
            ("GL Account 8300 – Office Supplies", ["GLAccount", "CostCenter"]),
            ("Theta Legal Services PLLC", ["Vendor", "ServiceProvider", "Legal"]),
            ("Remote Work Equipment Policy", ["ExpensePolicy", "Document"]),
            ("Project Horizon Q1-2025", ["Project", "Initiative"]),
            ("Zeta Catering Services", ["Vendor", "ServiceProvider"]),
            ("GL Account 9100 – Training & Development", ["GLAccount", "CostCenter", "HR"]),
            ("Annual Conference Travel Policy", ["ExpensePolicy", "Document", "Event"]),
            ("Kappa IT Solutions Corp", ["Vendor", "TechnologyPartner", "Consultant"]),
            ("GL Account 5600 – Lodging", ["GLAccount", "CostCenter"]),
            ("Lambda Recruitment Partners", ["Vendor", "ServiceProvider", "HR"]),
            ("Expense Approval Workflow 2025", ["ExpensePolicy", "Document", "Process"]),
            ("Project Quantum Leap", ["Project", "Initiative", "Transformation"]),
            ("Epsilon Marketing Agency", ["Vendor", "ServiceProvider", "Marketing"]),
            ("GL Account 7200 – Software Licenses", ["GLAccount", "CostCenter", "Technology"]),
            ("Iota Facilities Management", ["Vendor", "ServiceProvider"]),
            ("Vendor Payment Terms Policy", ["ExpensePolicy", "Document", "FinancePolicy"]),
            ("GL Account 8500 – Telecommunications", ["GLAccount", "CostCenter"]),
            ("Nu Data Security Solutions", ["Vendor", "TechnologyPartner", "Security"]),
            ("Project Innovation Hub", ["Project", "Initiative", "R&D"]),
            ("Xi Event Planning Services", ["Vendor", "ServiceProvider", "Event"]),
            ("Per Diem Policy International", ["ExpensePolicy", "Document"]),
            ("GL Account 6300 – Advertising", ["GLAccount", "CostCenter", "Marketing"]),
            ("Omicron Healthcare Benefits", ["Vendor", "ServiceProvider", "HR"]),
            ("Capital Expenditure Policy", ["ExpensePolicy", "Document", "FinancePolicy"]),
            ("Rho Engineering Contractors", ["Vendor", "ServiceProvider", "Engineering"]),
            ("GL Account 9200 – Professional Development", ["GLAccount", "CostCenter", "HR"]),
            ("Tau Translation Services", ["Vendor", "ServiceProvider", "Consultant"]),
            ("Project Digital Transformation", ["Project", "Initiative", "Technology"]),
            ("Upsilon Shipping & Freight", ["Vendor", "Logistics", "ServiceProvider"]),
            ("Mileage Reimbursement Policy", ["ExpensePolicy", "Document"]),
            ("GL Account 5700 – Ground Transportation", ["GLAccount", "CostCenter"]),
            ("Phi Property Management LLC", ["Vendor", "ServiceProvider", "RealEstate"]),
        ]

        possible_labels = sorted(
            {label for _, labels in sample_entities for label in labels}
        )

        for idx in range(1, n + 1):
            raw_name, labels = sample_entities[idx % len(sample_entities)]

            system = (
                f"You are {cfg.agent_name} advanced classification module. "
                "Classify the entity into one or more labels, and assign a confidence "
                "score per label. If a label does not apply, its confidence should be low."
            )
            instruction = f"Classify the entity with multi-label output: {raw_name}"

            # Assign high confidence to correct labels and low to others. The values
            # alternate slightly with the index to introduce minor variation.
            label_confidences = {
                label: (0.85 if label in labels else 0.05 + 0.01 * (idx % 5))
                for label in possible_labels
            }

            output_dict = {
                "entity": raw_name,
                "multi_label": True,
                "predicted_labels": labels,
                "label_confidences": label_confidences,
            }

            meta = make_metadata(
                section="advanced_entity_classification",
                index=idx,
                complexity="medium",
                tags=["classification", "multi_label", "advanced"],
                reasoning_mode="classification",
                confidence=0.8,
                possible_labels=possible_labels,
            )

            examples.append({
                "system": system,
                "instruction": instruction,
                "input": raw_name,
                "output": json.dumps(output_dict, ensure_ascii=False),
                "metadata": meta,
            })

        return examples
