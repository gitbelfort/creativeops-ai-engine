import re
from typing import List
from pydantic import BaseModel, Field

class QAReport(BaseModel):
    is_valid: bool
    score: int
    passed_checks: List[str] = Field(default_factory=list)
    violations: List[str] = Field(default_factory=list)
    recommendations: List[str] = Field(default_factory=list)

class BrandQAEngine:
    FORBIDDEN_TERMS = [
        "ugly", "deformed", "bad quality", "lowres", "amateur",
        "nsfw", "nude", "violence", "blood", "cheap", "glitch"
    ]
    
    INJECTION_PATTERNS = [
        r"ignore\s+(all\s+|previous\s+|prior\s+)?instructions",
        r"disregard\s+(all\s+|previous\s+)?instructions",
        r"system\s+override",
        r"you\s+are\s+now\s+(unfiltered|dan|evil)",
        r"jailbreak",
        r"reveal\s+(your\s+)?(system\s+prompt|instructions)",
        r"bypass\s+rules",
        r"<script>",
        r"DROP\s+TABLE"
    ]

    @classmethod
    def audit_security(cls, text: str) -> tuple[bool, List[str]]:
        """Scans input text for adversarial prompt injection attempts."""
        findings = []
        for pattern in cls.INJECTION_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                findings.append(f"Prompt Injection Signature Detected: match for '{pattern}'")
        return (len(findings) == 0, findings)

    @classmethod
    def audit_scene(cls, prompt: str, negative_prompt: str, duration_sec: int, aspect_ratio: str) -> QAReport:
        passed = []
        violations = []
        recommendations = []
        score = 100

        # Aspect Ratio Validation
        if aspect_ratio in ["9:16", "16:9", "1:1", "4:5"]:
            passed.append(f"Aspect ratio '{aspect_ratio}' is compliant.")
        else:
            violations.append(f"Invalid aspect ratio '{aspect_ratio}'.")
            score -= 30

        # Duration validation (SOTA diffusion model sweet spot: <= 8s)
        if duration_sec <= 8:
            passed.append(f"Scene duration ({duration_sec}s) complies with <= 8s engine limit.")
        else:
            violations.append(f"Scene duration ({duration_sec}s) exceeds stability threshold (max 8s).")
            score -= 25

        # Forbidden brand vocabulary check
        prompt_lower = prompt.lower()
        found_forbidden = [w for w in cls.FORBIDDEN_TERMS if w in prompt_lower]
        if not found_forbidden:
            passed.append("No forbidden brand vocabulary detected.")
        else:
            violations.append(f"Forbidden terms detected: {', '.join(found_forbidden)}")
            score -= 30

        # Camera movement requirement check
        camera_keywords = ["pan", "tilt", "dolly", "tracking", "zoom", "orbital", "pull-out", "push-in", "static", "crane", "handheld"]
        if any(w in prompt_lower for w in camera_keywords):
            passed.append("Explicit camera movement detected (avoids static drift).")
        else:
            violations.append("Missing explicit camera motion keyword.")
            recommendations.append("Add a camera motion direction (e.g. 'orbital tracking', 'dolly-in').")
            score -= 15

        # Essential negative constraints check
        neg_lower = negative_prompt.lower()
        essential_negatives = ["jitter", "drift", "watermark", "subtitles"]
        missing_negatives = [n for n in essential_negatives if n not in neg_lower]
        if not missing_negatives:
            passed.append("All baseline quality negative tokens are present.")
        else:
            violations.append(f"Missing negative guardrails: {', '.join(missing_negatives)}")
            recommendations.append(f"Append negative tokens: {', '.join(missing_negatives)}")
            score -= 10

        final_score = max(0, score)
        return QAReport(
            is_valid=(final_score >= 80 and len(violations) == 0),
            score=final_score,
            passed_checks=passed,
            violations=violations,
            recommendations=recommendations
        )
