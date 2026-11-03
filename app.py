
import streamlit as st
import pandas as pd

from ai_engine import analyze_enquiry
from data_manager import (
    initialize_data,
    save_enquiry,
    get_all_enquiries
)

# Page configuration
st.set_page_config(
    page_title="AI Healthcare Reception Assistant",
    page_icon="🏥",
    layout="wide"
)

initialize_data()

# Header
st.title("🏥 AI Healthcare Reception Assistant")
st.caption(
    "AI-powered healthcare administrative enquiry management"
)

st.warning(
    "Educational prototype only. Not for diagnosis, treatment, "
    "medical advice, or actual appointment confirmation. "
    "Do not enter real patient information."
)

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Choose a section",
    ["Enquiry Assistant", "Dashboard", "About Project"]
)

# --------------------------------------------------
# Enquiry Assistant
# --------------------------------------------------
if page == "Enquiry Assistant":

    st.header("Patient Enquiry")

    enquiry = st.text_area(
        "Enter a sample administrative enquiry",
        placeholder=(
            "Example: I would like to book an appointment "
            "with a general physician next Monday."
        ),
        max_chars=2000,
        height=150
    )

    if st.button("Analyze Enquiry", type="primary"):

        if not enquiry.strip():
            st.error("Please enter an enquiry.")

        else:
            with st.spinner("Analyzing enquiry with Gemini AI..."):

                try:
                    result = analyze_enquiry(enquiry)

                    # Save only successful analysis results
                    save_enquiry(enquiry, result)

                    st.success("Enquiry analysis completed!")

                    st.subheader("AI Analysis")

                    st.write("**Category:**", result["category"])
                    st.write("**Intent:**", result["intent"])

                    st.subheader("Appointment Preferences")

                    details = result["patient_details"]

                    st.write(
                        "**Preferred Date:**",
                        details.get("preferred_date") or "Not provided"
                    )

                    st.write(
                        "**Preferred Time:**",
                        details.get("preferred_time") or "Not provided"
                    )

                    st.write(
                        "**Doctor Type:**",
                        details.get("doctor_type") or "Not provided"
                    )

                    st.write(
                        "**Missing Information:**",
                        details.get("missing_information", [])
                    )

                    st.subheader("Suggested Response")
                    st.info(result["response"])

                    if result["requires_human_review"]:
                        st.warning(
                            "Human review required: "
                            + str(result["reason"])
                        )
                    else:
                        st.success("No human review flag returned.")

                except Exception as error:
                    # Show friendly messages instead of raw API errors
                    error_message = str(error).upper()

                    if (
                        "503" in error_message
                        or "UNAVAILABLE" in error_message
                    ):
                        st.warning(
                            "Gemini AI is temporarily unavailable due to "
                            "high demand. Please try again in a few minutes."
                        )

                    elif (
                        "429" in error_message
                        or "RESOURCE_EXHAUSTED" in error_message
                        or "QUOTA" in error_message
                    ):
                        st.warning(
                            "The Gemini API request limit has been reached. "
                            "Please try again later or check your API quota."
                        )

                    elif (
                        "API_KEY_INVALID" in error_message
                        or "API KEY NOT VALID" in error_message
                        or "UNAUTHENTICATED" in error_message
                    ):
                        st.error(
                            "Gemini API authentication failed. "
                            "Please check the API key in the app configuration."
                        )

                    else:
                        st.error(
                            "The enquiry could not be analyzed. "
                            "Please try again later."
                        )


# --------------------------------------------------
# Dashboard
# --------------------------------------------------
elif page == "Dashboard":

    st.header("Enquiry Dashboard")

    df = get_all_enquiries()
    total = len(df)

    if total > 0:

        review_count = (
            df["requires_human_review"]
            .astype(str)
            .str.lower()
            .isin(["true", "1"])
            .sum()
        )

        col1, col2, col3 = st.columns(3)

        col1.metric("Total Enquiries", total)
        col2.metric("Human Review Required", int(review_count))
        col3.metric("Other Enquiries", total - int(review_count))

        st.subheader("Enquiry Category Distribution")

        category_counts = df["category"].value_counts()
        st.bar_chart(category_counts)

        st.subheader("Human Review Overview")

        review_percentage = (review_count / total) * 100

        st.progress(float(review_percentage / 100))

        st.caption(
            f"{review_percentage:.1f}% of enquiries require human review."
        )

        st.subheader("Recent Enquiry Records")
        st.dataframe(df, width="stretch")

        csv_data = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            "Download Enquiry Records",
            data=csv_data,
            file_name="enquiry_records.csv",
            mime="text/csv"
        )

    else:
        st.info("No enquiries have been recorded yet.")


# --------------------------------------------------
# About Project
# --------------------------------------------------
elif page == "About Project":

    st.header("About This Project")

    st.write("""
    This project demonstrates how Generative AI can support
    healthcare reception workflows.

    **Technologies used:**
    - Python
    - Streamlit
    - Google Gemini API
    - Pandas
    - CSV data storage

    **Main capabilities:**
    - Administrative enquiry classification
    - Appointment preference extraction
    - Suggested response generation
    - Human review flagging
    - Enquiry record management

    This application is an educational prototype and requires
    human verification before any real-world use.
    """)
