import os
import json
from typing import List, Optional
from pydantic import BaseModel, Field
from core.qa_engine import BrandQAEngine, QAReport

try:
    import streamlit as st
    STREAMLIT_AVAILABLE = True
except ImportError:
    STREAMLIT_AVAILABLE = False

try:
    import google.generativeai as genai
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False

class SceneManifest(BaseModel):
    scene_id: int
    duration_sec: int = Field(default=8, le=8)
    camera_movement: str
    visual_prompt: str
    negative_prompt: str
    audio_ambience: str
    voiceover_script: str
    qa_report: Optional[QAReport] = None

class CampaignManifest(BaseModel):
    campaign_name: str
    target_aspect_ratio: str
    total_estimated_duration_sec: int
    engine_source: str
    security_passed: bool
    security_notes: List[str] = Field(default_factory=list)
    scenes: List[SceneManifest]
    overall_qa_pass: bool

class CreativePipelineOrchestrator:
    def __init__(self):
        self.api_key = self._resolve_api_key()
        self.ai_enabled = False
        if self.api_key and GENAI_AVAILABLE:
            try:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel("gemini-2.5-flash")
                self.ai_enabled = True
            except Exception:
                self.ai_enabled = False

    def _resolve_api_key(self) -> Optional[str]:
        if STREAMLIT_AVAILABLE:
            try:
                if "GEMINI_API_KEY" in st.secrets:
                    return st.secrets["GEMINI_API_KEY"]
            except Exception:
                pass
        return os.environ.get("GEMINI_API_KEY")

    def execute_pipeline(self, brief: str, campaign_name: str, aspect_ratio: str, num_scenes: int, visual_aesthetic: str) -> CampaignManifest:
        # Step 1: Security & Prompt Injection Audit
        sec_passed, sec_findings = BrandQAEngine.audit_security(brief)
        if not sec_passed:
            blocked_scene = SceneManifest(
                scene_id=1,
                duration_sec=0,
                camera_movement="BLOCKED",
                visual_prompt="PIPELINE BLOCKED: Input triggered safety guardrails.",
                negative_prompt="malicious_payload",
                audio_ambience="None",
                voiceover_script="Execution halted due to adversarial prompt injection detection.",
                qa_report=QAReport(
                    is_valid=False,
                    score=0,
                    violations=sec_findings,
                    recommendations=["Remove adversarial or override keywords from the executive brief."]
                )
            )
            return CampaignManifest(
                campaign_name=campaign_name,
                target_aspect_ratio=aspect_ratio,
                total_estimated_duration_sec=0,
                engine_source="Security Guardrail Interceptor",
                security_passed=False,
                security_notes=sec_findings,
                scenes=[blocked_scene],
                overall_qa_pass=False
            )

        # Step 2: Generation (Gemini AI or Deterministic Fallback)
        scenes = []
        engine_used = "Deterministic Production Rulebase"

        if self.ai_enabled:
            ai_scenes = self._generate_with_gemini(brief, aspect_ratio, num_scenes, visual_aesthetic)
            if ai_scenes:
                scenes = ai_scenes
                engine_used = "Gemini 2.5 Flash Enterprise Engine"

        if not scenes:
            scenes = self._generate_deterministic(aspect_ratio, num_scenes, visual_aesthetic)

        # Step 3: Run Deterministic QA Engine on every scene
        all_passed = True
        for scene in scenes:
            report = BrandQAEngine.audit_scene(
                prompt=scene.visual_prompt,
                negative_prompt=scene.negative_prompt,
                duration_sec=scene.duration_sec,
                aspect_ratio=aspect_ratio
            )
            scene.qa_report = report
            if not report.is_valid:
                all_passed = False

        return CampaignManifest(
            campaign_name=campaign_name,
            target_aspect_ratio=aspect_ratio,
            total_estimated_duration_sec=len(scenes) * 8,
            engine_source=engine_used,
            security_passed=True,
            security_notes=["Input brief passed all OWASP prompt injection guardrails."],
            scenes=scenes,
            overall_qa_pass=all_passed
        )

    def _generate_with_gemini(self, brief: str, aspect_ratio: str, num_scenes: int, visual_aesthetic: str) -> Optional[List[SceneManifest]]:
        prompt = f"""
You are the Lead CreativeOps & Multimodal AI Director for a high-end enterprise creative pipeline.
Deconstruct this brief into exactly {num_scenes} sequential scenes for SOTA generative video models (Veo 3.1 / Kling 3.0).

Parameters:
- Campaign Intent: {brief}
- Target Aspect Ratio: {aspect_ratio}
- Visual Style / Grade: {visual_aesthetic}
- Scene Duration Rule: Maximum 8 seconds per scene for diffusion stability.

Return ONLY a valid JSON array of objects with these exact keys:
[
  {{
    "scene_id": 1,
    "duration_sec": 8,
    "camera_movement": "explicit camera motion (e.g. stabilized dolly-in push, orbital tracking arc)",
    "visual_prompt": "Cinematic shot description including subject, action, lighting, camera lens and aesthetic",
    "negative_prompt": "jitter, bent limbs, identity drift, subtitles, text watermark, cartoon, 3d render, plastic skin, blurry eyes, deformed hands",
    "audio_ambience": "Foley and ambient sound description",
    "voiceover_script": "Short authoritative voiceover line"
  }}
]
"""
        try:
            response = self.model.generate_content(
                prompt,
                generation_config={"response_mime_type": "application/json"}
            )
            data = json.loads(response.text)
            scenes = [SceneManifest(**item) for item in data]
            return scenes[:num_scenes]
        except Exception:
            return None

    def _generate_deterministic(self, aspect_ratio: str, num_scenes: int, visual_aesthetic: str) -> List[SceneManifest]:
        presets = [
            ("stabilized dolly-in push", "Establishing character posture and authoritative workspace setting.", "Deep resonant industrial server room tone with soft cinematic drone", "A verdadeira inovação começa onde o método encontra a escala técnica."),
            ("smooth 90-degree orbital tracking arc", "Close-up on interface interaction and micro-precision mechanics.", "Crisp electronic synthesizer pulses and subtle haptic Foley", "Cada frame precisa ser desenhado com controle absoluto de física e luz."),
            ("slow pull-out revealing cinematic silhouette", "Product hero framing and final brand call-to-action lock.", "Uptempo electronic riser resolving on a clean, crystalline bell chime", "Não aceite o mediano. Eleve o posicionamento da sua marca agora.")
        ]
        scenes = []
        for i in range(num_scenes):
            cam, act, sfx, vo = presets[i % len(presets)]
            prompt = f"Cinematic {aspect_ratio} shot. Subject in a {visual_aesthetic} aesthetic. {act} Camera executes a {cam}. Volumetric warm amber rim lighting paired with cyan accents. Photorealistic 35mm film."
            neg = "jitter, bent limbs, identity drift, subtitles, text watermark, cartoon, 3d render, plastic skin, blurry eyes, deformed hands"
            scenes.append(SceneManifest(
                scene_id=i + 1,
                duration_sec=8,
                camera_movement=cam,
                visual_prompt=prompt,
                negative_prompt=neg,
                audio_ambience=sfx,
                voiceover_script=vo
            ))
        return scenes
