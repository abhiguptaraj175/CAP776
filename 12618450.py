import pandas as pd
import numpy as np

EXCEL_FILE = "12618450.xlsx"
SHEET_NAME = "Daily Log"
START_DATE = pd.Timestamp("2026-08-13")

raw = pd.read_excel(
    EXCEL_FILE,
    sheet_name=SHEET_NAME,
    header=None
)

headers = raw.iloc[4].tolist()
data = raw.iloc[5:].copy()
data.columns = headers

data["Date"] = pd.to_datetime(
    data["Date"],
    errors="coerce"
)

data = data[data["Date"].notna()].copy()

numeric_columns = [
    "Sleep (min)",
    "Fitness (min)",
    "Study (min)",
    "Coding (min)",
    "Class (min)",
    "Classes Attended",
    "Other Activities (min)",
    "Total Tracked (min)",
    "Free/Unaccounted (min)"
]

for column in numeric_columns:
    data[column] = pd.to_numeric(
        data[column],
        errors="coerce"
    )

feeling_scores = {
    "Excellent": 5,
    "Good": 4,
    "Neutral": 3,
    "Low": 2,
    "Stressed": 1
}

satisfaction_scores = {
    "Very Satisfied": 5,
    "Satisfied": 4,
    "Neutral": 3,
    "Unsatisfied": 2,
    "Very Unsatisfied": 1
}

energy_scores = {
    "High": 3,
    "Medium": 2,
    "Low": 1
}

data["Feeling Score"] = data["Day's Feeling"].map(feeling_scores)
data["Satisfaction Score"] = data["Satisfaction Level"].map(
    satisfaction_scores
)
data["Energy Score"] = data["Energy Level"].map(energy_scores)

required_columns = [
    "Sleep (min)",
    "Fitness (min)",
    "Study (min)",
    "Coding (min)",
    "Class (min)",
    "Total Tracked (min)",
    "Free/Unaccounted (min)",
    "Feeling Score",
    "Satisfaction Score",
    "Energy Score"
]

valid_mask = data[required_columns].notna().all(axis=1)

valid_data = data[valid_mask].copy()
invalid_data = data[~valid_mask].copy()

END_DATE = valid_data["Date"].max()

expected_dates = pd.date_range(
    start=START_DATE,
    end=END_DATE,
    freq="D"
)

expected_days = len(expected_dates)

recorded_dates = set(
    valid_data["Date"].dt.normalize()
)

missing_dates = [
    date
    for date in expected_dates
    if date not in recorded_dates
]

missing_days = len(missing_dates)

average_sleep = valid_data["Sleep (min)"].mean()
average_fitness = valid_data["Fitness (min)"].mean()
average_study = valid_data["Study (min)"].mean()
average_coding = valid_data["Coding (min)"].mean()
average_class = valid_data["Class (min)"].mean()
average_other = valid_data["Other Activities (min)"].mean()
average_free = valid_data["Free/Unaccounted (min)"].mean()

TPI = valid_data["Coding (min)"].mean()

AAI = (
    valid_data["Study (min)"] +
    valid_data["Class (min)"]
).mean()

PhAI = valid_data["Fitness (min)"].mean()

SRI = valid_data["Sleep (min)"].mean()

ABI = valid_data["Free/Unaccounted (min)"].mean()

TUI = valid_data["Total Tracked (min)"].mean()

valid_data["Daily EI"] = (
    valid_data["Feeling Score"] +
    valid_data["Satisfaction Score"] +
    valid_data["Energy Score"]
) / 3

EI = valid_data["Daily EI"].mean()

valid_recorded_days = len(valid_data)

DCI = (
    valid_recorded_days /
    expected_days
) * 100

PAI = (
    0.15 * TPI +
    0.20 * AAI +
    0.15 * PhAI +
    0.20 * SRI +
    0.15 * TUI +
    0.10 * EI +
    0.05 * DCI
)

print("=" * 65)
print("       CAP776 - MY DATA, MY STORY")
print("       PERSONAL ACTIVITY INTELLIGENCE REPORT")
print("=" * 65)

print("\nACTIVITY DATA SUMMARY")
print("-" * 65)

print(f"Start Date                 : {START_DATE.strftime('%d-%b-%Y')}")
print(f"Last Recorded Date         : {END_DATE.strftime('%d-%b-%Y')}")
print(f"Expected Number of Days    : {expected_days}")
print(f"Valid Recorded Days        : {valid_recorded_days}")
print(f"Missing Days               : {missing_days}")
print(f"Invalid / Excluded Records : {len(invalid_data)}")

print(f"\nAverage Sleep/day          : {average_sleep:.2f} min")
print(f"Average Fitness/day        : {average_fitness:.2f} min")
print(f"Average Study/day          : {average_study:.2f} min")
print(f"Average Coding/day         : {average_coding:.2f} min")
print(f"Average Class/day          : {average_class:.2f} min")
print(f"Average Other Activities   : {average_other:.2f} min")
print(f"Average Free/Unaccounted   : {average_free:.2f} min")

print("\n")
print("INDEX VALUES")
print("-" * 65)

print(f"TPI  - Tech Productivity   : {TPI:.2f} min/day")
print(f"AAI  - Academic Activity   : {AAI:.2f} min/day")
print(f"PhAI - Physical Activity   : {PhAI:.2f} min/day")
print(f"SRI  - Sleep & Recovery    : {SRI:.2f} min/day")
print(f"ABI  - Activity Balance    : {ABI:.2f} min/day")
print(f"TUI  - Time Utilization    : {TUI:.2f} min/day")
print(f"EI   - Experience Index    : {EI:.2f} / 5")
print(f"DCI  - Data Continuity     : {DCI:.2f} %")
print(f"PAI  - Personal Activity   : {PAI:.2f}")

print("\n")
print("MISSING DATES")
print("-" * 65)

if missing_dates:
    for date in missing_dates:
        print(date.strftime("%d-%b-%Y"))
else:
    print("No missing dates.")

print("\n")
print("=" * 65)
print("Calculation completed successfully.")
print("=" * 65)