# dataset_generator/sections/resume_intelligence.py

from __future__ import annotations

import json
from typing import Any, Dict, List

from .base import SectionBuilder
from ..utils import make_metadata


class ResumeIntelligenceTrainingBuilder(SectionBuilder):
    """
    Section 9: Resume Intelligence (Work, Skills, Timeline)

    Teaches the model to:
    - Parse resume-like text
    - Extract structured timeline
    - Identify roles, companies, skills
    - Answer HR-style questions later
    """

    @property
    def file_name(self) -> str:
        return "resume_intelligence_training.json"

    def build_examples(self) -> List[Dict[str, Any]]:
        cfg = self.config
        n = 120
        examples: List[Dict[str, Any]] = []

        base_skills = [
            "Java", "Spring Boot", "PostgreSQL", "Kafka",
            "AWS", "Microservices", "React", "Python",
        ]

        # Provide multiple instruction phrases for variety
        instruction_templates = [
            "Extract structured resume information from the following text.",
            "Parse the CV below and return a JSON summary of the candidate's professional history.",
            "Read the resume and produce a structured representation of the person's work experience, education and skills.",
        ]

        for idx in range(1, n + 1):
            name = f"Candidate {idx:03d}"
            role = "Senior Software Engineer" if idx % 2 == 0 else "Solution Architect"
            company = f"Acme Corp {idx % 7 + 1}"
            years = 6 + (idx % 5)
            # Ensure at least 4 skills to avoid empty lists
            skills = base_skills[: (idx % len(base_skills)) or 4]

            resume_text = (
                f"{name} is a {role} with around {years} years of experience. "
                f"Currently working at {company}, focusing on {', '.join(skills[:3])}. "
                "Previously led multiple projects, owning design, implementation, and delivery."
            )

            system = (
                f"You are {cfg.agent_name}, a resume intelligence module. "
                "Given free-form resume text, extract a normalized JSON structure capturing "
                "personal, professional, timeline, and skills information."
            )

            # Choose an instruction template
            instruction = instruction_templates[idx % len(instruction_templates)]

            output_dict = {
                "name": name,
                "current_title": role,
                "current_company": company,
                "total_experience_years": years,
                "skills": skills,
                "summary": (
                    f"{name} has {years} years of experience, currently working as a {role} at "
                    f"{company}, with strong skills in {', '.join(skills)}."
                ),
                "timeline": [
                    {
                        "role": role,
                        "company": company,
                        "start_year": 2018,
                        "end_year": None,
                        "highlights": [
                            "Led key delivery projects",
                            "Owned design and implementation",
                        ],
                    }
                ],
            }

            metadata = make_metadata(
                section="resume_intelligence",
                index=idx,
                complexity="medium",
                tags=["resume", "extraction", "timeline", "skills"],
                reasoning_mode="extraction",
                is_negative_example=False,
                is_synthetic=True,
            )

            examples.append({
                "system": system,
                "instruction": instruction,
                "input": resume_text,
                "output": json.dumps(output_dict, ensure_ascii=False),
                "metadata": metadata,
            })

        return examples
