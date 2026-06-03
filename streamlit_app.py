import streamlit as st

st.set_page_config(page_title="Onboarding Cost Request", page_icon="📥", layout="centered")

page_style = """
    <style>
        .stApp {
            background: linear-gradient(180deg, #f7fafc 0%, #edf2f7 100%);
            color: #0f172a;
        }
        .title {
            color: #0f172a;
        }
        .section-header {
            font-size: 1.4rem;
            color: #1d4ed8;
            margin-bottom: 0.3rem;
        }
        .stButton>button {
            background-color: #2563eb;
            color: white;
            border-radius: 0.75rem;
            padding: 0.75rem 1rem;
        }
        .stButton>button:hover {
            background-color: #1d4ed8;
            color: white;
        }
    </style>
"""

st.markdown(page_style, unsafe_allow_html=True)

if "step" not in st.session_state:
    st.session_state.step = 1
    st.session_state.business_name = ""
    st.session_state.request_type = "New source ingestion request"
    st.session_state.data_volume = 10.0
    st.session_state.frequency = "Daily"
    st.session_state.retention_months = 12
    st.session_state.ingestion_mode = "Incremental"
    st.session_state.load_type = "SQL"
    st.session_state.estimate = None

st.title("Onboarding Request Cost Estimator")
st.markdown(
    "Use this guided form to capture your onboarding request details and estimate the cost for data ingestion."
)

st.markdown("---")

if st.session_state.step == 1:
    st.markdown("## Step 1: Business request details")
    with st.form(key="business_form"):
        st.markdown("<div class='section-header'>Tell us about the request</div>", unsafe_allow_html=True)
        business_name = st.text_input("Business user / team name", st.session_state.business_name)
        request_type = st.radio(
            "Is this a new source ingestion request or new data to an existing source?",
            ["New source ingestion request", "New data to existing source"],
            index=0 if st.session_state.request_type == "New source ingestion request" else 1,
        )
        col1, col2 = st.columns([1, 1])
        with col1:
            back = st.form_submit_button("Reset")
        with col2:
            continue_button = st.form_submit_button("Continue")

        if back:
            st.session_state.business_name = ""
            st.session_state.request_type = "New source ingestion request"
        if continue_button:
            st.session_state.business_name = business_name.strip()
            st.session_state.request_type = request_type
            st.session_state.step = 2

    if st.session_state.business_name:
        st.info(f"Current request for: **{st.session_state.business_name}**")
        st.write(f"Request type: **{st.session_state.request_type}**")

elif st.session_state.step == 2:
    st.markdown("## Step 2: Ingestion details")
    with st.form(key="detail_form"):
        st.markdown("<div class='section-header'>Fill in the pipeline parameters</div>", unsafe_allow_html=True)
        data_volume = st.number_input(
            "Estimated data volume (GB)",
            min_value=0.0,
            value=st.session_state.data_volume,
            step=1.0,
            format="%.1f",
        )
        frequency = st.selectbox(
            "Pipeline frequency",
            ["Daily", "Weekly", "Monthly", "Ad-hoc"],
            index=["Daily", "Weekly", "Monthly", "Ad-hoc"].index(st.session_state.frequency),
        )
        retention_months = st.number_input(
            "Retention period (months)",
            min_value=1,
            value=st.session_state.retention_months,
            step=1,
        )
        ingestion_mode = st.radio(
            "Ingestion mode",
            ["Incremental", "Bulk", "CDC"],
            index=["Incremental", "Bulk", "CDC"].index(st.session_state.ingestion_mode),
        )

        load_type = None
        if st.session_state.request_type == "New source ingestion request":
            load_type = st.selectbox(
                "Type of data load",
                ["SQL", "SFTP", "S3", "API", "Kafka"],
                index=["SQL", "SFTP", "S3", "API", "Kafka"].index(st.session_state.load_type),
            )

        col1, col2 = st.columns([1, 1])
        with col1:
            back_button = st.form_submit_button("Back")
        with col2:
            estimate_button = st.form_submit_button("Estimate Cost")

        if back_button:
            st.session_state.step = 1
        if estimate_button:
            st.session_state.data_volume = data_volume
            st.session_state.frequency = frequency
            st.session_state.retention_months = retention_months
            st.session_state.ingestion_mode = ingestion_mode
            if load_type is not None:
                st.session_state.load_type = load_type

            # Simple cost estimation logic
            base = 1200
            volume_cost = st.session_state.data_volume * 6
            frequency_factor = {
                "Daily": 2.0,
                "Weekly": 1.5,
                "Monthly": 1.2,
                "Ad-hoc": 1.0,
            }[st.session_state.frequency]
            retention_factor = 1.0 + min(st.session_state.retention_months, 36) / 36 * 0.25
            ingestion_factor = {
                "Incremental": 1.0,
                "Bulk": 1.2,
                "CDC": 1.4,
            }[st.session_state.ingestion_mode]
            source_factor = 1.25 if st.session_state.request_type == "New source ingestion request" else 1.0
            load_type_factor = {
                "SQL": 1.0,
                "SFTP": 1.1,
                "S3": 1.05,
                "API": 1.2,
                "Kafka": 1.3,
            }.get(st.session_state.load_type, 1.0)

            estimate = (
                base * frequency_factor * retention_factor * ingestion_factor * source_factor * load_type_factor
                + volume_cost
            )
            monthly_estimate = estimate * 0.08
            st.session_state.estimate = {
                "total": round(estimate, 2),
                "monthly": round(monthly_estimate, 2),
                "volume_cost": round(volume_cost, 2),
                "frequency_factor": frequency_factor,
                "retention_factor": round(retention_factor, 3),
                "ingestion_factor": ingestion_factor,
                "source_factor": source_factor,
                "load_type": st.session_state.load_type,
            }
            st.session_state.step = 3

    st.markdown("---")
    st.info(f"Request type: **{st.session_state.request_type}**")
    if st.session_state.request_type == "New source ingestion request":
        st.write(f"Data load type: **{st.session_state.load_type}**")
    st.write(f"Business request by: **{st.session_state.business_name or 'Not provided'}**")

elif st.session_state.step == 3:
    st.markdown("## Step 3: Cost estimate")
    if st.session_state.estimate is None:
        st.error("No estimate available yet. Please complete the form first.")
    else:
        estimate = st.session_state.estimate
        st.success("Your onboarding cost estimate is ready!")
        st.metric("Estimated onboarding cost", f"${estimate['total']:,.2f}")
        st.metric("Recommended monthly reserve", f"${estimate['monthly']:,.2f}")

        st.markdown("### Estimate details")
        st.write(f"- Data volume: **{st.session_state.data_volume:,.1f} GB**")
        st.write(f"- Frequency: **{st.session_state.frequency}**")
        st.write(f"- Retention: **{st.session_state.retention_months} months**")
        st.write(f"- Ingestion mode: **{st.session_state.ingestion_mode}**")
        if st.session_state.request_type == "New source ingestion request":
            st.write(f"- Load type: **{st.session_state.load_type}**")
        st.write(f"- Volume cost portion: **${estimate['volume_cost']:,.2f}**")
        st.write(
            f"- Factor multipliers: frequency **x{estimate['frequency_factor']}**, retention **x{estimate['retention_factor']}**, ingestion **x{estimate['ingestion_factor']}**, source **x{estimate['source_factor']}**"
        )

        with st.expander("See full calculation details"):
            st.write(
                "Base estimate * frequency * retention * ingestion * source * load type + volume cost"
            )
            st.write(
                f"Base: $1200 * {estimate['frequency_factor']} * {estimate['retention_factor']} * {estimate['ingestion_factor']} * {estimate['source_factor']} * {load_type_factor if 'load_type' in estimate else 1.0}"
            )
            st.write(f"Volume cost: ${estimate['volume_cost']:,.2f}")

        if st.button("Start a new request"):
            st.session_state.step = 1
            st.session_state.estimate = None

