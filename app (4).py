import streamlit as st
import pytesseract
from PIL import Image
import pandas as pd
import matplotlib.pyplot as plt
import re
from datetime import datetime


# ================= APP CONFIG =================

def setup_app():

    st.set_page_config(
        page_title="AI Financial Advisor",
        page_icon="💰",
        layout="wide"
    )

    st.title("💰 AI Financial Advisor & Expense Manager")
    st.write(
        "AI-powered expense tracking, Indian financial planning and personalized advice."
    )



# ================= FILE UPLOAD =================

def upload_images():

    return st.file_uploader(
        "Upload Payment Screenshots",
        type=["png","jpg","jpeg"],
        accept_multiple_files=True
    )



def upload_csv():

    return st.file_uploader(
        "Upload UPI / Expense CSV",
        type=["csv"]
    )



# ================= OCR EXTRACTION =================

def extract_text(image):

    return pytesseract.image_to_string(image)



def detect_amount(text):

    amount = None


    match = re.search(
        r'₹\s?([\d,]+)',
        text
    )

    if match:

        amount = match.group(1)

        amount = int(
            amount.replace(",","")
        )


    if amount is None:

        numbers = re.findall(
            r'\d{2,6}',
            text
        )

        numbers = [
            int(x)
            for x in numbers
            if 10 <= int(x) <= 100000
        ]


        if numbers:

            amount = min(numbers)


    return amount




# ================= MERCHANT DETECTION =================


def detect_merchant(text):

    text=text.lower()


    merchant_keywords={

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
        "apollo":"Healthcare",
        "medplus":"Healthcare"

    }


    for key,value in merchant_keywords.items():

        if key in text:

            return value



    return "Unknown"




# ================= CATEGORY SYSTEM =================


def detect_category(merchant):

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



    elif merchant=="healthcare":

        return "Healthcare"



    else:

        return "Others"




# ================= INDIAN CURRENCY =================


def indian_currency(amount):

    amount=int(amount)

    return "₹{:,.0f}".format(amount)




# ================= INDIAN FINANCE ADVISOR =================


def indian_finance_advisor(total,category):


    st.header("🇮🇳 Indian Personal Finance Advisor")


    st.info(
        """
### Investment Recommendations

🏦 PPF:
Safe long-term savings option with tax benefits.

📈 SIP:
Invest fixed amounts regularly for long-term wealth creation.

💹 ELSS:
Tax-saving mutual fund option with equity exposure.

🛡 Emergency Fund:
Maintain 3-6 months of expenses as savings.
"""
    )


    if total>30000:

        st.warning(
            "Your expenses are high. Try increasing savings and reducing unnecessary spending."
        )

    else:

        st.success(
            "Your spending is controlled. Continue saving and investing regularly."
        )



# ================= TAX SAVING MODULE =================


def tax_saving_advisor():

    st.header("📑 Tax Saving Recommendations")


    income=st.number_input(
        "Enter Annual Income (₹)",
        min_value=0,
        value=500000
    )


    if income>500000:


        st.write(
            """
Possible tax-saving options:

✅ ELSS Mutual Funds  
✅ PPF Investment  
✅ National Pension System (NPS)  
✅ Insurance deductions  
"""
        )


    else:

        st.success(
            "Explore basic savings and investment options."
        )




# ================= UPI ANALYSIS =================


def upi_analysis(df):


    st.header("📱 UPI Transaction Analysis")


    total=df["Amount"].sum()


    st.write(
        "Total UPI Spending:",
        indian_currency(total)
    )


    category=df.groupby(
        "Category"
    )["Amount"].sum()


    highest=category.idxmax()


    st.warning(
        f"Highest spending category: {highest}"
    )


    st.write(
        "Recommendation: Reduce spending in your highest category by 10-15%."
    )
    # ================= FINANCIAL HEALTH SCORE =================


def financial_health_score(total, budget):


    st.header("❤️ Financial Health Score")


    score = 100


    if total > budget:

        score -= 30


    elif total > budget*0.8:

        score -= 15



    if score >= 80:

        st.success(
            f"Financial Health Score: {score}/100 - Excellent"
        )


    elif score >= 50:

        st.warning(
            f"Financial Health Score: {score}/100 - Needs Improvement"
        )


    else:

        st.error(
            f"Financial Health Score: {score}/100 - Poor"
        )




# ================= EXPENSE PREDICTION =================


def expense_prediction(df):


    st.header("🔮 Future Expense Prediction")


    average = df["Amount"].mean()


    predicted = average * len(df)


    st.write(
        "Average Transaction:",
        indian_currency(average)
    )


    st.write(
        "Expected Future Spending:",
        indian_currency(predicted)
    )


    st.info(
        "Prediction is based on previous spending patterns."
    )




# ================= SAVINGS GOAL TRACKER =================


def savings_goal_tracker():


    st.header("🎯 Goal Based Savings Tracker")


    goal = st.text_input(
        "Enter your financial goal"
    )


    target = st.number_input(
        "Target Amount (₹)",
        min_value=0,
        value=50000
    )


    saved = st.number_input(
        "Current Savings (₹)",
        min_value=0,
        value=10000
    )


    if target>0:


        progress = saved/target


        st.progress(
            min(progress,1.0)
        )


        remaining = target-saved


        st.write(
            "Remaining:",
            indian_currency(remaining)
        )


        if remaining<=0:

            st.success(
                "Goal achieved!"
            )


        else:

            st.info(
                f"Save {indian_currency(remaining)} more to reach your goal."
            )




# ================= DASHBOARD =================


def show_dashboard(df):


    st.subheader("📋 Transactions")

    st.dataframe(df)



    total=df["Amount"].sum()



    st.header("Total Spending")

    st.write(
        indian_currency(total)
    )



    budget=st.number_input(

        "Monthly Budget",

        min_value=1000,

        value=50000

    )



    remaining=budget-total



    st.header("Budget Status")


    st.write(
        "Budget:",
        indian_currency(budget)
    )


    st.write(
        "Remaining:",
        indian_currency(remaining)
    )



    if remaining<0:

        st.error(
            "Budget exceeded!"
        )

    else:

        st.success(
            "Within budget"
        )



    category=df.groupby(
        "Category"
    )["Amount"].sum()



    st.header("Category Analysis")

    st.write(category)



    fig,ax=plt.subplots()


    category.plot(

        kind="pie",

        autopct="%1.1f%%",

        ax=ax

    )


    plt.ylabel("")

    st.pyplot(fig)



    fig2,ax2=plt.subplots()


    category.plot(

        kind="bar",

        ax=ax2

    )


    st.pyplot(fig2)



    st.download_button(

        "⬇ Download Financial Report",

        df.to_csv(index=False),

        "financial_report.csv"

    )



    financial_health_score(
        total,
        budget
    )


    expense_prediction(df)


    return category,total




# ================= MAIN APPLICATION =================


def main():


    setup_app()


    transactions=[]



    st.header("✍ Manual Expense Entry")


    merchant=st.text_input(
        "Merchant Name"
    )


    amount=st.number_input(

        "Amount",

        min_value=0

    )



    if st.button("Add Expense"):


        transactions.append({

            "Date":
            datetime.now().strftime("%d-%m-%Y"),

            "Merchant":
            merchant,

            "Amount":
            amount,

            "Category":
            detect_category(merchant)

        })


        st.success(
            "Expense Added"
        )




    # CSV UPLOAD

    csv_file=upload_csv()



    if csv_file:


        df=pd.read_csv(csv_file)



        if "Category" not in df.columns:


            df["Category"]=df["Merchant"].apply(
                detect_category
            )



        category,total=show_dashboard(df)



        indian_finance_advisor(
            total,
            category
        )


        tax_saving_advisor()


        upi_analysis(df)


        savings_goal_tracker()




    # IMAGE UPLOAD


    images=upload_images()



    if images:


        for img_file in images:


            image=Image.open(img_file)



            st.image(
                image,
                caption=img_file.name
            )



            text=extract_text(image)



            amount=detect_amount(text)



            merchant=detect_merchant(text)



            if amount:


                transactions.append({

                    "Date":
                    datetime.now().strftime("%d-%m-%Y"),


                    "Merchant":
                    merchant,


                    "Amount":
                    amount,


                    "Category":
                    detect_category(merchant)

                })



        if transactions:


            df=pd.DataFrame(
                transactions
            )


            category,total=show_dashboard(df)



            indian_finance_advisor(
                total,
                category
            )


            tax_saving_advisor()


            upi_analysis(df)


            savings_goal_tracker()




# ================= RUN =================


if __name__=="__main__":

    main()
