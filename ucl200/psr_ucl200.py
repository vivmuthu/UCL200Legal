import json
import streamlit as st
from openai import OpenAI
from utils.theme_utils import *

# set_page_config must be the first Streamlit call, and only called once
st.set_page_config(page_title="PSR Generator", layout="wide")

load_theme(secondary="#155a8a",
    secondary_hover="#1F4264",
    secondary_active="#12324D"
    )

st.title("Sentencing Guidelines Teaching Tool")

# API key is read from Streamlit secrets (never hard-code it)
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

with st.form("psr_form"):
    st.subheader("Offence details")

    c1, c2 = st.columns(2)

    with c1:
        offence = st.selectbox(
            "Offence",
            ["Theft", "Burglary", "Robbery",  "Fraud", "Common Assault",
             "GBH", "Murder", "Harassment/stalking", "Possession with intent to supply", "Possession of an offensive weapon", "Other"]
        )

        plea = st.selectbox(
            "Plea", ["Guilty", "Convicted after trial", "Mixed"]
        )

        convictions = st.selectbox(
                    "Previous convictions",
                    ["None", "Non-violent", "Violent",
                     "Extensive", "Unknown"]
        )
        offence_facts = st.selectbox(
                    "Offence facts",
                    [
                        "Single incident, low value / minor harm",
                        "Single incident, significant harm or high value",
                        "Premeditated / planned offence",
                        "Opportunistic offence",
                        "Offence committed as part of a group",
                        "Offence committed while on bail",
                        "Weapon present but not used",
                        "Weapon used or threatened",
                        "Vulnerable victim targeted",
                        "Multiple victims",
                        "Offence committed in a domestic context",
                        "Commercial or organised element",
                        "Custom / other",
                    ]
                )

    with c2:

        mental_health = st.selectbox(
            "Mental health",
            ["None reported", "Schizophrenia", "Depression",
             "Bipolar disorder", "Other", "Unknown"]
        )
        housing = st.selectbox(
            "Accommodation",
            ["Stable", "Temporary", "Homeless", "Unknown"]
        )

        personal = st.selectbox(
            "Personal circumstances",
            [
                "No significant mitigation",
                "Genuine remorse expressed",
                "Sole or primary carer for dependants",
                "History of abuse or trauma relevant to offending",
                "Offending driven by addiction",
                "Offending driven by financial desperation",
                "Good employment history / in stable employment",
                "Strong community ties and character references",
                "Young adult (18–25), maturity considerations",
                "Serious physical ill-health",
                "Recent bereavement or personal crisis",
                "Custom / other",
            ]
        )

        risk = st.selectbox(
            "Risk assessment findings",
            [
                "No formal assessment available",
                "Low risk of reoffending (OASys / PSR)",
                "Medium risk of reoffending",
                "High risk of reoffending",
                "Low risk of serious harm to others",
                "Medium risk of serious harm to others",
                "High risk of serious harm to others (MAPPA referral likely)",
                "Risk linked specifically to substance misuse",
                "Risk linked to untreated mental health needs",
                "Protective factors identified (family, employment, engagement)",
                "Previously completed community order successfully",
                "Previously breached community order",
                "Custom / other",
            ]
        )

    submitted = st.form_submit_button(
        "Generate Sentencing Report", type="primary"
    )

if submitted:
    case = {
        "offence": offence,
        "plea": plea,
        "previous_convictions": convictions,
        "mental_health": mental_health,
        "accommodation": housing,
        "offence_facts": offence_facts,
        "personal_circumstances": personal,
        "risk_assessment": risk,
    }

    instructions = """
    You are a teaching tool to help students understand UK sentencing guidelines for England and Wales.

    Use the supplied case information only. Do not fabricate interviews, assessments, diagnoses,
    offending history, risk ratings or legal findings.

    Structure your output in exactly two sections:

    ## Sentencing Remarks
    Write the judge's sentencing remarks as they would be delivered in court — formal, direct,
    addressed to the defendant. State the sentence clearly upfront (e.g. custodial length,
    community order requirements, fine). Keep to 2–3 short paragraphs.

    ## Why This Sentence?
    Explain the reasoning in plain English for a student audience. Use bullet points. Cover:
    - The starting point from the Sentencing Council guidelines and why
    - Key aggravating factors that increased the sentence
    - Key mitigating factors that reduced it
    - How the plea was treated and what credit (if any) was applied
    - Any relevant risk or personal circumstances that shaped the disposal
    - The range of sentences available and why this one was chosen

    Write the remarks in a formal judicial style and the explanation in clear, simple language
    a law student would understand. Avoid jargon in the explanation section.
    Begin the entire response with: DRAFT — NOT FOR COURT USE WITHOUT PROFESSIONAL VERIFICATION
    """

    with st.spinner("Generating report..."):
        response = client.responses.create(
            model="gpt-4.1",
            instructions=instructions,
            input=json.dumps(case, indent=2)
        )

    st.session_state["report"] = response.output_text

if "report" in st.session_state:
    st.markdown(st.session_state["report"])
