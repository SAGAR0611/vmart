import streamlit as st
import requests
import os
import json
import re
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("API_URL", "http://localhost:8000")

# Configure the page
st.set_page_config(
    page_title="VMart Inventory Management",
    page_icon="🏪",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .title-container {
        background: linear-gradient(90deg, #1E88E5 0%, #1565C0 100%);
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .main-title {
        color: white;
        text-align: center;
        font-size: 3rem !important;
        font-weight: 600;
        margin: 0;
        padding: 0;
    }
    .subtitle {
        color: #E3F2FD;
        text-align: center;
        font-size: 1.2rem !important;
        margin: 0;
        padding: 0;
    }
    </style>
    <div class="title-container">
        <h1 class="main-title">VMart Inventory Management</h1>
        <p class="subtitle">Streamline your inventory tracking and bill management</p>
    </div>
""", unsafe_allow_html=True)

# Sidebar configuration
st.sidebar.image("https://img.icons8.com/fluency/96/shop.png", width=96)
st.sidebar.markdown("## Navigation")
option = st.sidebar.radio(
    "",
    ["📋 View Inventory", "📤 Upload Inventory"],
    label_visibility="collapsed"
)

def parse_bill_from_text(raw_text):
    """Helper function to parse bill JSON from raw text"""
    if not raw_text:
        return None
        
    match = re.search(r"```json\s*(\{.*?\})\s*```", raw_text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            pass
    return None

def display_bill_details(data):
    """Helper function to display bill details in a consistent format"""
    # Parse bill data from raw text if needed
    bill_data = data
    if "raw_text" in data:
        parsed = parse_bill_from_text(data["raw_text"])
        if parsed:
            bill_data = parsed
        else:
            st.json(data)
            return

    with st.expander(f"Bill #{bill_data.get('bill_no', 'Unknown')}"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Bill Details:**")
            st.write(f"Bill No: {bill_data.get('bill_no', '')}")
            st.write(f"Date: {bill_data.get('date', '')}")
            st.write(f"Customer: {bill_data.get('customer', '')}")
            st.write(f"Phone: {bill_data.get('customer_phone', '')}")

        with col2:
            st.write("**Vendor Details:**")
            st.write(f"Name: {bill_data.get('vendor', '')}")
            st.write(f"Address: {bill_data.get('vendor_address', '')}")

        st.write("**Items:**")
        items = bill_data.get("items", [])
        if items:
            # Convert items to ensure numeric values are float
            processed_items = []
            for item in items:
                processed_item = item.copy()
                for field in ['rate', 'amount', 'quantity']:
                    if field in processed_item:
                        try:
                            processed_item[field] = float(processed_item[field])
                        except (ValueError, TypeError):
                            processed_item[field] = 0.0
                processed_items.append(processed_item)
            
            df = pd.DataFrame(processed_items)
            st.dataframe(
                df,
                column_config={
                    "hsn": "HSN",
                    "description": "Description",
                    "quantity": "Quantity",
                    "rate": st.column_config.NumberColumn("Rate", format="₹%.2f"),
                    "amount": st.column_config.NumberColumn("Amount", format="₹%.2f")
                },
                hide_index=True
            )

        col3, col4 = st.columns(2)
        with col3:
            st.write("**Totals:**")
            st.write(f"Sub Total: ₹{float(bill_data.get('total', 0)):.2f}")
            st.write(f"CGST: ₹{float(bill_data.get('cgst', 0)):.2f}")
            st.write(f"SGST: ₹{float(bill_data.get('sgst', 0)):.2f}")
            st.write(f"IGST: ₹{float(bill_data.get('igst', 0)):.2f}")
            st.write(f"**Grand Total: ₹{float(bill_data.get('grand_total', 0)):.2f}**")

        with col4:
            st.write("**Bank Details:**")
            bank = bill_data.get('bank_details', {})
            if bank:
                st.write(f"Bank: {bank.get('bank_name', '')}")
                st.write(f"Branch: {bank.get('branch', '')}")
                st.write(f"A/C: {bank.get('account_no', '')}")
                st.write(f"IFSC: {bank.get('ifsc', '')}")

if option == "📤 Upload Inventory":
    # Container for upload section
    with st.container():
        st.markdown("""
            <h2 style='color: #1565C0; margin-bottom: 1rem;'>📤 Upload Inventory Bill</h2>
        """, unsafe_allow_html=True)
        
        # Create columns for better layout
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            uploaded_file = st.file_uploader(
                "Upload your bill image or PDF",
                type=["jpg", "jpeg", "png", "pdf"],
                help="Supported formats: JPG, JPEG, PNG, PDF"
            )
            
            if uploaded_file:
                files = {"file": uploaded_file.getvalue()}
                with st.spinner("Processing bill..."):
                    resp = requests.post(f"{API_URL}/inventory/upload", files=files)
                    if resp.ok:
                        st.success("✅ Bill processed and inventory updated!")
                        data = resp.json()
                        display_bill_details(data)
                    else:
                        st.error("❌ Failed to process bill. Please try again.")

elif option == "📋 View Inventory":
    # Container for inventory list
    with st.container():
        st.markdown("""
            <h2 style='color: #1565C0; margin-bottom: 1rem;'>📋 Current Inventory</h2>
        """, unsafe_allow_html=True)
        
        with st.spinner("Loading inventory..."):
            resp = requests.get(f"{API_URL}/inventory/view")
            if resp.ok:
                data = resp.json()
                inventory = data.get("inventory", [])
                if inventory:
                    for entry in inventory:
                        display_bill_details(entry)
                else:
                    st.info("🔍 No inventory records found. Upload some bills to get started!")
            else:
                st.error("❌ Failed to fetch inventory. Please try again later.")
