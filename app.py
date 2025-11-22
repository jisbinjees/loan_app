# app.py
import streamlit as st
import random
from datetime import datetime, timedelta

st.set_page_config(page_title="LoanGuide — Prototype + Brief", layout="wide")

# ---------- Basic styling / background ----------
st.markdown(
    """
    <style>
    body {
      background-color: #f5f7fb;
    }
    .block-container {
      padding: 1.2rem 1.5rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- Header ----------
st.title("🏦 LoanGuide — Loan Eligibility & Viral Growth Prototype")

# ---------- About Button / Prototype Brief ----------

with st.expander("✨ About — Prototype brief", expanded=False):
    st.markdown(
        """
**Problem framing:** People waste time visiting bank branches and often miss documents or eligibility info. LoanGuide brings eligibility checks, document lists, uploads, and lead/submission options to the user's phone — reducing friction and days of waiting.

**Product focus (prompt chosen): Viral Product Design** — this prototype demonstrates a referral/share loop: users generate downloadable lead summaries and referral links; sharing these drives new users. We intentionally prioritize a simple, demonstrable viral loop tied to a monetisation path.

**User journey & core UX (simplified):**
1. Choose loan type & bank  
2. Enter income and existing EMI → check eligibility  
3. See EMI examples for 5/10/15 years  
4. Choose submit method:
   - Upload (Assisted, paid)  
   - Visit branch (Free) → generates downloadable lead summary  
5. Share referral / invite friends → earn rewards

**Monetisation & retention:**
- Paid: 'Assisted upload & submission' (1% simulated fee) and 'Loan Concierge' premium (one-time fee)  
- Free: generate verified lead (banks pay commission)  
- Retention: EMI reminders, saved leads, periodic offers

**Primary metric to track (North Star):** Share-to-Conversion Rate — how many shared summaries convert into saved leads / paid submissions. This shows virality and monetisation together.
"""
    )

st.write("---")

# ---------- App state & analytics ----------
def mk_ref():
    return f"LG{random.randint(1000,9999)}"

if "analytics" not in st.session_state:
    st.session_state.analytics = {
        "visits": 1,
        "flows_started": 0,
        "elig_checks": 0,
        "service_selected": 0,
        "online_paid_submissions": 0,
        "manual_leads": 0,
        "leads_converted": 0,
        "referrals_sent": 0,
        "referrals_converted": 0,
        "premium_purchases": 0,
    }

if "leaderboard" not in st.session_state:
    st.session_state.leaderboard = {}

if "user_ref" not in st.session_state:
    st.session_state.user_ref = mk_ref()

if "saved_leads" not in st.session_state:
    st.session_state.saved_leads = []

if "eligible_amount" not in st.session_state:
    st.session_state.eligible_amount = None

# Count visit once per session
if "visit_counted" not in st.session_state:
    st.session_state.analytics["visits"] += 1
    st.session_state.visit_counted = True

# ---------- Mock data ----------
LOAN_DOCS = {
    "Personal Loan": ["Aadhaar", "PAN", "3 months salary slip", "6 months bank statement"],
    "Home Loan": ["Aadhaar", "PAN", "Property papers", "Latest salary slip", "6 months bank statement"],
    "Education Loan": ["Aadhaar", "PAN", "Admission letter", "Fee structure", "Guarantor docs"],
    "Business Loan": ["Aadhaar/PAN", "GST", "ITR (2 yrs)", "Business bank statement (6m)"],
}

BANKS = ["HDFC", "ICICI", "SBI", "Axis", "Kotak"]

# ---------- Layout (flow left, metrics right) ----------
left, right = st.columns([2, 1])

with left:
    st.header("Step 1 — Loan flow (try it)")

    # Loan type and docs preview (sidebar-like)
    loan_type = st.selectbox("Loan Type", ["-- pick --"] + list(LOAN_DOCS.keys()), key="loan_type_ui")
    if loan_type != "-- pick --" and not st.session_state.get("flow_started"):
        st.session_state.analytics["flows_started"] += 1
        st.session_state.flow_started = True

    # bank
    bank = st.selectbox("Preferred Bank", ["-- pick --"] + BANKS, key="bank_ui")

    # income & requested amount
    st.subheader("Income & loan request")
    monthly_income = st.number_input("Monthly Income (₹)", min_value=0, step=1000, key="salary_ui")
    requested_amount = st.number_input(
        "Requested Loan Amount (₹)", min_value=0, step=10000, key="requested_ui", value=100000
    )

    # existing loans
    existing_flag = st.radio("Do you have existing loan(s)?", ["No", "Yes"], key="existing_ui")
    existing_emi = 0
    if existing_flag == "Yes":
        existing_emi = st.number_input("Total monthly EMI (₹)", min_value=0, step=500, key="existing_emi_ui")

    st.write("---")

    # Eligibility
    st.subheader("Step 2 — Check eligibility")
    if st.button("Check Eligibility", key="elig_btn"):
        st.session_state.analytics["elig_checks"] += 1
        if monthly_income <= 0:
            st.error("Please enter monthly income to calculate eligibility.")
        else:
            # simple heuristic
            disposable = max(0, monthly_income - existing_emi)
            eligible = int(disposable * 12 * 2)  # demo multiplier
            st.session_state.eligible_amount = eligible
            st.success(f"Estimated eligible amount: ₹{eligible:,.0f}")

            # EMI examples (interest default 10%)
            st.subheader("EMI examples (10% p.a.)")
            def calc_emi(principal, years, annual_rate=10.0):
                n = years * 12
                r = annual_rate / 12 / 100
                if r == 0:
                    return principal / n
                emi = principal * r * (1 + r) ** n / ((1 + r) ** n - 1)
                return emi
            emi_cols = st.columns(3)
            for i, yrs in enumerate([5, 10, 15]):
                with emi_cols[i]:
                    emi_val = calc_emi(eligible, yrs)
                    st.metric(f"{yrs} yrs EMI", f"₹{emi_val:,.0f}")

    # show last eligible value (if exists)
    if st.session_state.eligible_amount:
        st.info(f"Last calculated eligible amount: ₹{st.session_state.eligible_amount:,.0f}")

    st.write("---")

    # Required docs preview
    st.subheader("Required documents")
    if loan_type == "-- pick --":
        st.info("Choose loan type to view typical required documents.")
    else:
        for d in LOAN_DOCS[loan_type]:
            st.write(f"- {d}")

    st.write("---")

    # Submission options
    st.subheader("Step 3 — Submission options (choose one)")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Upload documents online (Assisted, paid)", key="btn_assisted"):
            # must check eligibility first
            if not st.session_state.eligible_amount:
                st.error("Please run eligibility check before selecting assisted upload.")
            else:
                st.session_state.analytics["service_selected"] += 1
                st.session_state.analytics["online_paid_submissions"] += 1
                st.success("Assisted upload selected (simulated). Service fee 1% will apply on approval.")
                # file uploads
                st.write("Upload documents (salary slip, bank statement, ID).")
                f1 = st.file_uploader("Upload Salary Slip", key="upload_salary")
                f2 = st.file_uploader("Upload Bank Statement (6m)", key="upload_bank")
                f3 = st.file_uploader("Upload ID (Aadhaar/PAN)", key="upload_id")
                if f1 and f2 and f3:
                    if st.button("Simulate payment & submit", key="btn_sim_pay"):
                        st.success("Payment (simulated) confirmed and documents forwarded to partner bank.")
                        # create saved lead
                        lead = {
                            "id": f"LD{random.randint(10000,99999)}",
                            "loan_type": loan_type,
                            "bank": bank,
                            "eligible": st.session_state.eligible_amount,
                            "method": "assisted",
                            "time": datetime.utcnow().isoformat(),
                        }
                        st.session_state.saved_leads.append(lead)

    with col2:
        if st.button("I'll visit branch and submit (Generate lead)", key="btn_manual"):
            if not st.session_state.eligible_amount:
                st.error("Please run eligibility check first.")
            else:
                st.session_state.analytics["service_selected"] += 1
                st.session_state.analytics["manual_leads"] += 1
                lead = {
                    "id": f"LD{random.randint(10000,99999)}",
                    "loan_type": loan_type,
                    "bank": bank,
                    "eligible": st.session_state.eligible_amount,
                    "method": "manual",
                    "time": datetime.utcnow().isoformat(),
                }
                st.session_state.saved_leads.append(lead)
                st.success("Lead generated. Download your lead summary below.")
                # prepare summary
                summary = f"""LOAN LEAD SUMMARY
Lead ID: {lead['id']}
Loan Type: {lead['loan_type']}
Bank: {lead['bank']}
Eligible Amount: ₹{lead['eligible']:,.0f}
Monthly Income: ₹{monthly_income:,.0f}
Existing EMI: ₹{existing_emi:,.0f}

Required Documents:
{chr(10).join('- ' + d for d in LOAN_DOCS.get(loan_type, []))}

Generated by LoanGuide (ref: {st.session_state.user_ref})
"""
                st.download_button(
                    "📥 Download Lead Summary (TXT)",
                    data=summary,
                    file_name=f"lead_{lead['id']}.txt",
                    mime="text/plain",
                    key=f"dl_{lead['id']}",
                )

    st.write("---")

    # Monetisation CTA
    st.subheader("Premium: Loan Concierge (demo)")
    st.write("Priority verification and expedited submission to partner banks.")
    if st.button("Buy Loan Concierge — ₹199 (Simulate)", key="buy_premium"):
        st.session_state.analytics["premium_purchases"] += 1
        st.success("Premium purchased (simulation). You will be prioritized.")

    st.write("---")

    # Retention: EMI reminders
    st.subheader("Retention & Reuse")
    if st.checkbox("Enable EMI reminders (demo)", key="reminder_ui"):
        st.session_state.reminder_on = True
        next_emi = datetime.utcnow() + timedelta(days=30)
        st.info(f"EMI reminders enabled (demo). Next EMI: {next_emi.date()}")

    st.write("- Recommended products: Credit Card offers, Balance-transfer when eligible")

with right:
    st.header("Metrics & Viral Controls (Demo)")

    a = st.session_state.analytics
    st.metric("Visits", a["visits"])
    st.metric("Flows started", a["flows_started"])
    st.metric("Service selections", a["service_selected"])

    st.write("### Key metrics (demo)")
    flows = a["flows_started"] or 1
    ssr = a["service_selected"] / flows * 100
    total_leads = a["manual_leads"] + a["online_paid_submissions"]
    lead_conv = a["leads_converted"] / (total_leads or 1) * 100
    st.write(f"- **Service Selection Rate (SSR):** {ssr:.1f}%")
    st.write(f"- **Lead Conversion Rate (simulated):** {lead_conv:.1f}%")

    st.write("---")
    st.subheader("Viral loop — Share & Earn (demo)")
    st.write(f"Your referral code: **{st.session_state.user_ref}**")
    st.write("Share your code. When a referred user converts, you get rewards (demo).")

    if st.button("Simulate: I shared my code", key="sim_share"):
        st.session_state.analytics["referrals_sent"] += 1
        st.session_state.leaderboard.setdefault(st.session_state.user_ref, 0)
        st.session_state.leaderboard[st.session_state.user_ref] += 1
        st.success("Share simulated.")

    if st.button("Simulate: Friend converted using my code", key="sim_ref_conv"):
        st.session_state.analytics["referrals_converted"] += 1
        st.session_state.analytics["leads_converted"] += 1
        st.success("Referral conversion simulated. Reward granted (demo).")

    st.write("---")
    st.subheader("Leaderboard (Top Sharers)")
    lb = sorted(st.session_state.leaderboard.items(), key=lambda x: x[1], reverse=True)
    if lb:
        for i, (code, cnt) in enumerate(lb[:10], 1):
            st.write(f"{i}. {code} — {cnt} shares")
    else:
        st.write("No shares yet. Use 'Simulate: I shared my code'.")

    st.write("---")
    st.subheader("Saved Leads (recent)")
    if st.session_state.saved_leads:
        for lead in st.session_state.saved_leads[-10:]:
            st.write(f"- {lead['id']}: {lead['loan_type']} @ {lead['bank']} — ₹{lead['eligible']:,.0f} ({lead['method']})")
    else:
        st.write("No leads yet.")

    st.write("---")
#     st.subheader("Raw analytics")
#     st.code(a)

st.markdown("---")
st.caption("Prototype — Viral Product Design demo. Replace simulated actions with real backend, tracking, and payment integration for production.")
