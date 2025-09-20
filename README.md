# 🚚 SABINA SUPPLIERS Transport Log

A real-world Streamlit app designed to solve a genuine business challenge — replacing pen-and-paper transport logs with a smart, searchable, and exportable digital system.

---

## 🧠 Why This App Exists

This project wasn’t born in a classroom or during a hackathon. It started when I visited my uncle’s friend, who runs a transport business in Hetauda, Nepal. I watched him manually record every truck, weight slip, and payment detail in a notebook — and then spend hours flipping through pages just to find one entry.

The problem wasn’t the data — it was the *lack of filtering, search, and export tools*. So I built this app for him.

---

## 🔐 Key Features

- *Login System*: Secure access with admin credentials
- *Data Entry*: Add transport logs with auto-calculated balances
- *Smart Filtering*: Search by vehicle, company, material, and date range
- *Inline Editing*: Update entries directly with live recalculations
- *PDF Export*: Branded reports for filtered, company, or full views
- *Monthly Backup*: Auto-backups with rolling 12-month retention
- *Deletion Controls*: Selective row deletion or full table reset

---

## 🛠 Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/sabina-suppliers.git
   cd sabina-suppliers

2. Install dependencies:
   pip install -r requirements.txt

3. Run the app:
   streamlit run code.py 

---

## Requirements 

See requirments.txt for full list.
Make sure wkhtmltopdf is installed for PDF export:
. Download here: https://wkhtmltopdf.org/downloads.html
. Default path: C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe

## 🔑 Access Instructions

To use the app, login with the following credentials:

- *Username*: admin
- *Password*: pass123

Once logged in, you’ll have full access to data entry, filtering, PDF export, and management tools.

---

## 🌐 Live App

Try it now:  
🔗 [SABINA SUPPLIERS Transport Log](https://transportlog-lvxvghpfjmaw8ve8yftvae.streamlit.app/)


## Data format 
The app reads and writes to data.csv. Monthly backups are stored in /backups

### Real Impact 

This app is now used by a local business to:
- Save hours of manual filtering 
- Generate clean pdf reports for clients 
- keep monthly backups without extra effort 

It's not just software -- it's a solution built from empathy, observation, and action.

#### Contact

Built with ❤ by Shubham Raj Sah
Drop a ⭐ if you found this helpful! `

Feel free to reach out for improvements, collaborations, or deployment help.

--- 