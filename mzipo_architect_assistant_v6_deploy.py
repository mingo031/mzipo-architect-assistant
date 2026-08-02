"""
Mzipo Architect Assistant - Version 6 (Deployment Ready)
=======================================================
This version is prepared for Streamlit Community Cloud.

IMPORTANT:
- Do NOT put your real API key in this file.
- The API key must be added as a Secret in Streamlit Cloud.
"""

import streamlit as st
from openai import OpenAI
from datetime import datetime
import requests
from typing import Optional

# ============================================
# PAGE CONFIG
# ============================================
st.set_page_config(
    page_title="Mzipo Architect Assistant",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# PREMIUM DARK THEME
# ============================================
st.markdown("""
<style>
    .stApp {
        background-color: #0e0e0e;
        color: #e8e8e8;
    }
    section[data-testid="stSidebar"] {
        background-color: #141414;
        border-right: 1px solid #2a2a2a;
    }
    .main-title {
        font-size: 2.4rem;
        font-weight: 700;
        color: #ffffff;
        letter-spacing: -0.5px;
        margin-bottom: 0.1rem;
    }
    .main-subtitle {
        font-size: 1.05rem;
        color: #8a8a8a;
        margin-bottom: 1.6rem;
    }
    .section-title {
        font-size: 1.25rem;
        font-weight: 600;
        color: #ffffff;
        margin-top: 1.8rem;
        margin-bottom: 0.7rem;
        padding-bottom: 0.35rem;
        border-bottom: 1px solid #2f2f2f;
    }
    .stTextArea textarea {
        background-color: #1a1a1a !important;
        color: #e8e8e8 !important;
        border: 1px solid #333 !important;
        border-radius: 8px !important;
    }
    .stButton > button[kind="primary"] {
        background-color: #1F4E79;
        border: none;
        border-radius: 6px;
    }
    .stButton > button[kind="primary"]:hover {
        background-color: #2a6aa3;
    }
    .status-live {
        background-color: #0f2318;
        color: #4ade80;
        border: 1px solid #166534;
        padding: 0.4rem 0.85rem;
        border-radius: 6px;
        font-size: 0.85rem;
        font-weight: 500;
        display: inline-block;
    }
    .info-card {
        background-color: #161616;
        border: 1px solid #2a2a2a;
        border-radius: 10px;
        padding: 1.1rem 1.3rem;
        margin-bottom: 1.3rem;
        color: #cfcfcf;
        font-size: 0.93rem;
        line-height: 1.55;
    }
    .prompt-box {
        background-color: #1a1a1a;
        border: 1px solid #333;
        border-radius: 8px;
        padding: 0.9rem 1.1rem;
        margin-top: 0.5rem;
        margin-bottom: 1rem;
        font-family: monospace;
        font-size: 0.88rem;
        color: #d0d0d0;
        white-space: pre-wrap;
        line-height: 1.45;
    }
    .sidebar-title {
        font-size: 1.15rem;
        font-weight: 600;
        color: #ffffff;
    }
    .sidebar-sub {
        font-size: 0.85rem;
        color: #777;
        margin-bottom: 1.2rem;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ============================================
# GET API KEY FROM STREAMLIT SECRETS
# ============================================
def get_api_key():
    try:
        return st.secrets["XAI_API_KEY"]
    except Exception:
        return None

# ============================================
# SIDEBAR
# ============================================
with st.sidebar:
    st.markdown('<div class="sidebar-title">Mzipo Architect</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-sub">Version 6 • Deployed</div>', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("**Workflow**")
    st.markdown("""
    1. Write Project Brief  
    2. Generate Concept + Prompts  
    3. Generate 2D or 3D images  
    4. Experiment in Prompt Lab
    """)
    st.markdown("---")
    st.markdown('<div class="status-live">● Live • Full Control</div>', unsafe_allow_html=True)
    st.markdown("---")
    st.caption("Mzipo Architectural Solution\nDurban, South Africa")

# ============================================
# HEADER
# ============================================
st.markdown('<div class="main-title">Mzipo Architect Assistant</div>', unsafe_allow_html=True)
st.markdown('<div class="main-subtitle">Professional concepts • Clean floor plans • 3D renders</div>', unsafe_allow_html=True)

st.markdown("""
<div class="info-card">
Write a detailed brief → Generate the architectural concept and ready-to-use prompts → 
Then generate the actual 2D floor plan or 3D exterior when you want.
</div>
""", unsafe_allow_html=True)

# ============================================
# SESSION STATE
# ============================================
if "concept_text" not in st.session_state:
    st.session_state.concept_text = None
if "prompt_2d" not in st.session_state:
    st.session_state.prompt_2d = None
if "prompt_3d" not in st.session_state:
    st.session_state.prompt_3d = None

# ============================================
# 1. PROJECT BRIEF
# ============================================
st.markdown('<div class="section-title">1. Project Brief</div>', unsafe_allow_html=True)

default_brief = """I need a modern single-storey four-bedroom house for a family in Durban.

Requirements:
- Open-plan kitchen, dining and lounge
- Master bedroom with en-suite and walk-in closet
- Three additional bedrooms
- Double garage
- Butterfly roof style
- Clean modern look with white walls, dark cladding and timber accents
- Large glass sliding doors to the garden from the living area
- Covered outdoor patio at the back
- Suitable for a typical suburban plot in eThekwini"""

user_brief = st.text_area(
    "Describe the house in detail:",
    value=default_brief,
    height=210,
    label_visibility="collapsed"
)

# ============================================
# HELPERS
# ============================================
def get_client(api_key: str):
    return OpenAI(api_key=api_key, base_url="https://api.x.ai/v1")

def generate_concept_and_prompts(brief: str, api_key: str):
    client = get_client(api_key)

    system_prompt = """You are Mzipo Architect Assistant — a professional residential architectural design AI specialised in South Africa (Durban / KwaZulu-Natal).

When given a house brief, respond with these exact sections:

### DESIGN SUMMARY
Short professional overview.

### FLOOR PLAN DESCRIPTION
Organise by zones (Public, Private, Service, Garage). Include approximate room sizes in metres.

### KEY DESIGN FEATURES
Clear bullet points.

### PRELIMINARY MATERIAL SCHEDULE
Simple clean table.

### TECHNICAL NOTES
Mark as conceptual. Mention National Building Regulations and SANS. State that a registered professional must review.

### IMAGE PROMPTS
Create two high-quality prompts:

**2D Floor Plan Prompt:**
A detailed prompt for a clean, professional, labelled architectural floor plan (top-down, black lines on white, high contrast, clear room names, furniture outlines, scale).

**3D Exterior Prompt:**
A detailed prompt for a photorealistic modern architectural exterior render (materials, camera angle, lighting, style).

Make both prompts ready to copy-paste into an image generator.
"""

    response = client.chat.completions.create(
        model="grok-3",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": brief}
        ],
        temperature=0.35
    )
    return response.choices[0].message.content


def extract_prompts(full_text: str):
    prompt_2d = ""
    prompt_3d = ""

    if "**2D Floor Plan Prompt:**" in full_text:
        parts = full_text.split("**2D Floor Plan Prompt:**")
        if len(parts) > 1:
            after = parts[1]
            if "**3D Exterior Prompt:**" in after:
                prompt_2d = after.split("**3D Exterior Prompt:**")[0].strip()
                prompt_3d = after.split("**3D Exterior Prompt:**")[1].strip()
            else:
                prompt_2d = after.strip()

    if not prompt_2d:
        prompt_2d = (
            "Professional architectural floor plan, clean top-down 2D view, pure white background, "
            "sharp black lines, clearly labelled rooms with dimensions, modern single-storey house, "
            "open-plan kitchen dining lounge, master bedroom with en-suite, three bedrooms, double garage, "
            "high contrast, precise architectural drawing style, furniture outlines, north arrow, scale bar, "
            "professional CAD quality, high resolution"
        )
    if not prompt_3d:
        prompt_3d = (
            "Photorealistic architectural exterior render of a modern single-storey four-bedroom house "
            "with dramatic butterfly roof, clean white rendered walls, dark charcoal vertical cladding, "
            "warm timber accents, large glass sliding doors, double garage, concrete driveway, "
            "low native landscaping, three-quarter front view, soft natural daylight, ultra-realistic materials, "
            "professional architectural visualisation, sharp focus, high detail"
        )

    return prompt_2d, prompt_3d


def generate_image(prompt: str, api_key: str) -> Optional[bytes]:
    try:
        client = get_client(api_key)
        response = client.images.generate(
            model="grok-imagine-image-quality",
            prompt=prompt,
            n=1
        )
        image_url = response.data[0].url
        img_response = requests.get(image_url, timeout=90)
        if img_response.status_code == 200:
            return img_response.content
        return None
    except Exception as e:
        st.error(f"Image generation error: {str(e)}")
        return None


# ============================================
# 2. GENERATE CONCEPT + PROMPTS
# ============================================
st.markdown('<div class="section-title">2. Generate Architectural Concept</div>', unsafe_allow_html=True)

api_key = get_api_key()

if st.button("Generate Concept + Prompts", type="primary"):
    if not api_key:
        st.error("API key not found. Please add XAI_API_KEY in Streamlit Secrets.")
    elif not user_brief.strip():
        st.warning("Please enter a project brief first.")
    else:
        with st.spinner("Grok is creating the architectural concept and prompts..."):
            try:
                full_response = generate_concept_and_prompts(user_brief, api_key)
                prompt_2d, prompt_3d = extract_prompts(full_response)

                st.session_state.concept_text = full_response
                st.session_state.prompt_2d = prompt_2d
                st.session_state.prompt_3d = prompt_3d
            except Exception as e:
                st.error(f"Failed to generate concept: {e}")

if st.session_state.concept_text:
    st.success("Concept generated")
    st.caption(datetime.now().strftime("%d %B %Y • %H:%M"))
    st.markdown(st.session_state.concept_text)

    st.markdown("#### Ready-to-use Image Prompts")
    st.markdown("**2D Floor Plan Prompt**")
    st.markdown(f'<div class="prompt-box">{st.session_state.prompt_2d}</div>', unsafe_allow_html=True)

    st.markdown("**3D Exterior Prompt**")
    st.markdown(f'<div class="prompt-box">{st.session_state.prompt_3d}</div>', unsafe_allow_html=True)


# ============================================
# 3. GENERATE VISUALS
# ============================================
st.markdown('<div class="section-title">3. Generate Visuals</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("**2D Floor Plan**")
    if st.button("Generate 2D Floor Plan", use_container_width=True):
        if not api_key:
            st.error("API key missing.")
        elif not st.session_state.prompt_2d:
            st.warning("Generate the Concept first.")
        else:
            with st.spinner("Generating clean 2D floor plan..."):
                img_bytes = generate_image(st.session_state.prompt_2d, api_key)
            if img_bytes:
                st.image(img_bytes, use_container_width=True)
                st.download_button(
                    label="Download Floor Plan",
                    data=img_bytes,
                    file_name="mzipo_floorplan.png",
                    mime="image/png",
                    use_container_width=True
                )
            else:
                st.warning("Could not generate the floor plan.")

with col2:
    st.markdown("**3D Exterior Render**")
    if st.button("Generate 3D Exterior", use_container_width=True):
        if not api_key:
            st.error("API key missing.")
        elif not st.session_state.prompt_3d:
            st.warning("Generate the Concept first.")
        else:
            with st.spinner("Generating 3D exterior render..."):
                img_bytes = generate_image(st.session_state.prompt_3d, api_key)
            if img_bytes:
                st.image(img_bytes, use_container_width=True)
                st.download_button(
                    label="Download 3D Render",
                    data=img_bytes,
                    file_name="mzipo_3d_exterior.png",
                    mime="image/png",
                    use_container_width=True
                )
            else:
                st.warning("Could not generate the 3D render.")


# ============================================
# 4. PROMPT LAB
# ============================================
st.markdown('<div class="section-title">4. Prompt Lab</div>', unsafe_allow_html=True)
st.markdown("Test your own prompts or paste the ones generated above.")

lab_prompt = st.text_area(
    "Write or paste any image prompt here:",
    height=130,
    placeholder="Paste a 2D or 3D prompt here to test different styles..."
)

if st.button("Generate from Prompt Lab"):
    if not api_key:
        st.error("API key missing.")
    elif not lab_prompt.strip():
        st.warning("Please enter a prompt first.")
    else:
        with st.spinner("Generating image..."):
            test_img = generate_image(lab_prompt, api_key)
        if test_img:
            st.image(test_img, use_container_width=True)
            st.download_button(
                label="Download Test Image",
                data=test_img,
                file_name="mzipo_prompt_lab.png",
                mime="image/png"
            )
        else:
            st.warning("Image generation failed.")

st.markdown("<br>", unsafe_allow_html=True)
st.caption("Mzipo Architect Assistant  •  Version 6 (Deploy Ready)  •  Powered by Grok")
