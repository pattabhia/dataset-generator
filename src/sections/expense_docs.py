# dataset_generator/sections/expense_docs.py

from __future__ import annotations

from typing import Any, Dict, List

from .base import SectionBuilder
from ..utils import default_currencies, default_expense_doc_types, make_metadata


class ExpenseDocumentsTrainingBuilder(SectionBuilder):
    """New: Expense documents dataset (invoices, bills, receipts...)."""

    @property
    def file_name(self) -> str:
        return "expense_documents_training.json"

    def build_examples(self) -> List[Dict[str, Any]]:
        cfg = self.config
        n = 150
        examples: List[Dict[str, Any]] = []

        doc_types = default_expense_doc_types(cfg)
        currencies = default_currencies(cfg)

        for idx in range(1, n + 1):
            doc_type = doc_types[idx % len(doc_types)]
            currency = currencies[idx % len(currencies)]
            invoice_no = f"{doc_type[:3].upper()}-{2025}{idx:04d}"
            vendor = f"Vendor {idx:03d} Pvt Ltd"

            raw_doc = (
                f"{doc_type} Number: {invoice_no}\n"
                f"Vendor: {vendor}\n"
                f"Date: 2025-10-{(idx % 28) + 1:02d}\n"
                f"Amount: {currency} {1000 + idx * 5:.2f}\n"
                "Description: Taxi ride from airport to office\n"
                "GST: 18%\n"
            )

            system = (
                f"You are {cfg.agent_name}, specialized in {cfg.domain_name}. "
                "Given an invoice/bill/receipt, extract normalized fields and explain if it "
                "is compliant with basic policy rules (only high-level, no real legal advice)."
            )

            # Introduce variation in extraction task phrasing
            if doc_type.lower() in ["invoice", "bill"]:
                task_templates = [
                    "Extract and normalize all key fields from this document.",
                    "Identify and standardize each important field in this document.",
                    "List all critical fields from this document in a structured format.",
                ]
            else:
                task_templates = [
                    "Identify key fields and classify this document type.",
                    "Classify this document and extract its key attributes.",
                    "Determine the document type and capture essential fields.",
                ]
            task = task_templates[idx % len(task_templates)]
            instruction = f"{task} Document type: {doc_type}."

            output = {
                "document_type": doc_type,
                "invoice_number": invoice_no,
                "vendor_name": vendor,
                "currency": currency,
                "amount": round(1000 + idx * 5, 2),
                "transaction_date": f"2025-10-{(idx % 28) + 1:02d}",
                "description": "Taxi ride from airport to office",
                "tax_rate": "18%",
                "policy_flags": [
                    "AUTO_APPROVE_IF_UNDER_LIMIT",
                    "REQUIRES_TRAVEL_CATEGORY_TAG"
                ]
            }

            metadata = make_metadata(
                section="expense_docs",
                index=idx,
                complexity="medium",
                tags=["invoice_parsing", "expense_docs", doc_type.lower()],
                reasoning_mode="extraction+classification",
                is_negative_example=False,
                is_synthetic=True,
                document_type=doc_type,
            )

            examples.append({
                "system": system,
                "instruction": instruction,
                "input": raw_doc,
                "output": output,
                "metadata": metadata
            })

        return examples
  