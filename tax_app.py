import streamlit as st

# Tax calculation function (as we discussed earlier)
def calculate_tax(
    salary_income,
    other_income,
    regime='new',
    deductions=None,
    hra_exemption=0,
    home_loan_interest=0
):
    if deductions is None:
        deductions = {}
    
    gross_income = salary_income + other_income
    standard_deduction = 50000
    total_deductions = 0

    if regime == 'old':
        total_deductions += standard_deduction
        total_deductions += deductions.get('80C', 0)
        total_deductions += deductions.get('80D', 0)
        total_deductions += home_loan_interest
        total_deductions += hra_exemption
    elif regime == 'new':
        total_deductions += standard_deduction

    taxable_income = max(0, gross_income - total_deductions)

    tax = 0
    if regime == 'old':
        if taxable_income <= 250000:
            tax = 0
        elif taxable_income <= 500000:
            tax = (taxable_income - 250000) * 0.05
        elif taxable_income <= 1000000:
            tax = (250000 * 0.05) + (taxable_income - 500000) * 0.20
        else:
            tax = (250000 * 0.05) + (500000 * 0.20) + (taxable_income - 1000000) * 0.30
        if taxable_income <= 500000:
            tax = 0
    elif regime == 'new':
        slabs = [(300000, 0.0), (300000, 0.05), (300000, 0.10),
                 (300000, 0.15), (300000, 0.20), (float('inf'), 0.30)]
        remaining = taxable_income
        for slab_amount, rate in slabs:
            if remaining <= 0:
                break
            amount_in_slab = min(slab_amount, remaining)
            tax += amount_in_slab * rate
            remaining -= amount_in_slab
        if taxable_income <= 700000:
            tax = 0

    cess = tax * 0.04
    total_tax = tax + cess

    return {
        'Gross Income': gross_income,
        'Total Deductions': total_deductions,
        'Taxable Income': taxable_income,
        'Tax (Before Cess)': tax,
        'Cess (4%)': cess,
        'Total Tax Payable': total_tax
    }

# Streamlit UI
st.set_page_config(page_title="Income Tax Calculator", layout="centered")
st.title("🧾 Personal Income Tax Calculator (AY 2024–25)")
st.markdown("Built using the latest income tax slabs and deductions under Old and New Regimes.")

# Inputs
st.header("Enter Your Income Details")
salary = st.number_input("Salary Income (₹)", min_value=0, step=1000)
other_income = st.number_input("Other Income (₹)", min_value=0, step=1000)

regime = st.radio("Select Tax Regime", options=["old", "new"], horizontal=True)

st.header("Deductions (Old Regime Only)")
d80c = st.number_input("80C (Max ₹1.5L)", min_value=0, max_value=150000, step=1000)
d80d = st.number_input("80D (Health Premium)", min_value=0, step=500)
hra = st.number_input("HRA Exemption", min_value=0, step=1000)
home_loan = st.number_input("Home Loan Interest (Sec 24b)", min_value=0, step=1000)

# Submit
if st.button("Calculate Tax"):
    result = calculate_tax(
        salary_income=salary,
        other_income=other_income,
        regime=regime,
        deductions={'80C': d80c, '80D': d80d},
        hra_exemption=hra,
        home_loan_interest=home_loan
    )

    st.subheader("📊 Results")
    st.write(f"**Gross Income:** ₹{result['Gross Income']:,}")
    st.write(f"**Total Deductions:** ₹{result['Total Deductions']:,}")
    st.write(f"**Taxable Income:** ₹{result['Taxable Income']:,}")
    st.write(f"**Tax Before Cess:** ₹{result['Tax (Before Cess)']:,}")
    st.write(f"**Cess (4%):** ₹{result['Cess (4%)']:,}")
    st.success(f"**Total Tax Payable: ₹{result['Total Tax Payable']:,}**")
