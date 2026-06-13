import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import pytesseract
from PIL import Image
import re
from datetime import datetime


# ==========================
# APP CONFIG
# ==========================

st.set_page_config(
    page_title="AI Financial Advisor",
    page_icon="💰",
    layout="wide"
)


st.title("💰 AI Financial Advisor & Expense Manager")
st.write(
    "AI-powered expense tracking and Indian personal finance assistant"
)



# ==========================
# OCR FUNCTIONS
# ==========================

def extract_text(image):

    return pytesseract.image_to_string(image)



def detect_amount(text):

    matches = re.findall(
        r'\d+',
        text.replace(",","")
    )

    amounts=[]

    for x in matches:

        value=int(x)

        if 10 <= value <= 100000:

            amounts.append(value)


    if amounts:

        return max(amounts)


    return 0




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





# ==========================
# CATEGORY SYSTEM
# ==========================


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


    elif "apollo" in merchant:

        return "Healthcare"


    else:

        return "Others"





# ==========================
# CURRENCY FORMAT
# ==========================

def money(value):

    return f"₹{value:,.0f}"





# ==========================
# INDIAN FINANCE ADVICE
# ==========================


def indian_finance_advisor(total):


    st.header("🇮🇳 Indian Financial Advisor")


    st.info(
"""
### Investment Suggestions

📈 SIP:
Invest a fixed amount regularly for long-term wealth creation.

🏦 PPF:
Safe government-backed long-term savings option.

💹 ELSS:
Tax-saving mutual fund option.

🛡 Emergency Fund:
Maintain 3-6 months of expenses.
"""
    )


    if total > 30000:

        st.warning(
            "Your spending is high. Try reducing unnecessary expenses and increase savings."
        )

    else:

        st.success(
            "Your spending is under control. Continue saving and investing."
        )





# ==========================
# TAX SAVING
# ==========================


def tax_advisor():


    st.header("📑 Tax Saving Suggestions")


    income=st.number_input(
        "Annual Income",
        min_value=0,
        value=600000,
        key="tax_income"
        
    )


    if income>500000:

        st.write(
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
            "Explore savings and investment options according to your goals."
        )





# ==========================
# UPI ANALYSIS
# ==========================


def upi_analysis(df):


    st.header("📱 UPI Spending Analysis")


    category=df.groupby(
        "Category"
    )["Amount"].sum()


    st.write(category)


    highest=category.idxmax()


    st.warning(
        f"Highest spending category: {highest}"
    )


    st.info(
        "Suggestion: Reduce spending in your highest category by 10-15%."
    )
    # ==========================
# GURU ADVICE
# ==========================


def guru_advice(category):


    st.header("📚 Financial Guru Advice")


    advice={

        "Food":
        "Warren Buffett: Avoid unnecessary recurring expenses.",

        "Shopping":
        "Robert Kiyosaki: Buy assets before liabilities.",

        "Entertainment":
        "Ramit Sethi: Spend consciously on things you value.",

        "Transport":
        "Optimize recurring costs to improve savings."

    }


    for item in category.index:

        if item in advice:

            st.info(
                f"{item}: {advice[item]}"
            )





# ==========================
# FINANCIAL HEALTH SCORE
# ==========================


def health_score(total,budget):


    st.header("❤️ Financial Health Score")


    score=100


    if total > budget:

        score-=30


    elif total > budget*0.8:

        score-=15



    if score>=80:

        st.success(
            f"Score: {score}/100 - Excellent"
        )


    elif score>=50:

        st.warning(
            f"Score: {score}/100 - Average"
        )


    else:

        st.error(
            f"Score: {score}/100 - Needs Improvement"
        )





# ==========================
# EXPENSE PREDICTION
# ==========================


def expense_prediction(df):


    st.header("🔮 Expense Prediction")


    average=df["Amount"].mean()


    predicted=average*len(df)


    st.write(
        "Average Transaction:",
        money(average)
    )


    st.write(
        "Expected Future Spending:",
        money(predicted)
    )


    st.info(
        "Prediction is calculated from previous spending behaviour."
    )





# ==========================
# SAVINGS GOAL TRACKER
# ==========================


def savings_goal_tracker():


    st.header("🎯 Savings Goal Tracker")


    goal=st.text_input(
        "Financial Goal",
        placeholder="Example: Emergency Fund",
        key="goal_name"
    )


    target=st.number_input(
        "Target Amount",
        min_value=0,
        value=100000
        
    )


    saved=st.number_input(
        "Current Savings",
        min_value=0,
        value=25000
        
    )


    if target>0:


        progress=saved/target


        if progress>1:

            progress=1



        st.progress(progress)


        remaining=target-saved


        st.write(
            "Remaining:",
            money(remaining)
        )


        if remaining<=0:

            st.success(
                "Goal Completed 🎉"
            )

        else:

            st.info(
                "Keep saving to achieve your goal."
            )





# ==========================
# DASHBOARD
# ==========================


def dashboard(df):


    st.header("📋 Transactions")


    st.dataframe(df)



    total=df["Amount"].sum()



    st.header("💰 Total Spending")

    st.write(
        money(total)
    )



    budget=st.number_input(

        "Monthly Budget",

        min_value=1000,

        value=50000,
        key=f"budget_{len(df)}_{df['Amount'].sum()}"

        

    )



    remaining=budget-total



    st.header("📊 Budget Tracker")


    st.write(
        "Budget:",
        money(budget)
    )


    st.write(
        "Remaining:",
        money(remaining)
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



    st.header("Category Spending")


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

        "⬇ Download Report",

        df.to_csv(index=False),

        file_name="financial_report.csv",
        key=f"download_report_{len(df)}_{int(df['Amount'].sum())}"

    )



    health_score(
        total,
        budget
    )


    expense_prediction(df)



    return category,total
    # ==========================
# MAIN APPLICATION
# ==========================


def main():


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
            "Expense Added Successfully"
        )





    # ==========================
    # CSV UPLOAD
    # ==========================


    st.header("📂 Upload UPI / Expense CSV")


    csv_file=st.file_uploader(

        "Upload CSV",

        type=["csv"]

    )



    if csv_file:


        df=pd.read_csv(csv_file)



        # Automatically create category

        if "Category" not in df.columns:


            df["Category"]=df["Merchant"].apply(
                detect_category
            )



        category,total=dashboard(df)



        indian_finance_advisor(
            total
        )


        guru_advice(
            category
        )


        tax_advisor()


        upi_analysis(
            df
        )


        savings_goal_tracker()






    # ==========================
    # IMAGE UPLOAD
    # ==========================


    st.header("📷 Upload Payment Screenshot")


    images=st.file_uploader(

        "Upload Screenshot",

        type=["png","jpg","jpeg"],

        accept_multiple_files=True,

        key="image_upload"

    )



    if images:


        image_transactions=[]



        for file in images:


            image=Image.open(file)


            st.image(
                image,
                caption=file.name
            )



            text=extract_text(image)



            amount=detect_amount(text)



            merchant=detect_merchant(text)



            category=detect_category(
                merchant
            )



            image_transactions.append({

                "Date":
                datetime.now().strftime("%d-%m-%Y"),

                "Merchant":
                merchant,

                "Amount":
                amount,

                "Category":
                category

            })




        if image_transactions:


            df=pd.DataFrame(
                image_transactions
            )



            category,total=dashboard(df)



            indian_finance_advisor(
                total
            )


            guru_advice(
                category
            )


            tax_advisor()


            upi_analysis(
                df
            )


            savings_goal_tracker()





# ==========================
# START APP
# ==========================


if __name__=="__main__":

    main()
