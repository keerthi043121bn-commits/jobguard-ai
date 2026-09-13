import streamlit as st
import re

st.set_page_config(
    page_title="JobGuard AI",
    page_icon="🛡️",
    layout="wide"
)


# =====================================================
# FAKE JOB ANALYSIS ENGINE
# =====================================================

def analyze_job(job_text):

    text = job_text.lower()

    red_flags = []
    green_flags = []
    suspicious_words = []

    # Payment related red flags
    payment_words = [
        "registration fee",
        "processing fee",
        "security deposit",
        "joining fee",
        "training fee",
        "pay money",
        "payment required",
        "pay ₹",
        "pay rs"
    ]

    # Unrealistic salary claims
    salary_words = [
        "earn money easily",
        "guaranteed income",
        "earn ₹",
        "earn rs",
        "high salary no experience",
        "50,000 per week",
        "1 lakh per month"
    ]

    # Urgency / pressure words
    urgency_words = [
        "urgent",
        "limited vacancies",
        "apply immediately",
        "today only",
        "act now"
    ]

    # Sensitive information requests
    personal_words = [
        "bank details",
        "bank account",
        "otp",
        "atm pin",
        "password",
        "aadhaar",
        "pan card"
    ]

    # Check payment red flags
    for word in payment_words:
        if word in text:
            red_flags.append(
                "Payment request detected: " + word
            )
            suspicious_words.append(word)

    # Check salary red flags
    for word in salary_words:
        if word in text:
            red_flags.append(
                "Unrealistic salary/earning claim: " + word
            )
            suspicious_words.append(word)

    # Check urgency red flags
    for word in urgency_words:
        if word in text:
            red_flags.append(
                "Urgency or pressure language: " + word
            )
            suspicious_words.append(word)

    # Check sensitive information
    for word in personal_words:
        if word in text:
            red_flags.append(
                "Sensitive information request: " + word
            )
            suspicious_words.append(word)

    # Green flags
    green_checks = [
        ("job title", "Clear job title"),
        ("responsibilities", "Clear job responsibilities"),
        ("qualification", "Qualification requirements mentioned"),
        ("experience", "Experience requirement mentioned"),
        ("location", "Job location mentioned"),
        ("company", "Company information mentioned"),
        ("skills", "Required skills mentioned"),
        ("salary", "Salary information mentioned")
    ]

    for keyword, message in green_checks:
        if keyword in text:
            green_flags.append(message)

    # Excessive exclamation marks
    exclamation_count = text.count("!")

    if exclamation_count >= 4:
        red_flags.append(
            "Excessive use of exclamation marks"
        )
        suspicious_words.append("!!!")

    # Risk score
    risk_score = min(
        100,
        len(red_flags) * 15
    )

    # Green flags slightly reduce the risk
    risk_score = max(
        0,
        risk_score - min(len(green_flags) * 3, 15)
    )

    # Risk level
    if risk_score >= 60:
        risk_level = "🔴 HIGH RISK"
    elif risk_score >= 30:
        risk_level = "🟡 MEDIUM RISK"
    else:
        risk_level = "🟢 LOW RISK"

    # Word count
    total_words = len(
        re.findall(r"\b\w+\b", job_text)
    )

    # Suspicious word ratio
    suspicious_ratio = 0

    if total_words > 0:
        suspicious_ratio = round(
            (len(set(suspicious_words)) / total_words) * 100,
            1
        )

    return (
        risk_score,
        risk_level,
        red_flags,
        green_flags,
        suspicious_words,
        total_words,
        suspicious_ratio
    )


# =====================================================
# LOGIN
# =====================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


if not st.session_state.logged_in:

    st.title("🛡️ JobGuard AI")

    st.subheader(
        "Fake Job Detection & Skill-Based Job Finder"
    )

    st.write(
        "Protect your career before you apply."
    )

    st.divider()

    st.header("🔐 Login / Create Account")

    email = st.text_input("Email ID")

    username = st.text_input("Username")

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button(
        "Login",
        use_container_width=True
    ):

        if email and username and password:

            st.session_state.logged_in = True
            st.session_state.username = username

            st.rerun()

        else:

            st.warning(
                "Please enter Email ID, Username and Password."
            )


# =====================================================
# DASHBOARD
# =====================================================

else:

    st.title("🛡️ JobGuard AI")

    st.success(
        f"Welcome, {st.session_state.username}! "
        "Your career safety dashboard is ready."
    )

    st.divider()

    st.header("🚀 Choose a Feature")

    col1, col2 = st.columns(2)


    # JOB CHECKER
    with col1:

        st.subheader("🔍 Check a Job")

        st.write(
            "Analyze a job description for "
            "red flags, green flags and risk level."
        )

        if st.button(
            "Check Job Description",
            use_container_width=True
        ):

            st.session_state.page = "checker"


    # SKILL FINDER
    with col2:

        st.subheader("💼 Find Jobs")

        st.write(
            "Enter your skills and discover "
            "suitable job roles."
        )

        if st.button(
            "Find Jobs by Skills",
            use_container_width=True
        ):

            st.session_state.page = "skills"


    st.divider()

    st.info(
        "JobGuard AI combines explainable "
        "rule-based analysis with skill matching."
    )


    # =================================================
    # JOB CHECKER PAGE
    # =================================================

    if st.session_state.get("page") == "checker":

        st.divider()

        st.header("🔍 Job Description Checker")

        job_text = st.text_area(
            "Paste the Job Description here",
            height=250,
            placeholder="Paste the complete job description..."
        )

        if st.button(
            "🔎 Analyze Job",
            use_container_width=True
        ):

            if job_text.strip():

                (
                    risk_score,
                    risk_level,
                    red_flags,
                    green_flags,
                    suspicious_words,
                    total_words,
                    suspicious_ratio
                ) = analyze_job(job_text)


                st.divider()

                st.header(
                    "📊 JobGuard Analysis Result"
                )


                col1, col2, col3 = st.columns(3)


                with col1:

                    st.metric(
                        "Risk Score",
                        f"{risk_score}/100"
                    )


                with col2:

                    st.metric(
                        "Total Words",
                        total_words
                    )


                with col3:

                    st.metric(
                        "Suspicious Ratio",
                        f"{suspicious_ratio}%"
                    )


                st.subheader(risk_level)


                # RED FLAGS
                st.subheader("🔴 Red Flags")

                if red_flags:

                    for flag in red_flags:

                        st.error(
                            "⚠️ " + flag
                        )

                else:

                    st.success(
                        "No major red flags detected."
                    )


                # GREEN FLAGS
                st.subheader("🟢 Green Flags")

                if green_flags:

                    for flag in green_flags:

                        st.success(
                            "✓ " + flag
                        )

                else:

                    st.warning(
                        "No strong trust indicators detected."
                    )


                # SUSPICIOUS TERMS
                st.subheader(
                    "🔎 Suspicious Terms"
                )

                if suspicious_words:

                    st.write(
                        ", ".join(
                            sorted(
                                set(suspicious_words)
                            )
                        )
                    )

                else:

                    st.write(
                        "No suspicious terms detected."
                    )


                # RECOMMENDATION
                st.subheader(
                    "💡 JobGuard Recommendation"
                )

                if risk_score >= 60:

                    st.warning(
                        "⚠️ Strong warning signs detected. "
                        "Verify the employer independently "
                        "before applying."
                    )

                elif risk_score >= 30:

                    st.info(
                        "⚠️ Some warning signs were detected. "
                        "Verify the company and job details carefully."
                    )

                else:

                    st.success(
                        "✅ No major warning signs detected. "
                        "Still verify the employer before "
                        "sharing personal information."
                    )

            else:

                st.warning(
                    "Please paste a job description first."
                )


    # =================================================
    # SKILL MATCHER PAGE
    # =================================================

    if st.session_state.get("page") == "skills":

        st.divider()

        st.header(
            "💼 Skill-Based Job Finder"
        )

        skills = st.text_input(
            "Enter your skills",
            placeholder="Example: Python, Excel, Power BI, Figma"
        )

        if st.button(
            "🚀 Find Matching Jobs",
            use_container_width=True
        ):

            if skills.strip():

                skill_text = skills.lower()

                st.success(
                    "Skills received successfully!"
                )

                st.subheader(
                    "🎯 Suggested Job Roles"
                )

                found_roles = []

                if "python" in skill_text:

                    found_roles.extend([
                        "Python Developer",
                        "Data Analyst",
                        "Junior Python Developer"
                    ])

                if "power bi" in skill_text:

                    found_roles.extend([
                        "Power BI Analyst",
                        "BI Analyst",
                        "Data Analyst"
                    ])

                if "excel" in skill_text:

                    found_roles.extend([
                        "Excel Analyst",
                        "Data Analyst",
                        "Business Analyst"
                    ])

                if "figma" in skill_text:

                    found_roles.extend([
                        "UI/UX Designer",
                        "UI Designer",
                        "Product Design Intern"
                    ])

                if "ui" in skill_text:

                    found_roles.extend([
                        "UI/UX Designer",
                        "UI Designer"
                    ])

                if "sql" in skill_text:

                    found_roles.extend([
                        "SQL Analyst",
                        "Data Analyst"
                    ])


                if found_roles:

                    for role in sorted(
                        set(found_roles)
                    ):

                        st.write(
                            "✅ " + role
                        )

                else:

                    st.info(
                        "No predefined role found. "
                        "Try skills such as Python, Excel, "
                        "Power BI, Figma or SQL."
                    )


                st.subheader(
                    "🌐 Professional Job Search"
                )

                st.write(
                    "Use these platforms to view current job listings:"
                )

                search_skill = skills.replace(
                    " ",
                    "+"
                )

                st.link_button(
                    "🔵 Search on LinkedIn",
                    "https://www.linkedin.com/jobs/search/?keywords="
                    + search_skill
                )

                st.link_button(
                    "🟢 Search on Indeed",
                    "https://in.indeed.com/jobs?q="
                    + search_skill
                )

                st.link_button(
                    "🟠 Search on Naukri",
                    "https://www.naukri.com/"
                )

            else:

                st.warning(
                    "Please enter at least one skill."
                )


    # LOGOUT

    st.divider()

    if st.button("Logout"):

        st.session_state.logged_in = False

        st.rerun()