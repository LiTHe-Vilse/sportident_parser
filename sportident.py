import pandas as pd
import math
df=pd.read_csv("control_146302.csv", delimiter=";", parse_dates=["Control time"])

df_si_number=pd.read_csv("Sportidentnummer (22).csv", delimiter=";", 
names=["SIID", "name", "club"])
times = {}

ssid = df["SIID"].unique()
for id in ssid:
    df_2 = df[df["SIID"] == id]
    df_2 = df_2.reset_index()
    if len(df_2) >1:
        time1 = df_2.iloc[0]["Control time"]
        time2 = df_2.iloc[1]["Control time"]
        diff = (time2 - time1).total_seconds()
        seconds = round(diff % 60, ndigits=3)
        minutes = (int)(diff)//60
        millis = seconds - math.floor(seconds)
        times[id] = (minutes, seconds, millis * 1000)
    else:
        x = df_2["SIID"].iloc[0]
        print(f"{x} found once")

rows = []
for key, time in times.items():
    row = df_si_number[df_si_number["SIID"] == key]
    if row.size > 0:
        name = row.iloc[0]["name"].strip()
        club = row.iloc[0]["club"]
        rows.append([name, club, f"{time[0]}:{int(time[1]):02d}.{int(time[2]):03d}"])
    else:
        print(f"SI: {key} not found")

new_df = pd.DataFrame(rows, columns=["name", "club", "time"])
new_df = new_df.sort_values("time")

new_df.to_csv("out.csv", index=None, encoding="utf-8-sig", sep=";")