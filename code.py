import streamlit as st
import pandas as pd
import os
from datetime import date
from datetime import datetime, timedelta
# from nepali_datetime import date as nep_date
# from nepali_datetime import datetime as nep_datetime
import shutil

from database import init_db
init_db()


import streamlit as st

# --- Login Credentials ---
VALID_USERNAME = "admin"
VALID_PASSWORD = "pass123"

# --- Session Setup ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# --- Login Form ---
if not st.session_state.authenticated:
    st.title("🔒 Login Required")

    with st.form("login_form"):
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
        login_btn = st.form_submit_button("🔓 Login")

        if login_btn:
            if username == VALID_USERNAME and password == VALID_PASSWORD:
                st.session_state.authenticated = True
                st.success("✅ Login successful!")
                st.rerun()  # 🔄 Refresh to hide login form
            else:
                st.error("❌ Invalid credentials")

if st.session_state.authenticated:
    
    #pdf export system
    import pdfkit

    def export_pdf(df, filename):
        # Create a folder directly on the desktop
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop", "pdf_exports")
        os.makedirs(desktop_path, exist_ok=True)

        # Full path for saving the PDF
        full_path = os.path.join(desktop_path, f"{filename}.pdf")

        # PDF configuration
        config = pdfkit.configuration(wkhtmltopdf=r"C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")

        # Convert DataFrame to HTML
        html_table = df.to_html(index=False, border=0, justify="center")

        # Styled HTML content with your official header
        html_content = f"""
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 20px;
                }}
                h1 {{
                    text-align: center;
                    font-size: 24px;
                    margin-bottom: 5px;
                }}
                h2 {{
                    text-align: center;
                    font-size: 18px;
                    margin-top: 0;
                    margin-bottom: 20px;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin-top: 10px;
                }}
                th, td {{
                    border: 1px solid #ccc;
                    padding: 6px;
                    text-align: center;
                    font-size: 12px;
                }}
                th {{
                    background-color: #f2f2f2;
                }}
            </style>
        </head>
        <body>
            <h1>SABINA SUPPLIERS</h1>
            <h2>HETAUDA -3, MAKWANPUR, NEPAL</h2>
            {html_table}
        </body>
        </html>
        """

        # Generate PDF
        pdfkit.from_string(html_content, full_path, configuration=config)
        return full_path

    # # --- Print Styling ---
    # st.markdown("""
    #     <style>
    #     @media print {
    #         button, .stButton, .stSidebar, .stForm {
    #             display: none !important;
    #         }

    #         @page {
    #             margin: 20mm;
    #         }

    #         body::after {
    #             content: "Page " counter(page);
    #             position: fixed;
    #             bottom: 10mm;
    #             left: 0;
    #             right: 0;
    #             text-align: center;
    #             font-size: 12px;
    #             color: #333;
    #         }
    #     }

    #     .print-header {
    #         text-align: center;
    #         font-size: 20px;
    #         font-weight: bold;
    #         margin-bottom: 20px;
    #     }
    #     </style>
    # """, unsafe_allow_html=True)

    # def print_button(label="🖨️ Print This Page"):
    #     st.markdown(f"""
    #         <button onclick="window.print()" style="margin-top:10px;">{label}</button>
    #     """, unsafe_allow_html=True)

    # def print_title():
    #     st.markdown("""
    #         <div style='text-align: center; line-height: 1.6; margin-bottom: 20px;'>
    #             <div style='font-size: 22px; font-weight: bold;'>SABINA SUPPLIERS</div>
    #             <div style='font-size: 18px;'>HETAUDA -3, MAKWANPUR, NEPAL</div>
    #             <hr style='border: 1px solid #000; margin-top: 10px; margin-bottom: 20px;' />    
    #         </div>
    #     """, unsafe_allow_html=True)
        
    st.set_page_config(page_title="Transport Log", layout="wide")
    st.markdown("version-1.3.2")

    st.title(" SABINA SUPPLIERS ")
    st.subheader("HETAUDA -3, MAKWANPUR, NEPAL")

    DATA_FILE = "data.csv"

    # Load or initialize data
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)

        # Drop unwanted columns if they exist
        df = df.drop(columns=["Fuel", "Payment", "Loading Date (BS)", "Unloading Date (BS)"], errors="ignore")

        # Parse dates
        df["Loading Date"] = pd.to_datetime(df["Loading Date"], errors='coerce')
        df["Unloading Date"] = pd.to_datetime(df["Unloading Date"], errors='coerce')

        # Save cleaned version back to CSV
        df.to_csv(DATA_FILE, index=False)

    else:
        df = pd.DataFrame(columns=[
            "Loading Date", "Transport Name", "Company Name", "Vehicle No", "Weight Slip",
            "Material", "Unloading Date", "Net Weight", "Rate", "Advance", "Remaining Balance"
        ])

    # Session state setup
    if "last_entry" not in st.session_state:
        st.session_state.last_entry = None
    if "manage_mode" not in st.session_state:
        st.session_state.manage_mode = False
    if "show_filters" not in st.session_state:
        st.session_state.show_filters = False

    # --- Data Entry Form ---
    st.subheader("📦 Add New Transport Entry")
    with st.form("entry_form"):
        col1, col2 = st.columns(2)
        with col1:
            loading_date = st.date_input("Loading Date", value=date.today())
            transport_name = st.text_input("Transport Name")
            company_name = st.text_input("Company Name")
            vehicle_no = st.text_input("Vehicle No")
            weight_slip = st.text_input("Weight Slip")
            Rate= st.number_input("Rate (Rs.)", min_value=0.0)
        with col2:
            material = st.text_input("Material")
            net_weight = st.number_input("Net Weight (kg)", min_value=0.0)
            Advance= st.number_input("Advance (Rs.)", min_value=0.0)
            Remaining_Balance = round((Rate * net_weight) - Advance, 2)
            st.write(f"💰 Remaining Balance: ₹{Remaining_Balance:,.2f}")
            unloading_date = st.date_input("Unloading Date", value=date.today())

        submitted = st.form_submit_button("Submit")

        if submitted:
            new_data = {
                "Loading Date": pd.to_datetime(loading_date),
                "Transport Name": transport_name.strip(),
                "Company Name": company_name.strip(),
                "Vehicle No": vehicle_no.strip(),
                "Weight Slip": weight_slip.strip(),
                "Rate": Rate,
                "Material": material.strip(),
                "Net Weight": net_weight,
                "Advance": Advance,
                "Remaining Balance": Remaining_Balance,
                "Unloading Date": pd.to_datetime(unloading_date)
            }

            new_entry_str = {
                "Loading Date": loading_date.strftime("%Y-%m-%d").strip().lower(),
                "Transport Name": transport_name.strip().lower(),
                "Company Name": company_name.strip().lower(),
                "Vehicle No": vehicle_no.strip().lower(),
                "Weight Slip": weight_slip.strip().lower(),
                "Rate": str(Rate).strip().lower(),
                "Material": material.strip().lower(),
                "Net Weight": str(net_weight).strip().lower(),
                "Advance": str(Advance).strip().lower(),
                "Remaining Balance": str(Remaining_Balance).strip().lower(),
                "Unloading Date": unloading_date.strftime("%Y-%m-%d").strip().lower()
            }

            if st.session_state.last_entry == new_entry_str:
                st.warning("⚠️ Duplicate submission detected. Data not saved.")
            else:
                df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
                df.to_csv(DATA_FILE, index=False)
                st.success("✅ Entry saved!")
                st.session_state.last_entry = new_entry_str

    # --- Filter & Manage Buttons Side by Side ---
    col_filter, col_manage = st.columns([1, 1])
    with col_filter:
        if st.button("Show Filters"):
            st.session_state.show_filters = not st.session_state.show_filters
    with col_manage:
        if st.button("Manage Entries"):
            st.session_state.manage_mode = not st.session_state.manage_mode

    # --- Filter Section ---
    if st.session_state.show_filters:
        with st.expander("Filter Options", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                search_vehicle = st.number_input("Vehicle No")
                search_transport = st.text_input("Transport Name")
                search_weight_slip = st.number_input("Weight Slip")
                search_company = st.text_input("Company Name")
            with col2:
                search_material = st.text_input("Material")
                start_date = st.date_input("Start Loading Date", value=date(2020, 1, 1))
                end_date = st.date_input("End Loading Date", value=date.today())

        filtered_df = df.copy()
        if search_vehicle:
            filtered_df = filtered_df[filtered_df["Vehicle No"] == search_vehicle]

        if search_company:
            filtered_df = filtered_df[filtered_df["Company Name"].fillna("").str.contains(search_company, case=False, na=False)]

        if search_weight_slip:
            filtered_df = filtered_df[filtered_df["Weight Slip"] == search_weight_slip]

        if search_transport:
            filtered_df = filtered_df[filtered_df["Transport Name"].fillna("").str.contains(search_transport, case=False, na=False)]

        if search_material:
            filtered_df = filtered_df[filtered_df["Material"].fillna("").str.contains(search_material, case=False, na=False)]
            
        if start_date != date(2020, 1, 1) or end_date != date.today():
            filtered_df["Loading Date"] = pd.to_datetime(filtered_df["Loading Date"], errors='coerce')
            filtered_df = filtered_df.dropna(subset=["Loading Date"])
            filtered_df = filtered_df[
                (filtered_df["Loading Date"] >= pd.to_datetime(start_date)) &
                (filtered_df["Loading Date"] <= pd.to_datetime(end_date))
            ]
    else:
        filtered_df = df.copy()

    # Format dates for display
    filtered_df = filtered_df.reset_index(drop=True)
    filtered_df["Loading Date"] = pd.to_datetime(filtered_df["Loading Date"], errors='coerce').dt.strftime("%Y-%m-%d")
    filtered_df["Unloading Date"] = pd.to_datetime(filtered_df["Unloading Date"], errors='coerce').dt.strftime("%Y-%m-%d")
    filtered_df["S.N."] = range(1, len(filtered_df) + 1)

    # --- Display Filtered Results ---
    if st.session_state.show_filters and (
        search_vehicle or search_transport or search_weight_slip or search_company or search_material or
        start_date != date(2020, 1, 1) or end_date != date.today()
    ):
        st.markdown("### 📋 Filtered Results")
        # print_title()
        # print_button("🖨️ Print Filtered Results")

        if not filtered_df.empty:
            display_columns = ["S.N.", "Loading Date", "Transport Name", "Company Name", "Vehicle No", "Weight Slip","Material", "Unloading Date", "Net Weight", "Rate", "Advance", "Remaining Balance"]
            st.dataframe(filtered_df[display_columns], use_container_width=True)
            st.write(f"🔢 Total Net Weight: {filtered_df['Net Weight'].sum():,.2f} kg")
            st.write(f"💸 Total Remaining Balance: ₹{filtered_df['Remaining Balance'].sum():,.2f}")
        else:
            st.info("No matching entries found.")

    if st.button("📄 Export Filtered Results for Transport", key="trigger_export_filtered"):
        st.session_state.show_pdf_input_filtered = True

    # --- Company PDF Export Trigger ---
    if st.button("📄 Export Filtered Results for Company", key="trigger_export_company"):
        st.session_state.show_pdf_input_company = True

    # --- Company PDF Filename Input & Export ---
    if st.session_state.get("show_pdf_input_company"):
        pdf_name_company = st.text_input("Enter PDF filename for Company", key="pdf_name_company")

        if st.button("✅ Confirm Export", key="confirm_export_company"):
            if pdf_name_company.strip():
                # Define company-facing columns
                company_columns = [
                    "S.N.", "Loading Date", "Company Name", "Vehicle No",
                    "Weight Slip", "Material", "Unloading Date", "Net Weight"
                ]

                # Prepare filtered data for company
                filtered_df_company = filtered_df.copy().reset_index(drop=True)
                filtered_df_company["S.N."] = range(1, len(filtered_df_company) + 1)

                for col in company_columns:
                    if col not in filtered_df_company.columns:
                        filtered_df_company[col] = ""

                filtered_df_company = filtered_df_company[company_columns]

                # Export to PDF
                path = export_pdf(filtered_df_company, pdf_name_company.strip())
                st.success(f"✅ Company PDF saved at: {path}")
                st.session_state.show_pdf_input_company = False
            else:
                st.warning("⚠️ Please enter a valid filename.")

    if st.session_state.get("show_pdf_input_filtered"):
        pdf_name_filtered = st.text_input("Enter PDF filename for Filtered Results", key="pdf_name_filtered")

        if st.button("✅ Confirm Export", key="confirm_export_filtered"):
            if pdf_name_filtered.strip():
                # Reorder filtered_df to place "Company Name" where you want it
                desired_order = [
                    "S.N.", "Loading Date", "Transport Name", "Company Name", "Vehicle No", "Weight Slip",
                    "Material", "Unloading Date", "Net Weight", "Rate", "Advance", "Remaining Balance"
                ]

                # Ensure all columns exist
                for col in desired_order:
                    if col not in filtered_df.columns:
                        filtered_df[col] = ""

                # Reorder the filtered DataFrame
                filtered_df = filtered_df[desired_order]
                path = export_pdf(filtered_df, pdf_name_filtered.strip())
                st.success(f"✅ PDF saved at: {path}")
                st.session_state.show_pdf_input_filtered = False
            else:
                st.warning("⚠️ Please enter a valid filename.")
        else:
            st.warning("⚠️ Please enter a valid filename.")

    # --- Ensure new columns exist ---
    for col in ["Company Name", "Rate", "Advance", "Remaining Balance"]:
        if col not in df.columns:
            df[col] = ""

    # --- Manage Entries Section ---
    if st.session_state.manage_mode:
        st.subheader("🛠️ Manage Entries")

        edited_rows = []
        delete_flags = []

        st.markdown("### ✏️ Edit entries directly below. Tick rows to delete.")

        # Header row
        header_cols = st.columns([0.6, 0.6, 1.1, 1.1, 1.1, 1.1, 1.1, 1.1, 1.1, 1.1, 1.1, 1.1, 1.1])
        headers = ["Delete", "Index", "Loading Date", "Transport Name", "Company Name", "Vehicle No", "Weight Slip", "Material", "Unloading Date", "Net Weight", "Rate (Rs)", "Advance (Rs)", "Remaining Balance (Rs)"]
        for col, label in zip(header_cols, headers):
            col.markdown(f"**{label}**")

        with st.form("manage_form"):
            for i, row in df.iterrows():
                # Handle NaT safely
                ld_raw = pd.to_datetime(row["Loading Date"], errors='coerce')
                ud_raw = pd.to_datetime(row["Unloading Date"], errors='coerce')
                ld_safe = ld_raw if not pd.isna(ld_raw) else date.today()
                ud_safe = ud_raw if not pd.isna(ud_raw) else date.today()

                # Alternate background color
                bg_color = "#f9f9f9" if i % 2 == 0 else "#e6f2ff"
                st.markdown(f"""<div style="background-color:{bg_color}; padding:10px; border-radius:6px; margin-bottom:6px;">""", unsafe_allow_html=True)

                cols = st.columns([0.6, 0.6, 1.1, 1.1, 1.1, 1.1, 1.1, 1.1, 1.1, 1.1, 1.1, 1.1, 1.1])

                with cols[0]:
                    delete = st.checkbox("", key=f"delete_{i}")

                with cols[1]:
                    st.write(f"**{i}**")

                with cols[2]:
                    loading_date = st.date_input("", value=ld_safe, key=f"ld_{i}")

                with cols[3]:
                    transport_name = st.text_input("", value=row["Transport Name"], key=f"tn_{i}")

                with cols[4]:
                    company_name = st.text_input("", value=row.get("Company Name", ""), key=f"comp_{i}")
    
                with cols[5]:
                    vehicle_no = st.text_input("", value=row["Vehicle No"], key=f"vn_{i}")

                with cols[6]:
                    weight_slip = st.text_input("", value=row["Weight Slip"], key=f"ws_{i}")

                with cols[7]:
                    material = st.text_input("", value=row["Material"], key=f"mat_{i}")

                with cols[8]:
                    unloading_date = st.date_input("", value=ud_safe, key=f"ud_{i}")

                with cols[9]:
                    net_weight = st.number_input("", value=float(row["Net Weight"]), min_value=0.0, key=f"nw_{i}")

                with cols[10]:
                    rate = st.number_input("", value=float(row["Rate"]) if str(row["Rate"]).replace('.', '', 1).isdigit() else 0.0, min_value=0.0, key=f"rate_{i}")

                with cols[11]:
                    advance = st.number_input("", value=float(row["Advance"]) if str(row["Advance"]).replace('.', '', 1).isdigit() else 0.0, min_value=0.0, key=f"adv_{i}")

                with cols[12]:
                    # Recalculate using live inputs
                    remaining_balance = round((rate * net_weight) - advance, 2)
                    st.write(f"₹{remaining_balance:,.2f}")

                st.markdown("</div>", unsafe_allow_html=True)

                edited_rows.append({
                    "index": i,
                    "Loading Date": pd.to_datetime(loading_date),
                    "Transport Name": transport_name.strip(),
                    "Company Name": company_name.strip(),
                    "Vehicle No": vehicle_no.strip(),
                    "Weight Slip": weight_slip.strip(),
                    "Material": material.strip(),
                    "Unloading Date": pd.to_datetime(unloading_date),
                    "Net Weight": net_weight,
                    "Rate": rate,
                    "Advance": advance,
                    "Remaining Balance": remaining_balance  # ✅ Now stored in CSV
                })
                delete_flags.append((i, delete))

            col_save, col_delete = st.columns([1, 1])
            with col_save:
                save_all = st.form_submit_button("💾 Save All Changes")
            with col_delete:
                delete_selected = st.form_submit_button("🗑️ Delete Selected")

        # --- Apply Edits ---
        if save_all:
            for row in edited_rows:
                i = row["index"]
                for key in row:
                    if key != "index":
                        df.at[i, key] = row[key]
            df.to_csv("data.csv", index=False)
            st.success("✅ All changes saved!")
            st.rerun()


        # --- Apply Deletions ---
        if delete_selected:
            indices_to_delete = [i for i, flag in delete_flags if flag]
            df = df.drop(index=indices_to_delete).reset_index(drop=True)
            df.to_csv("data.csv", index=False)
            st.success("🗑️ Selected entries deleted!")
            st.rerun()


    # --- Monthly Backup System ---
    backup_folder = "backups"
    os.makedirs(backup_folder, exist_ok=True)

    # Create or update this month's backup
    month_stamp = datetime.now().strftime("%Y_%m")
    monthly_backup = os.path.join(backup_folder, f"backup_{month_stamp}.csv")
    # Reorder columns for backup
    desired_order = [
        "S.N.", "Loading Date", "Transport Name", "Company Name", "Vehicle No",
        "Weight Slip", "Material", "Unloading Date", "Net Weight", "Rate",
        "Advance", "Remaining Balance"
    ]

    # Ensure all columns exist
    for col in desired_order:
        if col not in df.columns:
            df[col] = ""

    # Reorder the DataFrame
    df = df[desired_order]
    df.to_csv(monthly_backup, index=False)

    # Delete backup from exactly 365 days ago
    target_date = datetime.now() - timedelta(days=365)
    target_stamp = target_date.strftime("%Y_%m")
    target_file = os.path.join(backup_folder, f"backup_{target_stamp}.csv")

    if os.path.exists(target_file):
        try:
            os.remove(target_file)
            st.info(f"🗑️ Deleted backup from {target_stamp}")
        except Exception as e:
            st.warning(f"⚠️ Failed to delete old backup: {target_stamp} — {e}")

    # --- Display All Entries Table ---
    st.subheader("📋 All Entries")
    # print_title()
    # print_button("🖨️ Print All Entries")

    df_display = df.copy()
    df_display = df_display.reset_index(drop=True)
    df_display["S.N."] = range(1, len(df_display) + 1)
    df_display["Loading Date"] = pd.to_datetime(df_display["Loading Date"], errors='coerce').dt.strftime("%Y-%m-%d")
    df_display["Unloading Date"] = pd.to_datetime(df_display["Unloading Date"], errors='coerce').dt.strftime("%Y-%m-%d")

    display_columns = [
        "S.N.", "Loading Date", "Transport Name", "Company Name", "Vehicle No", "Weight Slip",
        "Material", "Unloading Date", "Net Weight", "Rate", "Advance", "Remaining Balance"
    ]

    st.dataframe(df_display[display_columns], use_container_width=True)
    st.write(f"🔢 Total Net Weight: {df_display['Net Weight'].sum():,.2f} kg")
    st.write(f"💸 Total Remaining Balance: ₹{df_display['Remaining Balance'].sum():,.2f}")


    # --- PDF Export Trigger ---
    if st.button("📄 Export All Entries to PDF", key="trigger_export_all"):
        st.session_state.show_pdf_input_all = True

    # --- PDF Filename Input & Export ---
    if st.session_state.get("show_pdf_input_all"):
        pdf_name_all = st.text_input("Enter PDF filename for All Entries (without .pdf)", key="pdf_name_all")

        if st.button("✅ Confirm Export", key="confirm_export_all"):
            if pdf_name_all.strip():
                # Reorder df_display to match desired column order
                desired_order = [
                    "S.N.", "Loading Date", "Transport Name", "Company Name", "Vehicle No", "Weight Slip",
                    "Material", "Unloading Date", "Net Weight", "Rate", "Advance", "Remaining Balance"
                ]

                for col in desired_order:
                    if col not in df_display.columns:
                        df_display[col] = ""

                df_display = df_display[desired_order]
                path = export_pdf(df_display, pdf_name_all.strip())
                st.success(f"✅ PDF saved at: {path}")
                st.session_state.show_pdf_input_all = False  # Reset after export
            else:
                st.warning("⚠️ Please enter a valid filename.")


    # --- Clear All Entries Confirmation Flow ---
    if "confirm_clear" not in st.session_state:
        st.session_state.confirm_clear = False

    if not st.session_state.confirm_clear:
        if st.button("🧹 Clear All Entries"):
            st.session_state.confirm_clear = True
            st.rerun()
    else:
        st.warning("⚠️ Are you sure you want to delete all entries? This action cannot be undone.")
        col_yes, col_no = st.columns([1, 1])
        with col_yes:
            if st.button("✅ Yes, clear all"):
                df = pd.DataFrame(columns=df.columns)
                df.to_csv("data.csv", index=False)
                st.success("✅ Table cleared. Fresh start!")
                st.session_state.confirm_clear = False
                st.rerun()
        with col_no:
            if st.button("❌ Cancel"):
                st.session_state.confirm_clear = False
                st.info("🛑 Clear action cancelled.")
                st.rerun()            