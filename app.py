import json
import streamlit as st
from core.orchestrator import PipelineOrchestrator

st.set_page_config(
    page_title="CreativeOps Engine | AI Transformation Pipeline",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 CreativeOps Engine")
st.caption("Enterprise AI Video Pipeline & Brand Governance Orchestrator | Developed by Charles Belfort")

st.markdown("""
This system translates high-level marketing briefs into **validated, production-grade multimodal manifests** 
tailored for next-generation generative video architectures (Veo 3.1, Seedance 2.5, Kling 3.0).
""")

# Painel lateral de configuração da campanha
st.sidebar.header("Campaign Parameters")
campaign_name = st.sidebar.text_input("Campaign Name", value="Cyberpunk Coffee Launch")
aspect_ratio = st.sidebar.selectbox("Aspect Ratio", options=["16:9", "9:16", "3:4", "1:1"], index=1)
scenes_count = st.sidebar.slider("Number of Scenes", min_value=1, max_value=3, value=3)

visual_style = st.sidebar.selectbox(
    "Visual Aesthetics",
    options=[
        "Dark Brutalist High-Tech Studio with Volumetric Neons",
        "Hyper-Realistic Luxury Macro Commercial",
        "Gritty Industrial Fabrication Plant with Tungsten Rim Lighting",
        "Vibrant Modern Agency Streetwear Look"
    ]
)

brief_objective = st.text_area(
    "Executive Brief Intent",
    value="Launch a high-energy B2B promotional campaign proving technical authority and physical realism without manual studio overhead."
)

if st.button("🚀 Orchestrate & Validate Pipeline", type="primary"):
    orchestrator = PipelineOrchestrator()
    manifest = orchestrator.generate_campaign_manifest(
        campaign_name=campaign_name,
        brief_objective=brief_objective,
        visual_style=visual_style,
        aspect_ratio=aspect_ratio,
        scenes_count=scenes_count
    )

    st.subheader(f"Pipeline Result: {manifest.campaign_name}")
    
    col1, col2 = st.columns(2)
    col1.metric("Total Duration", f"{manifest.total_estimated_duration_sec}s")
    status_label = "✅ Compliant (Ready for Dispatch)" if manifest.overall_qa_pass else "⚠️ Flagged by Governance"
    col2.metric("Brand QA Status", status_label)

    st.divider()

    for scene in manifest.scenes:
        with st.expander(f"Scene {scene.scene_id} - Duration: {scene.duration_sec}s | Camera: {scene.camera_movement}", expanded=True):
            col_left, col_right = st.columns([3, 2])
            
            with col_left:
                st.markdown("**Visual Shot Prompt (English Engine Command):**")
                st.code(scene.visual_prompt, language="markdown")
                
                st.markdown("**Negative Constraints Guardrail:**")
                st.code(scene.negative_prompt, language="text")
                
                st.markdown(f"**Sound Design / SFX Ambience:** `{scene.audio_ambience}`")
                st.markdown(f"**Voiceover Script:** *\"{scene.voiceover_script}\"*")

            with col_right:
                st.markdown("#### Quality & Governance Audit")
                st.metric("Adherence Score", f"{scene.qa_report.score}/100")
                
                if scene.qa_report.passed_checks:
                    st.success("**Passed Rules:**\n- " + "\n- ".join(scene.qa_report.passed_checks))
                
                if scene.qa_report.violations:
                    st.error("**Rule Violations:**\n- " + "\n- ".join(scene.qa_report.violations))
                
                if scene.qa_report.recommendations:
                    st.warning("**Optimization Notes:**\n- " + "\n- ".join(scene.qa_report.recommendations))

    st.divider()
    st.subheader("📦 Exportable JSON Manifest (Cloud API Ready)")
    st.json(manifest.model_dump())
