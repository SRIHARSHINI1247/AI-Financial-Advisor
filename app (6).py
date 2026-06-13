import streamlit as st
import pandas as pd
import numpy as np
import pytesseract
from PIL import Image
import matplotlib.pyplot as plt
import re
import io
from datetime import datetime

from sklearn.linear_model import LinearRegression
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)
from reportlab.lib.styles import getSampleStyleSheet



# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(
    page_title="AI Financial Advisor",
    page_icon="💰",
    layout="wide"
)



# =====================================
# SESSION STORAGE
# =====================================

def init_session():

    if "transactions" not in st.session_state:
        st.session_state.transactions = []



# =====================================
# CATEGORY DETECTION
# =====================================

def detect_category(merchant):

    merchant = str(merchant).lower()


    if any(x in merchant for x in [
        "swiggy",
        "zomato",
        "food",
        "restaurant"
    ]):
        return "Food"


    elif any(x in merchant for x in [
        "uber",
        "ola",
        "metro",
        "bus"
    ]):
        return "Transport"


    elif any(x in merchant for x in [
        "netflix",
        "prime",
        "movie"
    ]):
        return "Entertainment"


    elif any(x in merchant for x in [
        "amazon",
        "flipkart",
        "shopping"
    ]):
        return "Shopping"


    else:
        return "Other"




# =====================================
# CREATE TRANSACTION
# =====================================

def create_transaction(
        merchant,
        amount,
        date=None
):

    if date is None:
        date = datetime.now().strftime(
            "%Y-%m-%d"
        )


    return {

        "Date": date,

        "Merchant": merchant,

        "Amount": float(amount),

        "Category": detect_category(
            merchant
        )
    }




# =====================================
# OCR FUNCTIONS
# =====================================

def extract_text(image):

    return pytesseract.image_to_string(
        image
    )




def extract_amount(text):

    numbers = re.findall(
        r'\d+',
        text
    )


    values = []


    for n in numbers:

        value = int(n)

        if 10 <= value <= 50000:

            values.append(
                value
            )


    if values:

        return min(values)


    return 0




def detect_merchant(text):

    text = text.lower()


    merchants = {

        "swiggy":"Swiggy",

        "zomato":"Zomato",

        "uber":"Uber",

        "ola":"Ola",

        "netflix":"Netflix",

        "amazon":"Amazon",

        "flipkart":"Flipkart"

    }


    for key,value in merchants.items():

        if key in text:

            return value


    return "Unknown"




def extract_date(text):

    match = re.search(
        r'\d{2}[-/]\d{2}[-/]\d{4}',
        text
    )


    if match:

        return match.group()


    return datetime.now().strftime(
        "%Y-%m-%d"
    )





# =====================================
# CSV PROCESSING
# =====================================

def process_csv(file):

    df = pd.read_csv(
        file
    )


    if "Category" not in df.columns:

        df["Category"] = df[
            "Merchant"
        ].apply(
            detect_category
        )


    return df





# =====================================
# ADD TRANSACTIONS
# =====================================

def add_transactions(df):

    st.session_state.transactions = (
        df.to_dict(
            "records"
        )
    )
    # =====================================
# DASHBOARD ANALYSIS
# =====================================

def spending_summary(df):

    total = df["Amount"].sum()

    count = len(df)

    average = total / count if count > 0 else 0


    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
            "💰 Total Spending",
            f"₹{total:.0f}"
        )


    with col2:

        st.metric(
            "🧾 Transactions",
            count
        )


    with col3:

        st.metric(
            "📊 Average Expense",
            f"₹{average:.0f}"
        )


    return total




# =====================================
# CATEGORY ANALYSIS
# =====================================

def category_analysis(df):

    st.subheader(
        "📌 Category Spending"
    )


    category = (
        df.groupby("Category")
        ["Amount"]
        .sum()
    )


    st.dataframe(
        category
    )


    fig,ax = plt.subplots()


    category.plot(
        kind="pie",
        autopct="%1.1f%%",
        ax=ax
    )


    ax.set_ylabel("")


    st.pyplot(fig)



    fig2,ax2 = plt.subplots()


    category.plot(
        kind="bar",
        ax=ax2
    )


    ax2.set_ylabel(
        "Amount"
    )


    st.pyplot(fig2)


    return category





# =====================================
# SPENDING TREND ANALYSIS
# =====================================

def spending_trends(df):

    st.subheader(
        "📈 Spending Trends"
    )


    if "Date" in df.columns:


        df["Date"] = pd.to_datetime(
            df["Date"]
        )


        daily = (
            df.groupby("Date")
            ["Amount"]
            .sum()
        )


        fig,ax = plt.subplots()


        daily.plot(
            marker="o",
            ax=ax
        )


        ax.set_ylabel(
            "Amount"
        )


        st.pyplot(fig)


    else:

        st.info(
            "Date data not available"
        )





# =====================================
# ANOMALY DETECTION
# =====================================

def anomaly_detection(df):

    st.subheader(
        "🚨 Unusual Expense Detection"
    )


    mean = df["Amount"].mean()


    limit = mean * 2


    unusual = df[
        df["Amount"] > limit
    ]


    if len(unusual)>0:


        st.warning(
            "High value transactions detected"
        )


        st.dataframe(
            unusual
        )


    else:


        st.success(
            "No unusual spending detected"
        )





# =====================================
# MACHINE LEARNING PREDICTION
# =====================================

def spending_prediction(df):

    st.subheader(
        "🤖 Future Spending Prediction"
    )


    if len(df) < 3:

        st.info(
            "Add more transactions for prediction"
        )

        return



    temp = df.copy()


    temp["Day"] = np.arange(
        len(temp)
    )


    X = temp[
        ["Day"]
    ]

    y = temp[
        "Amount"
    ]



    model = LinearRegression()


    model.fit(
        X,
        y
    )


    future_day = np.array(
        [[len(temp)+1]]
    )


    prediction = model.predict(
        future_day
    )[0]


    st.success(
        f"Predicted next expense: ₹{prediction:.2f}"
    )





# =====================================
# FINANCIAL HEALTH SCORE
# =====================================

def financial_health(total):

    st.subheader(
        "❤️ Financial Health Score"
    )


    if total < 3000:

        score = 90


    elif total < 7000:

        score = 70


    else:

        score = 50



    st.progress(
        score/100
    )


    st.write(
        f"Health Score: {score}/100"
    )





# =====================================
# COMPLETE DASHBOARD
# =====================================

def dashboard(df):

    st.header(
        "📊 Financial Dashboard"
    )


    total = spending_summary(
        df
    )


    category_analysis(
        df
    )


    spending_trends(
        df
    )


    anomaly_detection(
        df
    )


    spending_prediction(
        df
    )


    financial_health(
        total
    )


    return total
    # =====================================
# AI FINANCIAL ASSISTANT
# =====================================

def financial_chatbot(df):

    st.subheader(
        "🤖 AI Financial Assistant"
    )


    total = df["Amount"].sum()


    category = (
        df.groupby("Category")
        ["Amount"]
        .sum()
    )


    highest = category.idxmax()



    st.info(
        f"""
        Your total spending is ₹{total:.0f}.

        Highest spending category:
        {highest}

        Try monitoring this category
        to improve savings.
        """
    )



    question = st.text_input(
        "Ask financial question",
        key="finance_question"
    )


    if question:


        q = question.lower()


        if "save" in q:

            st.success(
                "Try following the 50-30-20 rule: "
                "50% needs, 30% wants, 20% savings."
            )


        elif "budget" in q:

            st.info(
                "Create a monthly budget limit "
                "and review expenses weekly."
            )


        elif "invest" in q:

            st.success(
                "Consider diversified investments "
                "based on your risk level."
            )


        else:

            st.write(
                "Track expenses regularly and avoid unnecessary spending."
            )





# =====================================
# SMART FINANCIAL ADVICE
# =====================================

def financial_advice(df):

    st.subheader(
        "💡 Smart Financial Advice"
    )


    category = (
        df.groupby("Category")
        ["Amount"]
        .sum()
    )


    highest = category.idxmax()


    if highest == "Food":

        st.warning(
            "Food expenses are high. "
            "Reduce frequent online orders."
        )


    elif highest == "Shopping":

        st.warning(
            "Shopping expenses are high. "
            "Avoid unnecessary purchases."
        )


    elif highest == "Entertainment":

        st.warning(
            "Review your subscriptions."
        )


    else:

        st.success(
            "Your spending pattern looks balanced."
        )





# =====================================
# INVESTMENT ADVISOR
# =====================================

def investment_advisor():

    st.subheader(
        "📈 Investment Suggestions"
    )


    st.write(
        """
        Based on general financial principles:

        • Emergency fund: Save 3-6 months expenses

        • Low risk:
          Fixed deposits, bonds

        • Medium risk:
          Mutual funds

        • Long term:
          Index funds and diversified investments
        """
    )





# =====================================
# TAX SAVING ADVISOR
# =====================================

def tax_saving_advisor():

    st.subheader(
        "📑 Tax Saving Suggestions"
    )


    income = st.number_input(
        "Annual Income",
        min_value=0,
        value=600000,
        key="annual_income_input"
    )


    if income > 0:


        st.write(
            "Possible tax saving options:"
        )


        st.info(
            """
            • ELSS Mutual Funds

            • Public Provident Fund (PPF)

            • National Pension System (NPS)

            • Insurance deductions
            """
        )





# =====================================
# PDF REPORT GENERATOR
# =====================================

def create_pdf(df):

    buffer = io.BytesIO()


    pdf = SimpleDocTemplate(
        buffer
    )


    styles = getSampleStyleSheet()


    content = []


    total = df["Amount"].sum()


    content.append(
        Paragraph(
            "AI Financial Advisor Report",
            styles["Heading1"]
        )
    )


    content.append(
        Spacer(1,20)
    )


    content.append(
        Paragraph(
            f"Total Spending: Rs {total}",
            styles["Normal"]
        )
    )


    content.append(
        Spacer(1,10)
    )


    category = (
        df.groupby("Category")
        ["Amount"]
        .sum()
    )


    for name,value in category.items():

        content.append(
            Paragraph(
                f"{name}: Rs {value}",
                styles["Normal"]
            )
        )


    pdf.build(
        content
    )


    buffer.seek(0)


    return buffer





# =====================================
# REPORT SECTION
# =====================================

def report_section(df):

    st.subheader(
        "📄 Download Report"
    )


    pdf = create_pdf(
        df
    )


    st.download_button(
        label="⬇ Download Financial Report",
        data=pdf,
        file_name="financial_report.pdf",
        mime="application/pdf",
        key="financial_report_download"
    )
    # =====================================
# MAIN APPLICATION
# =====================================

def main():


    init_session()



    # ===============================
    # SIDEBAR
    # ===============================

    st.sidebar.title(
        "💰 AI Financial Advisor"
    )


    st.sidebar.write(
        """
        Week 7-8 Features

        ✅ OCR Receipt Scanner

        ✅ ML Prediction

        ✅ Spending Trends

        ✅ Anomaly Detection

        ✅ AI Assistant

        ✅ PDF Reports
        """
    )



    page = st.sidebar.radio(

        "Navigation",

        [
            "📂 Upload CSV",
            "📷 Upload Receipt",
            "🏠 Dashboard",
            "🤖 AI Assistant",
            "📄 Reports"
        ],

        index=0

    )



    # ===============================
    # CSV UPLOAD
    # ===============================

    if page == "📂 Upload CSV":


        st.header(
            "📂 Upload Expense CSV"
        )


        csv_file = st.file_uploader(

            "Upload CSV File",

            type=["csv"],

            key="main_csv_upload"

        )



        if csv_file:


            df = process_csv(
                csv_file
            )


            add_transactions(
                df
            )


            st.success(
                "CSV uploaded successfully!"
            )


            st.subheader(
                "Transaction Preview"
            )


            st.dataframe(

                df,

                use_container_width=True

            )



            st.info(
                "Go to Dashboard from sidebar to view analysis."
            )





    # ===============================
    # OCR RECEIPT
    # ===============================

    elif page == "📷 Upload Receipt":


        st.header(
            "📷 OCR Receipt Scanner"
        )


        images = st.file_uploader(

            "Upload Payment Screenshot",

            type=[
                "png",
                "jpg",
                "jpeg"
            ],

            accept_multiple_files=True,

            key="main_receipt_upload"

        )



        if images:


            for img in images:


                image = Image.open(
                    img
                )


                st.image(
                    image,
                    caption=img.name
                )



                text = extract_text(
                    image
                )


                st.subheader(
                    "Extracted Text"
                )


                st.write(
                    text
                )



                amount = extract_amount(
                    text
                )


                merchant = detect_merchant(
                    text
                )


                date = extract_date(
                    text
                )



                transaction = create_transaction(

                    merchant,

                    amount,

                    date

                )



                st.session_state.transactions.append(

                    transaction

                )



                st.success(

                    f"Added {merchant} ₹{amount}"

                )






    # ===============================
    # DASHBOARD
    # ===============================

    elif page == "🏠 Dashboard":


        st.header(
            "📊 Financial Dashboard"
        )


        if len(
            st.session_state.transactions
        ) > 0:



            df = pd.DataFrame(

                st.session_state.transactions

            )


            total = dashboard(
                df
            )


            financial_advice(
                df
            )


        else:


            st.warning(
                "Upload CSV or receipt first."
            )






    # ===============================
    # AI ASSISTANT
    # ===============================

    elif page == "🤖 AI Assistant":


        st.header(
            "🤖 AI Money Assistant"
        )



        if len(
            st.session_state.transactions
        ) > 0:



            df = pd.DataFrame(

                st.session_state.transactions

            )


            financial_chatbot(
                df
            )


        else:


            st.warning(
                "No expenses available."
            )







    # ===============================
    # REPORTS
    # ===============================

    elif page == "📄 Reports":


        st.header(
            "📄 Financial Reports"
        )



        if len(
            st.session_state.transactions
        ) > 0:



            df = pd.DataFrame(

                st.session_state.transactions

            )


            financial_advice(
                df
            )


            investment_advisor()


            tax_saving_advisor()


            report_section(
                df
            )


        else:


            st.warning(
                "Upload expenses to generate reports."
            )





# =====================================
# RUN
# =====================================

if __name__ == "__main__":

    main()
