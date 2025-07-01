import datetime as dt
import logging
import warnings
from warnings import filterwarnings

import yfinance as yf
import pandas as pd
import numpy as np
from darts import TimeSeries
from darts.dataprocessing.transformers import MissingValuesFiller
from darts.models import (
    ExponentialSmoothing, Prophet, AutoARIMA, Theta, ARIMA,
    FFT, FourTheta, NaiveDrift, NaiveMean, NaiveSeasonal
)
from darts.metrics import mape


def oracle(portfolio, start_date, weights=None, prediction_days=None, based_on='Adj Close'):
    print("Collecting data...")

    if weights is None:
        weights = [1.0 / len(portfolio)] * len(portfolio)

    today = dt.datetime.today().strftime('%Y-%m-%d')

    # Suppress warnings
    logger = logging.getLogger()
    warnings.simplefilter(action='ignore', category=FutureWarning)
    filterwarnings('ignore')
    logging.disable(logging.INFO)

    mape_df = pd.DataFrame(columns=[
        'Exponential smoothing', 'Prophet', 'Auto-ARIMA', 'Theta(2)', 'ARIMA',
        'FFT', 'FourTheta', 'NaiveDrift', 'NaiveMean', 'NaiveSeasonal'
    ])
    final_df = pd.DataFrame(columns=mape_df.columns)

    for asset in portfolio:
        print(f"\nProcessing asset: {asset}")

        # Download data
        df = yf.download(asset, start=start_date, end=today, progress=False)

        # Handle MultiIndex columns by flattening
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = ['_'.join(col).strip() if isinstance(col, tuple) else col for col in df.columns.values]

        # Determine price column name
        price_col = f"{based_on}_{asset}" if any(col.endswith(f"_{asset}") for col in df.columns) else based_on

        # Fallback logic for missing columns
        if price_col not in df.columns:
            if based_on == 'Adj Close':
                fallback_col = f"Close_{asset}" if any(col.endswith(f"_{asset}") for col in df.columns) else "Close"
                if fallback_col in df.columns:
                    print(f"'{based_on}' not found for {asset}. Falling back to '{fallback_col}'.")
                    price_col = fallback_col
                else:
                    print(f"Error: Neither '{based_on}' nor 'Close' found for {asset}. Skipping.")
                    continue
            else:
                print(f"Error: Column '{based_on}' not found for {asset}. Skipping.")
                continue

        # Prepare DataFrame for darts
        df_asset = df[[price_col]].copy()
        df_asset = df_asset.rename(columns={price_col: 'value'})
        df_asset.index.name = 'Date'
        df_asset = df_asset.reset_index()
        df_asset = df_asset.rename(columns={'Date': 'time'})

        if 'time' not in df_asset.columns:
            print(f"Date column not found for {asset}. Skipping.")
            continue

        # Determine prediction_days if None
        if prediction_days is None:
            x = 1
            while x / (len(df_asset) + x) < 0.3:
                x += 1
            prediction_days = x

        def eval_model(model):
            model.fit(train)
            forecast = model.predict(len(val))
            result[model] = [mape(val, forecast)]

        prediction = pd.DataFrame()

        def predict(model):
            model.fit(train)
            _ = model.predict(len(val))
            pred = model.predict(prediction_days)
            pred_val = pred[-1].values()
            pred_val = pred_val.item() if hasattr(pred_val, 'item') else pred_val
            pct_change = round(((pred_val - start_value) / start_value) * 100, 3)
            prediction[model] = [f"{pct_change} %"]

        try:
            series = TimeSeries.from_dataframe(df_asset, time_col='time', value_cols='value', freq='D')
        except Exception as e:
            print(f"Could not create time series for {asset}: {e}")
            continue

        series = MissingValuesFiller().transform(series)

        train_index = round(len(df_asset) * 0.7)
        train_date = df_asset.loc[train_index, 'time']
        timestamp = pd.Timestamp(train_date)

        try:
            train, val = series.split_before(timestamp)
        except Exception as e:
            print(f"Split failed for {asset}: {e}")
            continue

        print(f"Evaluating the models for {asset}...")
        result = pd.DataFrame()
        try:
            eval_model(ExponentialSmoothing())
            eval_model(Prophet())
            eval_model(AutoARIMA())
            eval_model(Theta())
            eval_model(ARIMA())
            eval_model(FFT())
            eval_model(FourTheta())
            eval_model(NaiveDrift())
            eval_model(NaiveMean())
            eval_model(NaiveSeasonal())
        except Exception as e:
            print(f"Model evaluation error for {asset}: {e}")
            continue
        print("Models evaluated!")

        result.columns = mape_df.columns
        result.index = [asset]
        mape_df = pd.concat([mape_df, result])

        start_value = df_asset['value'].iloc[-1]

        # split train/val again for prediction on latest data
        try:
            train, val = series.split_before(df_asset['time'].iloc[-1])
        except Exception:
            val = series[-prediction_days:]
            train = series[:-prediction_days]

        print(f"Making the predictions for {asset}...")
        try:
            predict(ExponentialSmoothing())
            predict(Prophet())
            predict(AutoARIMA())
            predict(Theta())
            predict(ARIMA())
            predict(FFT())
            predict(FourTheta())
            predict(NaiveDrift())
            predict(NaiveMean())
            predict(NaiveSeasonal())
        except Exception as e:
            print(f"Prediction error for {asset}: {e}")
            continue
        print("Predictions generated!")

        prediction.columns = mape_df.columns
        prediction.index = [asset]
        final_df = pd.concat([final_df, prediction])

    print("\nAssets MAPE (accuracy score):")
    print(mape_df)

    print(f"\nAssets returns prediction for the next {prediction_days} days:")
    print(final_df)

    # Portfolio aggregation
    portfolio_pred = pd.DataFrame()
    for column in final_df.columns:
        weighted_returns = []
        for index in final_df.index:
            try:
                percent = float(final_df[column][index].replace('%', '').strip())
                wts = weights[portfolio.index(index)]
                weighted_returns.append(percent * wts)
            except Exception as e:
                print(f"Error processing {index} for model {column}: {e}")
                continue
        portfolio_pred[column] = [sum(weighted_returns)]

    print(f"\nPortfolio returns prediction for the next {prediction_days} days:")
    print(portfolio_pred.iloc[0])

    logger.disabled = False
    return portfolio_pred
