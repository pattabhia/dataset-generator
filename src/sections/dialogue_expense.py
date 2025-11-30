"""
dataset_generator/sections/dialogue_expense.py

This module defines a multi‑turn dialogue dataset builder for the expense domain. Unlike
the single‑turn question/answer pairs elsewhere in the generator, these examples
simulate realistic conversations between a user and the assistant across two or more
turns. The goal is to teach the model to handle follow‑up questions, maintain
context across turns and provide consistent, grounded answers.

Each example defines a ``system`` prompt that instructs the assistant on its
identity and behaviour, and an ``output`` list containing alternating user and
assistant messages. A common metadata structure is attached via ``make_metadata``.

The examples are intentionally synthetic but cover typical expense scenarios:
approvals, reimbursements and policy clarifications.
"""

from __future__ import annotations

from typing import Any, Dict, List

from .base import SectionBuilder
from ..utils import make_metadata


class DialogueExpenseTrainingBuilder(SectionBuilder):
    """Multi‑turn dialogue dataset for expense domain assistance."""

    @property
    def file_name(self) -> str:
        return "dialogue_expense_training.json"

    def build_examples(self) -> List[Dict[str, Any]]:
        cfg = self.config
        n = 60
        examples: List[Dict[str, Any]] = []

        # Predefined conversation patterns. Each pattern is a list of message dicts
        # alternating between user and assistant roles. Additional patterns can be
        # appended here to increase diversity.
        conversations = [
            [
                {"role": "user", "content": "Hi, can you tell me who approves expense reports above the threshold?"},
                {"role": "assistant", "content": "Under the expense policy, the Finance Controller must approve any report that exceeds the approval threshold."},
                {"role": "user", "content": "What happens if the Finance Controller is unavailable?"},
                {"role": "assistant", "content": "In that case, the request escalates to the CFO for approval."},
            ],
            [
                {"role": "user", "content": "How long does reimbursement take once a report is approved?"},
                {"role": "assistant", "content": "Typically reimbursements are processed within 3 to 5 business days after approval."},
                {"role": "user", "content": "And if there is a delay?"},
                {"role": "assistant", "content": "If there's a delay beyond the usual window, please contact Finance Ops so they can check the payment status."},
            ],
            [
                {"role": "user", "content": "Does the expense policy allow reimbursement for ride-hailing services?"},
                {"role": "assistant", "content": "Yes, local transportation like ride-hailing is covered if it's part of a business trip and receipts are provided."},
                {"role": "user", "content": "Is there a daily limit on ride-hailing?"},
                {"role": "assistant", "content": "Yes, the daily cap is INR 2,000 or the equivalent in your local currency."},
            ],
            [
                {"role": "user", "content": "Who should I contact to get clarity on a rejected expense?"},
                {"role": "assistant", "content": "You should reach out to the Expense Ops Lead or Finance Controller to understand why it was rejected."},
                {"role": "user", "content": "Can I resubmit the report after correction?"},
                {"role": "assistant", "content": "Absolutely. After addressing the feedback, you can resubmit the report through the same system."},
            ],
            [
                {"role": "user", "content": "What receipts are required for a business lunch reimbursement?"},
                {"role": "assistant", "content": "For business lunch reimbursements, you need the itemized receipt and the payment confirmation showing the amount paid."},
                {"role": "user", "content": "Are there any spending limits?"},
                {"role": "assistant", "content": "Yes, lunch reimbursements are capped at INR 1,500 per person unless pre-approved by Finance."},
            ],
            [
                {"role": "user", "content": "Can I claim a taxi ride from home to the airport?"},
                {"role": "assistant", "content": "Yes, airport transfers are reimbursable as long as they are part of an approved business trip."},
                {"role": "user", "content": "What documentation is needed?"},
                {"role": "assistant", "content": "You should provide the ride receipt and a note linking it to the business trip itinerary."},
            ],
        ]

        # Build n examples by cycling through conversation patterns
        for idx in range(1, n + 1):
            conv = conversations[idx % len(conversations)]
            system = (
                f"You are {cfg.agent_name}, an expert assistant for {cfg.domain_name}. "
                "Maintain context across turns and provide concise, policy‑aware answers to follow‑up questions."
            )
            # Use empty instruction and input to focus on messages
            instruction = ""
            input_text = ""
            output = conv  # store conversation list as output (validated by utils)

            metadata = make_metadata(
                section="dialogue_expense",
                index=idx,
                complexity="medium",
                tags=["dialogue", "expense", "multi_turn"],
                reasoning_mode="multi_turn",
            )

            examples.append({
                "system": system,
                "instruction": instruction,
                "input": input_text,
                "output": output,
                "metadata": metadata,
            })

        return examples