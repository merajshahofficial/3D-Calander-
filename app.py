import streamlit as st
import calendar
import datetime

st.set_page_config(page_title="3D Color Calendar", page_icon="📅")

st.title("🎨 3D & Multi-Color Calendar")
st.write(f"**Current Date & Time:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

col1, col2 = st.columns(2)
with col1:
    year = st.number_input("Select Year", min_value=1900, max_value=2100, value=datetime.datetime.now().year)
with col2:
    month = st.number_input("Select Month", min_value=1, max_value=12, value=datetime.datetime.now().month)

cal_data = calendar.monthcalendar(year, month)
month_name = calendar.month_name[month]

st.subheader(f"{month_name} {year}")

html_code = """
<style>
    .cal-table { width: 100%; text-align: center; border-collapse: collapse; font-family: sans-serif; }
    .cal-table th { background-color: #4CAF50; color: white; padding: 10px; border-radius: 5px; }
    .cal-table td { padding: 12px; font-weight: bold; border: 1px solid #ddd; }
    .weekend { color: #e74c3c; }
    .today { background-color: #f1c40f; color: black; box-shadow: 2px 2px 5px rgba(0,0,0,0.3); border-radius: 5px; }
</style>
<table class="cal-table">
<tr><th>Mo</th><th>Tu</th><th>We</th><th>Th</th><th>Fr</th><th class="weekend">Sa</th><th class="weekend">Su</th></tr>
"""

today = datetime.datetime.now()
for week in cal_data:
    html_code += "<tr>"
    for idx, day in enumerate(week):
        if day == 0:
            html_code += "<td></td>"
        else:
            is_today = (year == today.year and month == today.month and day == today.day)
            td_class = "today" if is_today else ("weekend" if idx >= 5 else "")
            html_code += f"<td class='{td_class}'>{day}</td>"
    html_code += "</tr>"
html_code += "</table>"

st.markdown(html_code, unsafe_allow_html=True)

