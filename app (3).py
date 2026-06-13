import streamlit as st
import pytesseract
from PIL import Image
import pandas as pd
import matplotlib.pyplot as plt
import re


def setup_app():
    st.title("AI Financial Advisor & Expense Manager")
    st.write("Track expenses and get financial insights")


def upload_images():

    uploaded_files = st.file_uploader(
        "Upload Payment Screenshots",
        type=["png", "jpg", "jpeg"],
        accept_multiple_files=True
    )

    return uploaded_files


def upload_csv():

    csv_file = st.file_uploader(
        "Upload Expense CSV",
        type=["csv"]
    )

    return csv_file


def extract_text(image):

    text = pytesseract.image_to_string(image)

    return text


def detect_amount(text):

    amount_value = None

    match1 = re.search(r'₹\s*(\d+)', text)

    if match1:
        amount_value = int(match1.group(1))

    if not amount_value:

        match2 = re.search(r'(\d+)\s*Rupees', text)

        if match2:
            amount_value = int(match2.group(1))

    if not amount_value:

        numbers = re.findall(r'\d{2,4}', text)

        numbers = [int(x) for x in numbers if 10 <= int(x) <= 5000]

        if numbers:
            amount_value = min(numbers)

    return amount_value


def detect_merchant(text):

    text_lower = text.lower()

    if "swiggy" in text_lower:
        return "Swiggy"

    elif "zomato" in text_lower:
        return "Zomato"

    elif "netflix" in text_lower:
        return "Netflix"

    elif "uber" in text_lower:
        return "Uber"

    elif "ola" in text_lower:
        return "Ola"

    match = re.search(r'To:\s*([A-Za-z ]+)', text)

    if match:
        return match.group(1).strip()

    return "Unknown"


def detect_category(merchant):

    merchant = merchant.lower()

    if merchant in ["swiggy", "zomato"]:
        return "Food"

    elif merchant in ["uber", "ola"]:
        return "Transport"

    elif merchant in ["netflix", "prime"]:
        return "Entertainment"

    else:
        return "Transfer"


def financial_advice(category_spending, total_spent):

    st.header("Financial Advice")

    if "Food" in category_spending.index:

        if category_spending["Food"] > 2000:
            st.warning("High spending on food. Try reducing food delivery expenses.")
        else:
            st.success("Food spending is under control.")

    if "Transport" in category_spending.index:

        if category_spending["Transport"] > 1500:
            st.warning("Transport expenses are high.")
        else:
            st.success("Transport spending looks reasonable.")

    if "Entertainment" in category_spending.index:

        if category_spending["Entertainment"] > 1000:
            st.warning("Entertainment spending is high.")
        else:
            st.success("Entertainment spending is balanced.")

    if total_spent > 5000:
        st.error("Overall spending is high. Consider budgeting.")

    elif total_spent > 2000:
        st.info("Moderate spending. Track expenses carefully.")

    else:
        st.success("Great! Your spending is under control.")


def guru_advice(category_spending):

    st.header("Guru Based Advice")

    advice = {

        "Food":
        "Warren Buffett: Avoid unnecessary recurring food delivery expenses.",

        "Transport":
        "Ramit Sethi: Optimize recurring transportation costs.",

        "Entertainment":
        "Robert Kiyosaki: Spend money on assets before liabilities."
    }

    for category in category_spending.index:

        if category in advice:
            st.info(f"{category}: {advice[category]}")


def personalized_recommendation(
        category_spending,
        total_spent
):

    st.header("Personalized Recommendations")

    highest = category_spending.idxmax()

    if highest == "Food":

        st.warning(
            "Food expenses are highest. Consider cooking at home more often."
        )

    elif highest == "Transport":

        st.warning(
            "Transport costs are high. Try public transport or carpooling."
        )

    elif highest == "Entertainment":

        st.warning(
            "Entertainment spending is high. Review subscriptions regularly."
        )

    if total_spent > 5000:

        st.error(
            "You crossed ₹5000 spending. Create a stricter monthly budget."
        )

    else:

        st.success(
            "Your spending pattern looks healthy."
        )


def show_dashboard(df):

    st.subheader("All Transactions")
    st.write(df)

    total_spent = df["Amount"].sum()

    st.header("Total Amount Spent")
    st.write(f"₹ {total_spent}")

    budget = st.number_input(
        "Enter Monthly Budget",
        min_value=1000,
        value=5000
        key=f"budget_{len(df)}"
    )
    

    remaining = budget - total_spent

    st.header("Budget Tracker")

    st.write(f"Budget: ₹{budget}")
    st.write(f"Remaining Budget: ₹{remaining}")

    if total_spent > budget:
        st.error("Budget Exceeded!")
    else:
        st.success("Within Budget")

    category_spending = df.groupby(
        "Category"
    )["Amount"].sum()

    st.header("Category Spending")
    st.write(category_spending)

    st.header("Spending Insights")

    highest_category = category_spending.idxmax()
    highest_amount = category_spending.max()

    st.write(
        f"Highest Spending Category: {highest_category}"
    )

    st.write(
        f"Amount Spent: ₹{highest_amount}"
    )

    avg_transaction = total_spent / len(df)

    st.write(
        f"Average Transaction Amount: ₹{avg_transaction:.2f}"
    )

    fig1, ax1 = plt.subplots()

    category_spending.plot(
        kind="pie",
        autopct="%1.1f%%",
        ax=ax1
    )

    plt.title("Expense Distribution")
    plt.ylabel("")

    st.pyplot(fig1)

    fig2, ax2 = plt.subplots()

    category_spending.plot(
        kind="bar",
        ax=ax2
    )

    plt.title("Category Spending")

    st.pyplot(fig2)

    st.header("Expense Summary")

    st.write(
        f"Total Transactions: {len(df)}"
    )

    st.write(
        f"Total Spent: ₹{total_spent}"
    )

    st.write(
        f"Highest Spending Category: {highest_category}"
    )

    return category_spending, total_spent


def main():

    setup_app()

    transactions = []

    st.header("Manual Expense Entry")

    manual_merchant = st.text_input(
        "Merchant Name"
    )

    manual_amount = st.number_input(
        "Amount",
        min_value=0
    )

    if st.button("Add Expense"):

        manual_category = detect_category(
            manual_merchant
        )

        transactions.append({

            "Merchant": manual_merchant,

            "Amount": manual_amount,

            "Category": manual_category
        })

        st.success(
            "Expense Added Successfully!"
        )

    csv_file = upload_csv()

    if csv_file:

        csv_df = pd.read_csv(csv_file)

        st.subheader("CSV Transactions")

        st.write(csv_df)

        if (
            "Merchant" in csv_df.columns
            and
            "Amount" in csv_df.columns
            and
            "Category" in csv_df.columns
        ):

            category_spending, total_spent = show_dashboard(csv_df)

            financial_advice(
                category_spending,
                total_spent
            )

            guru_advice(
                category_spending
            )

            personalized_recommendation(
                category_spending,
                total_spent
            )

    uploaded_files = upload_images()

    if uploaded_files:

        for file in uploaded_files:

            image = Image.open(file)

            st.image(
                image,
                caption=file.name
            )

            text = extract_text(image)

            amount = detect_amount(text)

            merchant = detect_merchant(text)

            category = detect_category(merchant)

            if amount is not None:

                transactions.append({

                    "Merchant": merchant,

                    "Amount": amount,

                    "Category": category
                })

        if len(transactions) > 0:

            df = pd.DataFrame(transactions)

            category_spending, total_spent = show_dashboard(df)

            financial_advice(
                category_spending,
                total_spent
            )

            guru_advice(
                category_spending
            )

            personalized_recommendation(
                category_spending,
                total_spent
            )


if __name__ == "__main__":
    main()

