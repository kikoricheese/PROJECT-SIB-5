# -*- coding: utf-8 -*-
"""pemodelan Time Series (LSTM)_optiminds.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1r23PXN2nYbzr3sv03RbC9EhgaOxrD6Jw

# Optimisasi Kebijakan Tenaga Kerja Melalui Prediksi Time Series Tingkat Pengangguran dan Peluang Kerja di Jawa Barat

## Business Undesrtanding

Salah satu provonsi di Indonesia yaitu Jawa Barat menghadapi tantangan kompleks dalam mengelola angka pengangguran dan peluang kerja.  Pendekatan yang canggih diperlukan untuk memahami dan memprediksi tren di pasar tenaga kerja. Dengan membuat model prediksi time series untuk tingkat pengangguran dan peluang kerja di Jawa Barat mampu memberikan dasar yang kuat untuk perencanaan kebijakan yang efisien dan disesuaikan dengan dinamika pasar tenaga kerja di Jawa Barat.

**Goal** : Predictive Tingkat Pengangguran untuk Peluang Kerja 1 Tahun Kedepan

**Case problem** : Time Series

**Jenis Machine Learning** = Supervised Learning

**Algoritma** :
* Moving average
* Exponential smoothing
* SARIMAX
* ARIMA
* LSTM
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
from sklearn.metrics import mean_absolute_error, mean_squared_error
from google.colab import drive
drive.mount('/content/drive')

"""### DATA PENGANGGURAN"""

path='/content/drive/MyDrive/DataProject/persentase_tingkat_pengangguran.csv'
load_data=pd.read_csv(path)
load_data.head()

df=pd.DataFrame(load_data)
df

df_filtered = df.loc[(df['tahun'] < 2007) | (df['tahun'] > 2015)]
df_filtered

df_mean = df_filtered.groupby('tahun')['persentase_tingkat_pengangguran_terbuka'].mean().reset_index()
df_mean.columns = ['tahun', 'mean_tingkat_pengangguran']
df_mean

"""### DATA JUMLAH LOWONGAN PEKERJAAN"""

path1='/content/drive/MyDrive/DataProject/jumlah_lowongan_kerja.csv'
load_data1=pd.read_csv(path1)
load_data1.head()

df1=pd.DataFrame(load_data1)
df1

df1_lowongan = df1.groupby('tahun')['jumlah_lowongan_kerja'].sum().reset_index()
df1_lowongan.columns = ['tahun', 'total_jumlah_lowongan_kerja']
df1_lowongan

"""### DATA JUMLAH PENDUDUK BERDASARKAN JENIS KELAMIN"""

path2='/content/drive/MyDrive/DataProject/jumlah_penduduk_yang_bekerja_berdasarkan_jenis_kelamin.csv'
load_data2=pd.read_csv(path2)
load_data2.head()

df2=pd.DataFrame(load_data2)
df2

df2_jml_penduduk = df2.groupby('tahun')['jumlah_penduduk'].sum().reset_index()
df2_jml_penduduk.columns = ['tahun', 'total_jumlah_penduduk']
df2_jml_penduduk

"""### DATA GABUNGAN"""

data = df_mean.merge(df1_lowongan, on='tahun').merge(df2_jml_penduduk, on='tahun')
data

# data.to_excel('/content/drive/MyDrive/DataProject/data_before_2018-2022.xlsx', index=False)

"""## Data Understanding"""

path3='/content/drive/MyDrive/DataProject/data_before_2018-2022.xlsx'
load_data3=pd.read_excel(path3)
load_data3

df3=pd.DataFrame(load_data3)
df3

df3.info()

df3.isnull().sum()

"""## Data Preparation"""

tahun = [2018, 2019, 2020, 2021, 2022]
mean_tingkat_pengangguran = [7.870370, 7.794074, 9.98, 9.401111, 7.801111]
total_jumlah_lowongan_kerja = [8498, 10068, 4509, 143707, 169005]
total_jumlah_penduduk = [20779888, 21902958, 21674854, 22313481, 23452568]

fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 15))

ax1.bar(tahun, mean_tingkat_pengangguran, color='blue')
ax1.set_title('Mean Tingkat Pengangguran Tiap Tahun')
ax1.set_ylabel('Mean Tingkat Pengangguran')

ax2.bar(tahun, total_jumlah_lowongan_kerja, color='green')
ax2.set_title('Total Jumlah Lowongan Kerja Tiap Tahun')
ax2.set_ylabel('Total Jumlah Lowongan Kerja')

ax3.bar(tahun, total_jumlah_penduduk, color='orange')
ax3.set_title('Total Jumlah Penduduk Tiap Tahun')
ax3.set_ylabel('Total Jumlah Penduduk')

plt.xlabel('Tahun')
plt.tight_layout()
plt.show()

"""## Data modelling

### MOVING AVERAGE
"""

window_size = 3
df3['tingkat_pengangguran_ma'] = df3['mean_tingkat_pengangguran'].rolling(window=window_size).mean()
print(df3[['tahun', 'mean_tingkat_pengangguran', 'tingkat_pengangguran_ma']])

"""#### Evaluation model"""

df3.dropna(inplace=True)

mae = mean_absolute_error(df3['mean_tingkat_pengangguran'], df3['tingkat_pengangguran_ma'])
print(f'MAE Moving Average: {mae}')


rmse = np.sqrt(mean_squared_error(df3['mean_tingkat_pengangguran'], df3['tingkat_pengangguran_ma']))
print(f'RMSE Moving Average: {rmse}')

"""### EXPONENTIAL SMOOTHING"""

!pip install statsmodels

from statsmodels.tsa.holtwinters import ExponentialSmoothing

df3['tahun'] = pd.to_datetime(df3['tahun'], format='%Y')
model = ExponentialSmoothing(df3['mean_tingkat_pengangguran'], trend='add', seasonal=None)
fit_model = model.fit()

# Melakukan prediksi untuk data yang telah ada
df3['tingkat_pengangguran_exp_smooth'] = fit_model.fittedvalues

# Melakukan prediksi untuk 1 tahun ke depan
forecast = fit_model.forecast(steps=12)
df3['tingkat_pengangguran_exp_smooth_forecast'] = forecast

"""#### Evaluation model"""

mae_exp_smooth = mean_absolute_error(df3['mean_tingkat_pengangguran'], df3['tingkat_pengangguran_exp_smooth'])
rmse_exp_smooth = np.sqrt(mean_squared_error(df3['mean_tingkat_pengangguran'], df3['tingkat_pengangguran_exp_smooth']))

print(f'MAE Exponential Smoothing: {mae_exp_smooth}')
print(f'RMSE Exponential Smoothing: {rmse_exp_smooth}')

"""### SARIMAX"""

from statsmodels.tsa.statespace.sarimax import SARIMAX

order = (1, 1, 1)  # Parameter order (p, d, q) yang dapat disesuaikan
seasonal_order = (1, 1, 1, 12)  # Parameter seasonal order (P, D, Q, m) yang dapat disesuaikan
model_sarimax = SARIMAX(df3['mean_tingkat_pengangguran'], order=order, seasonal_order=seasonal_order)
fit_model_sarimax = model_sarimax.fit(disp=False)

# Melakukan prediksi untuk data yang telah ada
df3['tingkat_pengangguran_sarimax'] = fit_model_sarimax.fittedvalues

# Melakukan prediksi untuk 1 tahun ke depan
forecast_sarimax = fit_model_sarimax.get_forecast(steps=12)
df3['tingkat_pengangguran_sarimax_forecast'] = forecast_sarimax.predicted_mean

"""#### Evaluation model"""

mae_sarimax = mean_absolute_error(df3['mean_tingkat_pengangguran'], df3['tingkat_pengangguran_sarimax'])
rmse_sarimax = np.sqrt(mean_squared_error(df3['mean_tingkat_pengangguran'], df3['tingkat_pengangguran_sarimax']))

print(f'MAE SARIMAX: {mae_sarimax}')
print(f'RMSE SARIMAX: {rmse_sarimax}')

"""### ARIMA"""

from statsmodels.tsa.arima.model import ARIMA

order = (1, 1, 1)  # Parameter order (p, d, q) yang dapat disesuaikan
model_arima = ARIMA(df3['mean_tingkat_pengangguran'], order=order)
fit_model_arima = model_arima.fit()

# Melakukan prediksi untuk data yang telah ada
df3['tingkat_pengangguran_arima'] = fit_model_arima.fittedvalues

# Melakukan prediksi untuk 1 tahun ke depan
forecast_arima = fit_model_arima.get_forecast(steps=12)
df3['tingkat_pengangguran_arima_forecast'] = forecast_arima.predicted_mean

"""#### Evaluation model"""

mae_arima = mean_absolute_error(df3['mean_tingkat_pengangguran'], df3['tingkat_pengangguran_arima'])
rmse_arima = np.sqrt(mean_squared_error(df3['mean_tingkat_pengangguran'], df3['tingkat_pengangguran_arima']))

print(f'MAE ARIMA: {mae_arima}')
print(f'RMSE ARIMA: {rmse_arima}')

"""### LSTM"""

import tensorflow as tf

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from sklearn.preprocessing import MinMaxScaler

print(df3.mean_tingkat_pengangguran)

from keras.models import Sequential
from keras.layers import LSTM, Dense

df4 = pd.DataFrame({'mean_tingkat_pengangguran': [7.870370, 7.794074, 9.98, 9.401111, 7.801111]})
array_data = df4['mean_tingkat_pengangguran'].values

scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(array_data.reshape(-1, 1))

time_steps = 2
def create_dataset(dataset, time_steps, target_column=0):
    x_data, y_data = [], []
    for i in range(len(dataset) - time_steps):
        a = dataset[i:(i + time_steps), :]
        x_data.append(a)
        y_data.append(dataset[i + time_steps, target_column])
    return np.array(x_data), np.array(y_data)

x_data, y_data = create_dataset(scaled_data, time_steps)

x_data = np.reshape(x_data, (x_data.shape[0], x_data.shape[1], 1))

model_lstm = Sequential()
model_lstm.add(LSTM(units=50, return_sequences=True, input_shape=(x_data.shape[1], 1)))
model_lstm.add(LSTM(units=50))
model_lstm.add(Dense(units=1))
model_lstm.compile(optimizer='adam', loss='mean_squared_error')

model_lstm.fit(x_data, y_data, epochs=50, batch_size=1, verbose=2)

predictions = model_lstm.predict(x_data)

predictions_original = scaler.inverse_transform(predictions.reshape(-1, 1))
y_data_original = scaler.inverse_transform(y_data.reshape(-1, 1))

"""#### Evaluation model"""

mae = mean_absolute_error(y_data_original, predictions_original)
rmse = np.sqrt(mean_squared_error(y_data_original, predictions_original))

print(f'MAE LSTM: {mae}')
print(f'RMSE LSTM: {rmse}')

train_loss = model_lstm.evaluate(x_data, y_data, verbose=0)
print(f'Training Loss: {train_loss}')

predictions = model_lstm.predict(x_data)

plt.plot(y_data, label='Actual Values')
plt.plot(predictions, label='Predictions')
plt.legend()
plt.show()

"""## Conclusion
Pada kelima pemodelan tingkat pengangguran diperoleh:
1. - MAE Moving Average: 1.0113991769547317
  - RMSE Moving Average: 1.118677913133318
2. - MAE Exponential Smoothing: 0.22694174108274337
  - RMSE Exponential Smoothing: 0.2406782397314199
3. - MAE SARIMAX: 4.052962962962962
  - RMSE SARIMAX: 5.845098013027069
4. - MAE ARIMA: 3.9294957106343396
  - RMSE ARIMA: 5.81513577241923
5. - MAE LSTM: 0.044519704182942675
  - RMSE LSTM: 0.0461618310576511


Dari kelima algoritma di atas, LSTM adalah yang paling cocok untuk apply model to machine learning. Hal ini karena LSTM memiliki MAE yang paling kecil, yaitu 0.044519704182942675. MAE yang kecil menunjukkan bahwa LSTM memiliki error yang kecil, sehingga LSTM lebih akurat dalam memprediksitingkat pengagguran untuk peluang kerja di Jawa Barat.

Secara umum, dalam konteks evaluasi model, nilai MAE dan RMSE yang lebih kecil menunjukkan bahwa model memiliki kinerja yang lebih baik. Model LSTM memberikan tingkat error yang sangat rendah, menunjukkan bahwa model ini mampu menangkap pola dan tren dengan baik pada data waktu yang kompleks.

### Implement Model to Machine Learning

Model yg akan digunakan adalah Long Short-Term Memory (LSTM)
"""

path4='/content/drive/MyDrive/DataProject/data_before_2018-2022.xlsx'
load_data4=pd.read_excel(path4)
load_data4
data_pred=pd.DataFrame(load_data4)
data_pred

data_pred.info()

data_pred.loc[:, "total_jumlah_lowongan_kerja"]

"""PREDIKSI TINGKAT PENGANGGURAN"""

time_steps = 2
steps_ahead = 12
future_predictions = []

current_data = x_data[-1]
for _ in range(steps_ahead):
    current_data_reshaped = current_data.reshape(1, time_steps, 1)
    next_prediction_scaled = model_lstm.predict(current_data_reshaped)
    future_predictions.append(next_prediction_scaled[0, 0])
    current_data = np.append(current_data[1:], next_prediction_scaled[0, 0])

future_predictions_original_pengangguran = scaler.inverse_transform(np.array(future_predictions).reshape(-1, 1))

print("Prediksi Tingkat Pengangguran 1 Tahun ke Depan:")
print(future_predictions_original_pengangguran)

"""PREDIKSI JUMLAH LOWONGAN KERJA"""

jumlah_lowongan_kerja = [8498, 10068, 4509, 143707, 169005]

scaler_lowongan = MinMaxScaler(feature_range=(0, 1))
scaled_data_lowongan = scaler_lowongan.fit_transform(np.array(jumlah_lowongan_kerja).reshape(-1, 1))

x_data_lowongan, y_data_lowongan = create_dataset(scaled_data_lowongan, time_steps)
x_data_lowongan = np.reshape(x_data_lowongan, (x_data_lowongan.shape[0], x_data_lowongan.shape[1], 1))

model_lstm_lowongan = Sequential()
model_lstm_lowongan.add(LSTM(units=50, return_sequences=True, input_shape=(x_data_lowongan.shape[1], 1)))
model_lstm_lowongan.add(LSTM(units=50))
model_lstm_lowongan.add(Dense(units=1))
model_lstm_lowongan.compile(optimizer='adam', loss='mean_squared_error')

model_lstm_lowongan.fit(x_data_lowongan, y_data_lowongan, epochs=50, batch_size=1, verbose=2)

predictions_lowongan = model_lstm_lowongan.predict(x_data_lowongan)

predictions_original_lowongan = scaler_lowongan.inverse_transform(predictions_lowongan.reshape(-1, 1))
y_data_original_lowongan = scaler_lowongan.inverse_transform(y_data_lowongan.reshape(-1, 1))

steps_ahead_lowongan = 12
future_predictions_lowongan = []

current_data_lowongan = x_data_lowongan[-1]
for _ in range(steps_ahead_lowongan):
    current_data_reshaped_lowongan = current_data_lowongan.reshape(1, time_steps_lowongan, 1)
    next_prediction_scaled_lowongan = model_lstm_lowongan.predict(current_data_reshaped_lowongan)
    future_predictions_lowongan.append(next_prediction_scaled_lowongan[0, 0])
    current_data_lowongan = np.append(current_data_lowongan[1:], next_prediction_scaled_lowongan[0, 0])

future_predictions_original_lowongan = scaler_lowongan.inverse_transform(np.array(future_predictions_lowongan).reshape(-1, 1))

pd.options.display.float_format = '{:,.0f}'.format

print("Prediksi Jumlah Lowongan Kerja 1 Tahun ke Depan:")
print(future_predictions_original_lowongan)

bulan = [
    'Januari',
    'Februari',
    'Maret',
    'April',
    'Mei',
    'Juni',
    'Juli',
    'Agustus',
    'September',
    'Oktober',
    'November',
    'Desember'
]

df_prediksi = pd.DataFrame({
    'Tahun': [2023 + i for i in range(steps_ahead)],
    'Tingkat Pengangguran': future_predictions_original_pengangguran.flatten(),
    'Jumlah Lowongan Pekerjaan': future_predictions_original_lowongan.flatten()
})
df_prediksi

df_prediksi['Bulan'] = [bulan[i % len(bulan)] for i in range(len(df_prediksi))]
df_prediksi['Jumlah Lowongan Pekerjaan'] = future_predictions_original_lowongan.flatten()
df_prediksi = df_prediksi[['Bulan', 'Tingkat Pengangguran', 'Jumlah Lowongan Pekerjaan']]
df_prediksi

df_prediksi_jenis_pekerjaan = pd.DataFrame({
    'Bulan': [bulan[i % len(bulan)] for i in range(len(df_prediksi))],
    'Tingkat Pengangguran': df_prediksi['Tingkat Pengangguran'],
    'Jumlah Lowongan Pekerjaan': df_prediksi['Jumlah Lowongan Pekerjaan']
})

def predict_jenis_pekerjaan(tingkat_pengangguran):
    jenis_pekerjaan = [
        "TENAGA PROFESIONAL, TEKNISI DAN YANG SEJENIS",
        "TENAGA KEPEMIMPINAN DAN KETATALAKSANAAN",
        "TENAGA TATA USAHA DAN YANG SEJENIS",
        "TENAGA USAHA PENJUALAN",
        "TENAGA USAHA JASA",
        "TENAGA USAHA PERTANIAN, KEHUTANAN, PERBURUAN, DAN PERIKANAN",
        "TENAGA PRODUKSI, OPERATOR ALAT-ALAT ANGKUTAN DAN PEKERJA KASAR, LAINNYA"
    ]

    if tingkat_pengangguran < 8:
        return jenis_pekerjaan[0]
    elif tingkat_pengangguran < 9:
        return jenis_pekerjaan[3]
    else:
        return jenis_pekerjaan[5]

df_prediksi_jenis_pekerjaan['Jenis Pekerjaan'] = df_prediksi_jenis_pekerjaan['Tingkat Pengangguran'].apply(predict_jenis_pekerjaan)

df_prediksi_jenis_pekerjaan

# df_prediksi_jenis_pekerjaan.to_excel('/content/drive/MyDrive/DataProject/data_after.xlsx', index=False)