from typing import List, Dict, Any
from pydantic import BaseModel
from .qa_engine import BrandGovernanceValidator, QAResult


class ShotInstruction(BaseModel):
    scene_id: int
    duration_sec: int
    camera_movement: str
    visual_prompt: str
    negative_prompt: str
    audio_ambience: str
    voiceover_script: str
    qa_report: QAResult


class CampaignManifest(BaseModel):
    campaign_name: str
    target_aspect_ratio: str
    total_estimated_duration_sec: int
    scenes: List[ShotInstruction]
    overall_qa_pass: bool


class PipelineOrchestrator:
    def __init__(self):
        self.validator = BrandGovernanceValidator()

    def generate_campaign_manifest(
        self,
        campaign_name: str,
        brief_objective: str,
        visual_style: str,
        aspect_ratio: str,
        scenes_count: int = 3
    ) -> CampaignManifest:
        scenes: List[ShotInstruction] = []
        overall_pass = True

        scene_templates = [
            {
                "camera": "stabilized dolly-in push",
                "focus": "Establishing character posture and authoritative workspace setting",
                "audio": "Deep resonant industrial server room tone with soft cinematic drone",
                "vo": "A verdadeira inovação começa onde o método encontra a escala técnica."
            },
            {
                "camera": "smooth 90-degree orbital tracking arc",
                "focus": "Close-up on interface interaction and micro-precision mechanics",
                "audio": "Crisp electronic synthesizer pulses and subtle haptic Foley",
                "vo": "Cada frame precisa ser desenhado com controle absoluto de física e luz."
            },
            {
                "camera": "slow pull-out revealing cinematic silhouette",
                "focus": "Product hero framing and final brand call-to-action lock",
                "audio": "Uptempo electronic riser resolving on a clean, crystalline bell chime",
                "vo": "Não aceite o mediano. Eleve o posicionamento da sua marca agora."
            }
        ]

        total_scenes = min(scenes_count, len(scene_templates))

        for idx in range(total_scenes):
            template = scene_templates[idx]
            
            prompt = (
                f"Cinematic {aspect_ratio} shot. Subject in a {visual_style} aesthetic. "
                f"{template['focus']}. Camera executes a {template['camera']}. "
                f"Volumetric warm amber rim lighting paired with cyan accents. Photorealistic 35mm film."
            )
            
            neg_prompt = (
                "jitter, bent limbs, identity drift, subtitles, text watermark, "
                "cartoon, 3d render, plastic skin, blurry eyes, deformed hands"
            )

            qa_res = self.validator.validate_scene_prompt(
                prompt=prompt,
                negative_prompt=neg_prompt,
                duration=8,
                aspect_ratio=aspect_ratio
            )

            if not qa_res.is_valid:
                overall_pass = False

            scenes.append(
                ShotInstruction(
                    scene_id=idx + 1,
                    duration_sec=8,
                    camera_movement=template["camera"],
                    visual_prompt=prompt,
                    negative_prompt=neg_prompt,
                    audio_ambience=template["audio"],
                    voiceover_script=template["vo"],
                    qa_report=qa_res
                )
            )

        return CampaignManifest(
            campaign_name=campaign_name,
            target_aspect_ratio=aspect_ratio,
            total_estimated_duration_sec=len(scenes) * 8,
            scenes=scenes,
            overall_qa_pass=overall_pass
        )
