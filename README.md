# 📦 SmartShift Planner

SmartShift Planner is a lightweight workforce scheduling and forecasting tool designed for warehouses, call centers, and service operations. Built using Streamlit and Python, it helps managers create optimized weekly schedules, check compliance with labor laws, and forecast staffing needs based on expected workload.

## 🚀 Features

- ✅ **Automatic Shift Scheduling** (Morning/Evening) based on roles, hours, and preferences
- ✅ **Labor Law Compliance Checks** for German regulations:
  - Max 48 hours/week
  - Max 10 hours/day
  - Minimum 11 hours rest between shifts
- ✅ **Training/Coaching Slot Scheduling** for employees flagged as needing retraining
- 📊 **Staffing Visualization** by day and station (role)
- 🔮 **Forecasted Workload Input** to predict required staffing per day
- 📥 **Downloadable Schedule Output** (CSV)

## 📊 Preview

![Schedule preview](https://via.placeholder.com/800x300.png?text=Schedule+Dashboard)
> Visual comparison of required vs. scheduled workers

## 🧱 Tech Stack

- [Streamlit](https://streamlit.io/) – for the web UI
- [Pandas](https://pandas.pydata.org/) – for schedule logic & data handling
- [Altair](https://altair-viz.github.io/) – for interactive charts
- Python modules: `openpyxl`, `random`, `datetime`

## 📂 Project Structure
smartshift-planner/ ├── app.py # Streamlit UI ├── scheduler.py # Schedule logic ├── utils.py # Labor law checks ├── requirements.txt # Pip dependencies └── warehouse_employees.xlsx # Sample input

pgsql
Kopieren
Bearbeiten

## 🧠 How to Use

1. Upload an Excel or CSV file with employee data
2. Adjust expected workload in the sidebar
3. Click “Generate Schedule”
4. View compliance, training, role breakdown, and forecast analysis
5. Download the schedule for deployment

## 📦 Example Employee File

| agent_id | name  | max_hours_per_week | preferred_shift | skills           | role     | training_required | contract_type |
|----------|-------|--------------------|------------------|------------------|----------|-------------------|----------------|
| W1       | Lukas | 40                 | Morning          | Picking,Packing  | Picking  | No                | Full-time      |

## 📈 Future Improvements

- Add peak season night shifts
- Smarter shift balancing by target role coverage
- Role-specific productivity rates
- Historical data tracking for ML-based forecasting

## 👤 Author

Built by [Your Name] – a data-minded operations enthusiast who blends logistics, software, and strategy to create practical tools that deliver.

---

## 💡 Want to try it live?

> Deploy to Streamlit Cloud and share the link with team leads, recruiters, or hiring managers.

