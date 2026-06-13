# ==========================================
# AI FINANCIAL ADVISOR - WEEK 7-8
# PART 1/4
# ==========================================


import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from PIL import Image
import pytesseract

import re
import uuid
from datetime import datetime

from sklearn.linear_model import LinearRegression

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet


# ==========================================
# PAGE CONFIG
# ==========================================


st.set_page_config(
    page_title="AI Financial Advisor",
    page_icon="💰",
    layout="wide"
)


st.title(
    "💰 AI Financial Advisor & Expense Manager"
)


st.write(
    "AI powered personal finance assistant with prediction and smart insights"
)



# ==========================================
# DATA STORAGE
# ==========================================


if "transactions" not in st.session_state:

    st.session_state.transactions = []





# ==========================================
# OCR FUNCTIONS
# ==========================================


def extract_text(image):

    text = pytesseract.image_to_string(image)

    return text





def extract_amount(text):

    text = text.replace(",","")


    numbers = re.findall(
        r'\d+',
        text
    )


    values=[]


    for n in numbers:

        value=int(n)


        if 10 <= value <= 100000:

            values.append(value)



    if values:

        return max(values)


    return 0





def extract_date(text):


    date_pattern = r'\d{2}[/-]\d{2}[/-]\d{4}'


    result=re.search(
        date_pattern,
        text
    )


    if result:

        return result.group()


    return datetime.now().strftime(
        "%d-%m-%Y"
    )





# ==========================================
# MERCHANT DETECTION
# ==========================================


def detect_merchant(text):


    text=text.lower()



    merchants={

        "swiggy":"Swiggy",
        "zomato":"Zomato",
        "uber":"Uber",
        "ola":"Ola",
        "amazon":"Amazon",
        "flipkart":"Flipkart",
        "netflix":"Netflix",
        "prime":"Prime Video",
        "blinkit":"Blinkit",
        "zepto":"Zepto",
        "apollo":"Apollo Pharmacy"

    }



    for key,value in merchants.items():


        if key in text:

            return value



    return "Unknown"





# ==========================================
# CATEGORY SYSTEM
# ==========================================


def category_predict(merchant):


    merchant=merchant.lower()



    if merchant in [

        "swiggy",
        "zomato",
        "blinkit",
        "zepto"

    ]:

        return "Food"



    elif merchant in [

        "uber",
        "ola"

    ]:

        return "Transport"



    elif merchant in [

        "amazon",
        "flipkart"

    ]:

        return "Shopping"



    elif merchant in [

        "netflix",
        "prime video"

    ]:

        return "Entertainment"



    elif "apollo" in merchant:

        return "Healthcare"



    else:

        return "Others"





# ==========================================
# DATAFRAME CREATION
# ==========================================


def create_transaction(
        merchant,
        amount,
        date=None
):


    if date is None:

        date=datetime.now().strftime(
            "%d-%m-%Y"
        )



    return {

        "Date":date,

        "Merchant":merchant,

        "Amount":amount,

        "Category":
        category_predict(merchant)

    }





# ==========================================
# MACHINE LEARNING PREDICTION
# ==========================================


def predict_future_expense(df):


    if len(df)<3:

        return None



    data=df.copy()


    data["Index"]=range(
        len(data)
    )



    X=data[["Index"]]


    y=data["Amount"]



    model=LinearRegression()


    model.fit(
        X,
        y
    )



    future_index=[
        [len(data)+1]
    ]



    prediction=model.predict(
        future_index
    )


    return max(
        0,
        round(prediction[0])
    )
    # ==========================================
# PART 2/4
# ADVANCED DASHBOARD + AI ANALYTICS
# ==========================================



# ==========================================
# SPENDING TREND ANALYSIS
# ==========================================


def spending_trends(df):


    st.header("📈 Spending Trends")


    data=df.copy()



    if "Date" in data.columns:


        try:

            data["Date"]=pd.to_datetime(
                data["Date"],
                dayfirst=True
            )


            monthly=data.groupby(
                data["Date"].dt.month
            )["Amount"].sum()



            fig,ax=plt.subplots()


            monthly.plot(
                kind="line",
                marker="o",
                ax=ax
            )


            ax.set_title(
                "Monthly Spending Trend"
            )


            ax.set_xlabel(
                "Month"
            )


            ax.set_ylabel(
                "Amount (₹)"
            )


            st.pyplot(fig)



        except:

            st.info(
                "Not enough date data for trend analysis."
            )





# ==========================================
# CATEGORY ANALYSIS
# ==========================================


def category_analysis(df):


    st.header(
        "📊 Category Analysis"
    )


    category=df.groupby(
        "Category"
    )["Amount"].sum()



    col1,col2=st.columns(2)



    with col1:


        fig,ax=plt.subplots()


        category.plot(
            kind="pie",
            autopct="%1.1f%%",
            ax=ax
        )


        ax.set_ylabel("")


        ax.set_title(
            "Expense Distribution"
        )


        st.pyplot(fig)



    with col2:


        fig,ax=plt.subplots()


        category.plot(
            kind="bar",
            ax=ax
        )


        ax.set_title(
            "Category Spending"
        )


        ax.set_ylabel(
            "Amount ₹"
        )


        st.pyplot(fig)



    return category





# ==========================================
# SMART EXPENSE ALERT SYSTEM
# ==========================================


def unusual_expense_detection(df):


    st.header(
        "🚨 Smart Expense Detection"
    )


    if len(df)<2:

        st.info(
            "Add more transactions for AI detection."
        )

        return



    average=df["Amount"].mean()



    threshold=average*2



    unusual=df[
        df["Amount"] > threshold
    ]



    if len(unusual)>0:


        st.warning(
            "Unusual expenses detected!"
        )


        st.dataframe(
            unusual
        )


        for index,row in unusual.iterrows():

            st.error(

                f"""
                {row['Merchant']} expense of ₹{row['Amount']} 
                is higher than your normal spending.
                """

            )


    else:


        st.success(
            "No unusual spending detected."
        )





# ==========================================
# SAVING INSIGHTS
# ==========================================


def smart_suggestions(df):


    st.header(
        "💡 AI Spending Suggestions"
    )


    category=df.groupby(
        "Category"
    )["Amount"].sum()



    highest=category.idxmax()



    amount=category.max()



    st.info(

        f"""
        Your highest spending category is 
        **{highest}** with ₹{amount}.

        Consider reducing this category by 10-20%
        to improve savings.
        """

    )



    if highest=="Food":

        st.write(
            "Try reducing food delivery orders."
        )


    elif highest=="Shopping":

        st.write(
            "Review unnecessary online purchases."
        )


    elif highest=="Entertainment":

        st.write(
            "Check recurring subscriptions."
        )





# ==========================================
# ADVANCED DASHBOARD
# ==========================================


def advanced_dashboard(df):


    st.header(
        "📋 AI Financial Dashboard"
    )


    st.dataframe(
        df,
        use_container_width=True
    )



    total=df["Amount"].sum()



    col1,col2,col3=st.columns(3)



    with col1:

        st.metric(
            "Total Spending",
            f"₹{total}"
        )



    with col2:

        st.metric(
            "Transactions",
            len(df)
        )



    with col3:

        st.metric(
            "Average Expense",
            f"₹{round(df['Amount'].mean())}"
        )



    category=category_analysis(
        df
    )



    spending_trends(
        df
    )



    unusual_expense_detection(
        df
    )


    smart_suggestions(
        df
    )



    prediction=predict_future_expense(
        df
    )


    if prediction:


        st.header(
            "🔮 ML Expense Prediction"
        )


        st.success(

            f"""
            Predicted next expense:
            ₹{prediction}
            """

        )



    return category,total
    # ==========================================
# PART 3/4
# AI ASSISTANT + REPORT GENERATION
# ==========================================



# ==========================================
# AI FINANCIAL CHAT ASSISTANT
# ==========================================


def financial_chatbot(df):


    st.header(
        "🤖 AI Financial Assistant"
    )


    question=st.text_input(
        "Ask your finance question"
    )



    if question:


        category=df.groupby(
            "Category"
        )["Amount"].sum()



        highest=category.idxmax()


        total=df["Amount"].sum()



        question=question.lower()



        if "save" in question:


            st.success(

                f"""
                Your total spending is ₹{total}.
                
                Your highest expense category is {highest}.
                
                Reduce spending in this category
                and save at least 10-20%.
                """

            )



        elif "investment" in question:


            st.info(

                """
                Suggested options:

                📈 SIP - Long term wealth creation

                🏦 PPF - Safe government savings

                💹 ELSS - Tax saving mutual fund

                🛡 Emergency Fund - 3-6 months expenses

                """

            )



        elif "budget" in question:


            average=df["Amount"].mean()



            st.write(

                f"""
                Your average transaction is ₹{round(average)}.

                Create a monthly budget based on
                your income and savings goals.
                """

            )



        else:


            st.info(

                """
                Try asking:

                • How can I save money?

                • Where should I invest?

                • How can I reduce expenses?

                • How much should I budget?

                """

            )





# ==========================================
# FINANCIAL HEALTH SCORE
# ==========================================


def financial_health(total):


    st.header(
        "❤️ Financial Health Score"
    )


    score=100



    if total>50000:

        score-=30


    elif total>20000:

        score-=15



    if score>=80:


        st.success(
            f"Score: {score}/100 Excellent"
        )


    elif score>=50:


        st.warning(
            f"Score: {score}/100 Average"
        )


    else:


        st.error(
            f"Score: {score}/100 Needs Improvement"
        )





# ==========================================
# INDIAN INVESTMENT ADVISOR
# ==========================================


def investment_advisor():


    st.header(
        "🇮🇳 Indian Investment Advisor"
    )


    st.write(

"""
### Suggested Financial Products

📈 SIP:
Invest regularly in mutual funds.

🏦 PPF:
Government-backed long-term savings.

💹 ELSS:
Tax-saving equity investment.

🛡 Emergency Fund:
Keep 3-6 months expenses separately.

"""

    )





# ==========================================
# TAX SAVING ADVISOR
# ==========================================


def tax_saving_advisor():


    st.header(
        "📑 Tax Saving Advisor"
    )


    income=st.number_input(

        "Annual Income",

        min_value=0,

        value=600000,

        key=f"income_{uuid.uuid4()}"

    )



    if income>500000:


        st.info(

"""
Possible tax-saving options:

✅ ELSS Mutual Funds

✅ PPF

✅ NPS

✅ Insurance deductions

"""

        )


    else:


        st.success(

            "Explore investments according to your goals."

        )





# ==========================================
# PDF REPORT GENERATOR
# ==========================================


def generate_pdf(df):


    filename="financial_report.pdf"



    doc=SimpleDocTemplate(
        filename
    )


    styles=getSampleStyleSheet()



    content=[]



    total=df["Amount"].sum()



    category=df.groupby(
        "Category"
    )["Amount"].sum()



    highest=category.idxmax()



    text=f"""

    AI Financial Report

    Total Spending:
    ₹{total}


    Highest Spending Category:
    {highest}


    Number of Transactions:
    {len(df)}


    Recommendation:

    Reduce unnecessary expenses
    and increase savings.

    """



    content.append(

        Paragraph(
            text,
            styles["Normal"]
        )

    )


    content.append(
        Spacer(1,20)
    )



    doc.build(
        content
    )



    return filename





# ==========================================
# REPORT SECTION
# ==========================================


def report_section(df):


    st.header(
        "📄 Financial Report"
    )



    if st.button(
        "Generate PDF Report",
        key=f"pdf_{uuid.uuid4()}"
    ):


        file=generate_pdf(
            df
        )


        with open(file,"rb") as pdf:


            st.download_button(

                "Download PDF",

                pdf,

                file_name=file,

                key=f"download_pdf_{uuid.uuid4()}"

            )
            # ==========================================
# PART 4/4
# MAIN APPLICATION
# ==========================================



def main():

    st.sidebar.title("💰 AI Financial Advisor")

    page = st.sidebar.radio(
        "Go To",
        [
            "🏠 Dashboard",
            "📷 Upload Receipt",
            "📂 Upload CSV",
            "🤖 AI Assistant",
            "📄 Reports"
        ]
    )


    # Create dataframe

    if len(st.session_state.transactions) > 0:

        df = pd.DataFrame(
            st.session_state.transactions
        )

    else:

        df = pd.DataFrame(
            columns=[
                "Date",
                "Merchant",
                "Amount",
                "Category"
            ]
        )


    # ==========================
    # DASHBOARD PAGE
    # ==========================

    if page == "🏠 Dashboard":


        st.title(
            "📊 Financial Dashboard"
        )


        if len(df)>0:

            advanced_dashboard(df)

        else:

            st.info(
                "Upload expenses to view dashboard"
            )



    # ==========================
    # CSV PAGE
    # ==========================

    elif page == "📂 Upload CSV":


        st.title(
            "📂 Upload Expense CSV"
        )


        csv_file = st.file_uploader(
            "Choose CSV",
            type="csv"
        )


        if csv_file:


            df = pd.read_csv(
                csv_file
            )


            st.session_state.transactions = (
                df.to_dict("records")
            )


            st.success(
                "CSV Added Successfully"
            )



    # ==========================
    # RECEIPT PAGE
    # ==========================


    elif page == "📷 Upload Receipt":


        st.title(
            "📷 Scan Payment Screenshot"
        )


        images = st.file_uploader(
            "Upload Receipt",
            type=[
                "png",
                "jpg",
                "jpeg"
            ],
            accept_multiple_files=True
        )


        if images:


            for img in images:


                image = Image.open(img)

                st.image(image)


                text = extract_text(image)


                amount = extract_amount(text)

                merchant = detect_merchant(text)


                transaction = create_transaction(
                    merchant,
                    amount
                )


                st.session_state.transactions.append(
                    transaction
                )


            st.success(
                "Receipt Added"
            )



    # ==========================
    # AI ASSISTANT
    # ==========================


    elif page == "🤖 AI Assistant":


        st.title(
            "🤖 AI Financial Assistant"
        )


        if len(df)>0:

            financial_chatbot(df)

        else:

            st.warning(
                "Add expenses first"
            )



    # ==========================
    # REPORT PAGE
    # ==========================


    elif page == "📄 Reports":


        st.title(
            "📄 Financial Reports"
        )


        if len(df)>0:


            financial_health(
                df["Amount"].sum()
            )


            investment_advisor()


            tax_saving_advisor()


            report_section(df)


        else:

            st.info(
                "No data available"
            )
