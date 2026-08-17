import api
import pandas as pd
import numpy as np
import calendar
from datetime import datetime

def make_df(type, start, end):

    if type == 1:
        flr_df = pd.DataFrame(api.get_flr(start, end))

        if not flr_df.empty:
            flr_df["date"] = flr_df["beginTime"].str[:10]

        return flr_df

    if type == 2:
        cme_df = pd.DataFrame(api.get_cme(start, end))

        if not cme_df.empty:
            cme_df["speed"] = cme_df["cmeAnalyses"].apply(
                lambda x: x[0]["speed"]
            )
            cme_df["date"] = cme_df["startTime"].str[:10]

        return cme_df

    if type == 3:
        gst_df = pd.DataFrame(api.get_gst(start, end))

        if not gst_df.empty:
            gst_df["kpIndex"] = gst_df["allKpIndex"].apply(
                lambda x: x[0]["kpIndex"]
            )
            gst_df["date"] = gst_df["startTime"].str[:10]

        return gst_df

def clean_df(df):
    df.drop(columns=["flrID",
    "activityID",
    "gstID",
    "catalog",
    "instruments",
    "activeRegionNum",
    "note",
    "submissionTime",
    "versionId",
    "link",
    "sentNotifications"], 
    inplace = True, errors = "ignore")

    return df

def highflr(df):
    if not df.empty:
        return df.sort_values("classType").iloc[-1]

def highspeed(df):
    if not df.empty:
        return df["speed"].max()

def highkp(df):
    if not df.empty:
        return df["kpIndex"].max()

def riskanalysis(flr, cme, gst):
    if not flr.empty:
        details = [highflr(flr)["classType"], highspeed(cme), highkp(gst)]
    else:
        details = [None, highspeed(cme), highkp(gst)]
    impact = 0
    flrnum = len(flr)
    cmenum = len(cme)
    gstnum = len(gst)

    if not flr.empty:
        flareclass = highflr(flr)["classType"][0]
    else:
        flareclass = None

    maxkp = highkp(gst)

    if flareclass in ['A', 'B', None]:
        details.append("Minimal")

    elif flareclass == 'C' or (flareclass == 'M' and int(highflr(flr)["classType"][1]) < 5):
        details.append("Low")
        impact += 1

    elif flareclass == "M":
        details.append("Moderate")
        impact += 2

    elif flareclass == "X":
        details.append("High")
        impact += 3

    if maxkp is None or maxkp <= 4:
        details.append("Minimal")

    elif maxkp<=5:
        details.append("Minor")

    elif maxkp<=6:
        details.append("Moderate")
        impact += 1

    elif maxkp<=7:
        details.append("Strong")
        impact += 2

    else:
        details.append("Extreme")
        impact += 3

    if "Extreme" in details or "Strong" in details or "High" in details:
        impactstr = "High"
    elif "Moderate" in details:
        impactstr = "Moderate"
    elif "Minor" in details or "Low" in details:
        impactstr = "Low"
    else:
        impactstr = "Minimal"

    details.append(impactstr)
    details.append(flrnum)
    details.append(cmenum)
    details.append(gstnum)
    return details


from datetime import datetime
import calendar


def monthly_event_counts(selected_date):

    selected_date = datetime.fromisoformat(selected_date)

    year = selected_date.year
    month = selected_date.month

    num_days = calendar.monthrange(year, month)[1]

    start = f"{year}-{month:02d}-01"
    end = f"{year}-{month:02d}-{num_days:02d}"

    # Only 3 API calls
    flr = make_df(1, start, end)
    cme = make_df(2, start, end)
    gst = make_df(3, start, end)

    days = list(range(1, num_days + 1))

    flare_counts = []
    cme_counts = []
    gst_counts = []

    for day in days:

        current_date = f"{year}-{month:02d}-{day:02d}"

        flare_counts.append(
            len(flr[flr["date"] == current_date])
            if not flr.empty else 0
        )

        cme_counts.append(
            len(cme[cme["date"] == current_date])
            if not cme.empty else 0
        )

        gst_counts.append(
            len(gst[gst["date"] == current_date])
            if not gst.empty else 0
        )

    return days, flare_counts, cme_counts, gst_counts