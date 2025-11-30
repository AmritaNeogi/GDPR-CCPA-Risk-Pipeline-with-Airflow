# scripts/forecast_policy_trends.py

import os
import pandas as pd
from prophet import Prophet
from datetime import datetime


def forecast_policy_trends(periods=7, freq='D'):
    """
    Fit a Prophet model on daily policy counts and write a forecast CSV.
    """

    # Build absolute paths
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    processed_path = os.path.join(
        base_dir, 'data', 'processed', 'cleaned_with_topic_and_severity.csv'
    )
    forecast_dir = os.path.join(base_dir, 'data', 'forecasts')
    os.makedirs(forecast_dir, exist_ok=True)

    # Load processed data
    df = pd.read_csv(processed_path)
    if df.empty:
        print("No processed policies to forecast.")
        return

    # Convert dates
    df['date'] = pd.to_datetime(df['date'], errors='coerce')

    # Group counts per day
    counts = df.groupby('date').size().reset_index(name='y')
    counts.rename(columns={'date': 'ds'}, inplace=True)

    # Fit Prophet
    m = Prophet()
    m.fit(counts)

    # Build future frame
    future = m.make_future_dataframe(periods=periods, freq=freq)
    forecast = m.predict(future)

    # Keep relevant columns
    out = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]

    # Save CSV
    ts = datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
    out_path = os.path.join(forecast_dir, f'forecast_{ts}.csv')
    out.to_csv(out_path, index=False)

    print(f"✅ Wrote forecast to: {out_path}")


if __name__ == '__main__':
    forecast_policy_trends()
