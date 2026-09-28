import re
from typing import List, Dict, Any
from pydantic import BaseModel, Field


class QAResult(BaseModel):
    is_valid: bool
    score: int = Field(ge=0, le=100)
    passed_checks: List[str]
    violations: List[str]
    recommendations: List[str]


class BrandGovernanceValidator:
    def __init__(self, brand_rules: Dict[str, Any] = None):
        self.rules = brand_rules or {
            "forbidden_words": ["ugly", "cheap", "plastic", "deformed", "cartoonish", "glitchy"],
            "required_negatives": ["jitter", "bent limbs", "identity drift", "subtitles", "text watermark"],
            "max_scene_duration_sec": 8,
            "required_camera_keywords": ["dolly", "pan", "tilt", "orbit", "static", "tracking", "crane", "push-in", "pull-out"],
            "supported_ratios": ["16:9", "9:16", "3:4", "1:1"]
        }

    def validate_scene_prompt(self, prompt: str, negative_prompt: str, duration: int, aspect_ratio: str) -> QAResult:
        passed = []
        violations = []
        recommendations = []
        score = 100

        # Validação de Aspect Ratio
        if aspect_ratio in self.rules["supported_ratios"]:
            passed.append(f"Aspect ratio '{aspect_ratio}' is compliant.")
        else:
            violations.append(f"Invalid aspect ratio '{aspect_ratio}'. Must be one of {self.rules['supported_ratios']}.")
            score -= 25

        # Verificação do limite de duração da cena para modelos generativos
        if duration <= self.rules["max_scene_duration_sec"]:
            passed.append(f"Scene duration ({duration}s) complies with <= 8s engine limit.")
        else:
            violations.append(f"Scene duration ({duration}s) exceeds engine threshold of {self.rules['max_scene_duration_sec']}s.")
            score -= 20

        # Filtro de vocabulário restrito no prompt positivo
        found_forbidden = [w for w in self.rules["forbidden_words"] if re.search(rf"\b{w}\b", prompt, re.IGNORECASE)]
        if not found_forbidden:
            passed.append("No forbidden brand vocabulary detected.")
        else:
            violations.append(f"Forbidden words detected: {', '.join(found_forbidden)}")
            score -= 25

        # Verificação de instrução explícita de câmera para evitar deriva
        has_camera_motion = any(re.search(rf"\b{cw}\b", prompt, re.IGNORECASE) for cw in self.rules["required_camera_keywords"])
        if has_camera_motion:
            passed.append("Explicit camera movement detected (avoids static drift).")
        else:
            recommendations.append("Consider adding explicit camera instruction (e.g., 'slow dolly-in', 'orbit').")
            score -= 10

        # Presença de guardrails mínimos no prompt negativo
        missing_negatives = [neg for neg in self.rules["required_negatives"] if neg.lower() not in negative_prompt.lower()]
        if not missing_negatives:
            passed.append("All baseline quality negative tokens are present.")
        else:
            recommendations.append(f"Missing recommended negative guardrails: {', '.join(missing_negatives)}")
            score -= 15

        score = max(score, 0)
        is_valid = len(violations) == 0 and score >= 70

        return QAResult(
            is_valid=is_valid,
            score=score,
            passed_checks=passed,
            violations=violations,
            recommendations=recommendations
        )
