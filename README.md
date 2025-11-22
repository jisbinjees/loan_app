# 🏦 Loan Eligibility Prototype

**LoanGuide** is a Streamlit-based app that helps users check loan eligibility, view required documents, and generate a downloadable lead summary — all without visiting a bank. It streamlines the loan process, making it faster and more convenient.

---

## **App Overview**

This app allows users to:

1. Select loan type (Personal, Home, Car, Education)
2. Choose their preferred bank
3. Enter salary details and existing EMIs
4. Check eligibility and view EMI breakdown for 5, 10, and 15-year tenures
5. Decide how to submit documents:
   - **Online (Assisted, Paid Service)**
   - **Visit Branch (Free)** → generates a downloadable lead summary

Additionally, the app provides a **sidebar checklist of required documents** based on loan type.

---

## **Why This App**

Visiting banks is time-consuming, and users often miss eligibility info or documents. LoanGuide reduces friction by:

- Showing required documents upfront  
- Calculating eligibility instantly  
- Allowing online document submission or downloadable lead summary  
- Providing EMI calculations for multiple tenures  

This makes the loan process faster, easier, and more transparent.

---

## **Features**

- Step-by-step loan eligibility check  
- EMI calculation for multiple tenures  
- Required document checklist based on loan type  
- Option to submit documents online (paid) or offline (downloadable lead summary)  
- Downloadable lead summary for bank submission  

---

## **User Journey / Core UX**

1. Select loan type and bank  
2. Enter income and existing EMIs → check eligibility  
3. View EMI examples for 5, 10, 15 years  
4. Choose submission method (Online or Branch)  
5. Download lead summary if visiting branch  

---

## **Monetisation / Retention**

- **Paid Service**: Assisted document submission online (1–2% fee)  
- **Free Service**: Downloadable verified lead summary  
- **Retention Features**: EMI reminders, saved leads, referral sharing  

---

## **Primary Metric**

**Share-to-Conversion Rate** — tracks how many shared lead summaries convert into new users or paid submissions.  

---

## **Getting Started**

### **Requirements**

- Python 3.8+  
- Streamlit  

Install dependencies:

```bash
pip install streamlit pandas numpy
