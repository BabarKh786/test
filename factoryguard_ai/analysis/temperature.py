import pandas as pd

def analyze_temperature_file(path, limit_min=None, limit_max=None):
    if path.lower().endswith((".xlsx",".xls")):
        df=pd.read_excel(path)
    elif path.lower().endswith(".csv"):
        df=pd.read_csv(path)
    else:
        raise ValueError("For spreadsheet analysis, upload XLSX or CSV.")
    df.columns=[str(c).strip() for c in df.columns]
    temp_col=next((c for c in df.columns if any(k in c.lower() for k in ["temp","temperature"])),None)
    if not temp_col:
        raise ValueError("Could not identify a temperature column. Include a column named Temperature or Temp.")
    values=pd.to_numeric(df[temp_col],errors="coerce")
    invalid=int(values.isna().sum())
    valid=df.loc[values.notna()].copy()
    valid["_temperature"]=values[values.notna()]
    deviations=[]
    if limit_min is not None or limit_max is not None:
        for idx,row in valid.iterrows():
            v=float(row["_temperature"])
            bad=(limit_min is not None and v<limit_min) or (limit_max is not None and v>limit_max)
            if bad:
                deviations.append({"row":int(idx)+2,"temperature":v})
    return {
        "records":int(len(df)),
        "valid_records":int(len(valid)),
        "invalid_records":invalid,
        "deviations":deviations,
        "columns":list(df.columns),
        "sample":df.head(10).fillna("").astype(str).to_dict("records")
    }
