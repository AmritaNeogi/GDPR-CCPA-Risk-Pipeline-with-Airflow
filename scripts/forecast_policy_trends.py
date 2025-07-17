# scripts/forecast_policy_trends.py

import os
import pandas as pd
from prophet import Prophet
from datetime import datetime


def forecast_policy_trends(periods=7, freq='D'):
    """
    Read processed policy dates from cleaned_policies.csv, fit a Prophet model
    on daily counts, and produce a CSV with forecasts.

    Args:
        periods (int): how many future periods to forecast (default 7)
        freq (str): frequency string for Prophet (e.g. 'D' for daily)
    """
    # Paths
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    processed_path = os.path.join(base_dir, 'data', 'processed', 'cleaned_policies.csv')
    forecast_dir = os.path.join(base_dir, 'data', 'forecasts')
    os.makedirs(forecast_dir, exist_ok=True)

    # Load processed data
    df = pd.read_csv(processed_path)
    if df.empty:
        print("No processed policies to forecast.")
        return

    # Prepare time series: daily counts
    df['date'] = pd.to_datetime(df['date'], dayfirst=True, errors='coerce')
    counts = df.groupby('date').size().reset_index(name='y')
    counts.rename(columns={'date': 'ds'}, inplace=True)

    # Fit Prophet model
    m = Prophet()
    m.fit(counts)

    # Future dataframe
    future = m.make_future_dataframe(periods=periods, freq=freq)
    forecast = m.predict(future)

    # Select relevant cols
    out = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]

    # Write CSV
    ts = datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
    out_path = os.path.join(forecast_dir, f'forecast_{ts}.csv')
    out.to_csv(out_path, index=False)
    print(f"Wrote forecast to {out_path}")


if __name__ == '__main__':
    forecast_policy_trends()
