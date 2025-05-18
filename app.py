import streamlit as st
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import streamlit.components.v1 as components
import pandas as pd
import os

# Page setup
st.set_page_config(page_title="Youtube Co-Pilot", layout="wide")


# Styling
st.markdown("""
<style>
    html, body, .stApp {
        background-color: #0f111a !important;
        color: #e0e0e0 !important;
        font-family: 'Segoe UI', sans-serif;
        font-size: 18px !important;
    }

    .block-container {
        padding: 1rem 1.5rem;
    }

    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
        font-weight: 600 !important;
        line-height: 1.4;
    }

    p, li, span, div {
        color: #e0e0e0 !important;
        line-height: 1.6;
    }

    input, textarea {
        background-color: #1a1d2b !important;
        color: #e0e0e0 !important;
        border: 1px solid #333 !important;
        font-size: 16px !important;
        padding: 8px;
        border-radius: 6px;
    }

    .stButton > button {
        background-color: #8a2be2 !important;
        color: white !important;
        font-weight: bold;
        border-radius: 6px;
        padding: 0.6rem 1.2rem;
        transition: all 0.3s ease;
    }

    .stButton > button:hover {
        background-color: #00ffe7 !important;
        color: black !important;
    }

div[data-baseweb="select"] > div {
        background-color: #1c1f26 !important;
        color: #FAFAFA !important;
    }
    div[data-baseweb="select"] span {
        color: #FAFAFA !important;
    }
    div[data-baseweb="select"] div[role="option"] {
        color: #FAFAFA !important;
    }
</style>
""", unsafe_allow_html=True)

components.html(
    """
    <style>
        /* Overall body & app styling */
        html, body, .stApp {
            background-color: #0e1117 !important;
            color: #FAFAFA !important;
        }

        /* Streamlit widgets including dropdowns */
        .css-1cpxqw2, .stTextInput>div>div>input, .stTextArea>div>textarea {
            background-color: #1c1f26 !important;
            color: #FAFAFA !important;
        }

        /* Selectbox input text and placeholder */
        div[data-baseweb="select"] .css-1jqq78o-placeholder, 
        div[data-baseweb="select"] .css-qc6sy-singleValue,
        div[data-baseweb="select"] input {
            color: #FAFAFA !important;
        }

        /* Dropdown options */
        div[data-baseweb="select"] [role="option"] {
            background-color: #1c1f26 !important;
            color: #FAFAFA !important;
        }

        /* Highlight selected option */
        div[data-baseweb="select"] [aria-selected="true"] {
            background-color: #343846 !important;
            color: #FFFFFF !important;
        }

        /* Hover style on options */
        div[data-baseweb="select"] [role="option"]:hover {
            background-color: #44495a !important;
            color: #FAFAFA !important;
        }
    </style>
    """,
    height=0
)


# Load API Key
import streamlit as st
import os

api_key = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")

# LLaMA 3 via Groq API

def call_llama3(prompt):
    # st.write("🧠 LLaMA 3 Prompt Sent:")
    # st.code(prompt)

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    body = {
        "model": "llama3-70b-8192",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }
    try:
        response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=body)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        st.error(f"Groq API Error: {e}")
        return ""

# Extract website content

# Hero section
st.markdown("""
<h1 style='font-size: 1.75rem;'>🎯 Youtube Strategy Co-Pilot</h1>
<p>Hey, I'm <a href='https://www.linkedin.com/in/manmeetakali/' target='_blank'>Manmeet</a>. I built this because most brands get YouTube wrong. 📉</p>

<p>Brands usually go "me-me-me" & treat YT like an ad campaign. Big budgets. Zero Soul. The content ends up saying what <em>the brand</em> wants to say, not what <em>the user</em> actually cares about. That’s why it flops. ❌</p>

<p>The secret of this tool? We don’t start with product features. We start with real-life problems your user faces — and build content that solves, celebrates, or spotlights those problems. 💡 The result: content that feels useful, shareable, and human. ❤️</p>

<p>Let’s build your plan the same way. This works like magic, Aai Shapat! ✨👇</p>
""", unsafe_allow_html=True)


# Step 0: Optional Brand Name Input
st.markdown("<h3>We're going to ask you few basic Qs.</h3>", unsafe_allow_html=True)
brand_name = st.text_input("Enter your brand name (e.g., Swiggy, Mokobara, Swish).. I'm AI generating info for now, feel free to copy paste this in the Qs ahead")
if brand_name:
    with st.spinner("Researching your brand and crafting insights..."):
        prompt = f"""
You are a research assistant. Find the most relevant, public-facing information available about the brand '{brand_name}' by searching the internet.

Summarize the following in a clean, useful way:
1. What the brand does (2-3 lines)
2. What geography they are targeting?
3. What their brand personality is in 1 word (e.g., Hero, Everyman, Creator,Sage, Outlaw, Magician etc.)
4. Who their target persona(s) are (1-2 paragraphs)

Be objective and insightful — this is meant to inform marketing & content strategy.
"""
        ai_output = call_llama3(prompt)
        st.markdown("### ✨ AI Summary for Your Brand")
        st.write(ai_output)

# Step 1: Business input
st.markdown("<h3>Step 1: What does your business do?</h3>", unsafe_allow_html=True)
biz_desc = st.text_area("Business Summary", placeholder="We make stylish, durable travel gear for ambitious, on-the-move millennials who love exploring the world without compromising on aesthetics or quality.", height=100)

# Step 2: Geography & Brand Personality
st.markdown("<h3>Step 2: Where is your audience and what type of brand are you?</h3>", unsafe_allow_html=True)
geo = st.text_input("Step 3: Which geography or region are you targeting? (e.g., India, Tier 1 cities, Dubai, GenZ in Bangalore)")

st.markdown("""
Here are some common brand archetypes:
- **Hero**: Motivates through courage and achievement (e.g., Nike)
- **Everyman**: Relatable, down-to-earth, inclusive (e.g., IKEA)
- **Creator**: Inspires through imagination and self-expression (e.g., Adobe)
- **Sage**: Shares knowledge, clarity, and insights (e.g., Google)
- **Outlaw**: Breaks rules and rebels against the norm (e.g., Red Bull)
- **Magician**: Creates transformation and wonder (e.g., Disney)
- **Explorer**: Appeals to discovery and freedom (e.g., The North Face)
- **Caregiver**: Nurtures and supports others (e.g., Johnson & Johnson)
- **Jester**: Brings fun, humor, and joy (e.g., Zomato)
- **Lover**: Focuses on connection and indulgence (e.g., Chanel)
- **Ruler**: Shows control, authority, and status (e.g., Rolex)
- **Innocent**: Values purity, simplicity, optimism (e.g., Amul)
""", unsafe_allow_html=True)

archetype = st.selectbox(
    "Select the brand archetype that best fits your brand:",
    ["Hero", "Everyman", "Creator", "Sage", "Outlaw", "Magician", "Explorer", "Caregiver", "Jester", "Lover", "Ruler", "Innocent"]
)

# Step 3: Personas input
st.markdown("<h3>Step 4: Who are your ideal customer personas?</h3>", unsafe_allow_html=True)
personas = st.text_area("Describe your target personas (you can include multiple)", placeholder="Young professionals in metros who travel frequently (for work or leisure), care about aesthetics, hate chaotic packing, and prefer Instagrammable yet functional accessories. Also includes digital nomads, creators, and weekend travelers.", height=100)

if st.button("✅ Confirm & Continue") and biz_desc and personas:
    st.session_state["confirmed_personas"] = personas
    st.session_state["confirmed_biz"] = biz_desc
    st.rerun()

if "confirmed_personas" in st.session_state and "confirmed_biz" in st.session_state:
    personas = st.session_state["confirmed_personas"]
    biz_desc = st.session_state["confirmed_biz"]

    if st.button("🔍 Generate Problems + YouTube Plan"):
        with st.spinner("Generating problem list and YouTube plan..."):
            problem_prompt = f"""
You are a consumer insights strategist. Your job is to uncover deep, real-life problems faced by the target personas in their everyday lives, *not* just in relation to the brand. 

List 50 unique, emotionally resonant, problem-sparking pain points that these personas face — across lifestyle, aspiration, productivity, social behavior, health, ambition, convenience, etc.

These should be independent of the brand or product — and instead act as content insight triggers that the brand (described below) can build videos around using the IUCTC framework.

Personas:
{personas}

Business:
{biz_desc}

Give them in simple language, as a list, each on a new line."""
            problems = call_llama3(problem_prompt)
            st.markdown("### 😟 Top 50 Problems Faced by Your Personas")
            st.write(problems)

            plan_prompt = f"""
You are an idea strategist and creative storyteller. Your task is to deeply analyze the 50 consumer problems listed below and come up with 12 highly relatable and powerful YouTube video content ideas that either:
- solve these problems in a useful or inspirational way
- celebrate or poke fun at them if they can't be solved

Make sure the brand's role is subtle — woven into the content like a friend offering help, not like a sales pitch. Prioritize making the viewer feel understood and seen.

Use the IUCTC lens (Inspirational, Useful, Celebratory, Topical, Change-the-world) to diversify the content tone. Limit to just the 12 strongest ideas. Each should be:

1. Deeply rooted in a real consumer insight
2. Emotionally engaging, surprising, or witty
3. Featuring the brand as an enabler, not the hero

Structure the output as a table with the following columns:
- Suggested Week (1 to 12) Arrange the ideas in ascending order of the week number
- Category (Inspirational, Useful, Celebratory, Topical, Change-the-world)
- Video Title (use best practices — curiosity-piquing)
- Concept Summary (explain why this video solves a real problem and how the brand fits in & what's the hook) 
- Suggested Format (e.g., Vlog, Voxpop, podcast, Animation, etc.)

Business Summary: {biz_desc}
Personas: {personas}
Geography: {geo}
Brand Archetype: {archetype}
Problems:
{problems}

Output the table above. Then suggest:
1. 5 bonus content ideas (short bullets, fun, high-virality potential)
2. A content repurposing plan for each video, especially recommending how to extract short-form clips (e.g., Reels, Shorts) from the main content — especially for podcasts or interviews. Highlight how the brand can drive visibility through these clips.

Avoid repetition. Let the brand feel like a helpful enabler woven into the narrative, not the main character.. Make them fun, surprising, and high-virality potential. Avoid repetition.
"""
            plan = call_llama3(plan_prompt)
            st.markdown("### 🔥🔥 90-Day YouTube Content Plan")
            st.markdown(plan)

            st.markdown("""
---
### 
Let me know your feedback on this tool! I’m always looking to improve it. I'm on manmeet.akali@gmail.com'
This tool is based on a storytelling framework (inspired by the book Fast, Cheap & Viral) that helped Scaler School of Technology go from 0 to 50,000 subscribers — without an agency or crazy spends. We’ve since shared it with other startups and seen it work again and again. 

Don’t keep the good stuff to yourself — your team deserves to see this 🔥👇
                    
- [💬 WhatsApp](https://api.whatsapp.com/send?text=Yo%2C%20just%20used%20this%20killer%20AI%20tool%20to%20build%20a%2090-day%20YouTube%20plan%20that%20actually%20makes%20sense.%20Try%20it%20👉%20https%3A%2F%2Fyourdomain.com)
- [🐦 Twitter](https://twitter.com/intent/tweet?text=Just%20used%20an%20AI%20tool%20to%20generate%20a%2090-day%20YouTube%20plan%20that%20makes%20you%20look%20like%20a%20genius.%20Try%20it%20👉%20https%3A%2F%2Fyourdomain.com)
- [🔗 LinkedIn](https://www.linkedin.com/sharing/share-offsite/?url=https://yourdomain.com)
""")
            st.image(
    "https://indianmemetemplates.com/wp-content/uploads/2019/01/jor-jor-se-bolke-sabko-scheme-bata-de.jpg",
    caption="Jor Jor Se Bolke Sabko Scheme Bata De",
    use_container_width=True
)

st.markdown("---")
st.info("💡 Pro tip: Don’t stress over camera gear or lighting. A well-shot iPhone video with tight storytelling will beat a 5-cam rig with no soul. Invest in scripts, editing, and empathy. That’s what makes people stop scrolling.")
