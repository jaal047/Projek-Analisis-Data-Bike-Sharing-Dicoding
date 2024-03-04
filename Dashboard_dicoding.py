import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go

# Load data
data_day = pd.read_csv("data_day.csv")
data_hr = pd.read_csv("data_hr.csv")
# List of datasets
datasets = {
    "Data Day": data_day,
    "Data Hour": data_hr
}
# Definisi pemetaan nilai ke keterangan
mapping = {
    'mnth': {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'},
    'season': {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'},
    'weekday': {0: 'Sun', 1: 'Mon', 2: 'Tue', 3: 'Wed', 4: 'Thu', 5: 'Fri', 6: 'Sat'},
    'weathersit': {1: 'Clear/Partly Cloudy', 2: 'Misty/Cloudy', 3: 'Light Snow/Rain', 4: 'Heavy Rain/Thunderstorm'}
}

# Melakukan pemetaan nilai ke keterangan dan mengubah tipe data secara massal
for df in [data_day, data_hr]:
    df.replace(mapping, inplace=True)
    df['dteday'] = pd.to_datetime(df['dteday'])
    df['season'] = df['season'].astype('category')
    df['yr'] = df['yr'].astype('category')
    df['mnth'] = df['mnth'].astype('category')
    df['holiday'] = df['holiday'].astype('category')
    df['weekday'] = df['weekday'].astype('category')
    df['workingday'] = df['workingday'].astype('category')
    df['weathersit'] = df['weathersit'].astype('category')
data_day = data_day.drop(columns=['instant'])
data_hr = data_hr.drop(columns=['instant'])

# Fungsi untuk menghasilkan deskripsi data
def generate_data_description(datasets):
    st.title("Deskripsi Data")
    st.subheader("Background")
    st.write("Sistem berbagi sepeda adalah generasi baru dari persewaan sepeda tradisional di mana seluruh proses mulai dari keanggotaan, penyewaan, dan pengembalian menjadi otomatis. Melalui sistem ini, pengguna dapat dengan mudah menyewa sepeda dari posisi tertentu dan kembali lagi ke posisi lain. Saat ini, terdapat lebih dari 500 program berbagi sepeda di seluruh dunia yang mencakup lebih dari 500 ribu sepeda. Saat ini, terdapat minat yang besar terhadap sistem ini karena peran pentingnya dalam masalah lalu lintas, lingkungan dan kesehatan.")
    st.write("Terlepas dari penerapan sistem bike sharing di dunia nyata yang menarik, karakteristik data yang dihasilkan oleh sistem ini menjadikannya menarik untuk penelitian. Berbeda dengan layanan transportasi lain seperti bus atau kereta bawah tanah, durasi perjalanan, posisi keberangkatan dan kedatangan dicatat secara eksplisit dalam sistem ini. Fitur ini mengubah sistem bike sharing menjadi jaringan sensor virtual yang dapat digunakan untuk mendeteksi mobilitas dalam kota. Oleh karena itu, diharapkan sebagian besar peristiwa penting di kota dapat dideteksi melalui pemantauan data ini.")
    st.subheader("Konten")
    st.write("Hour.csv dan day.csv memiliki kolom berikut,")
    text = '''
    - instant: record index
    - dteday: date
    - season: season (1: spring, 2: summer, 3: fall, 4: winter)
    - yr: year (0: 2011, 1: 2012)
    - mnth: month (1 to 12)
    - hr: hour (0 to 23)
    - holiday: weather day is holiday or not (extracted from http://dchr.dc.gov/page/holiday-schedule)
    - weekday: day of the week
    - workingday: if day is neither weekend nor holiday is 1, otherwise is 0.
    - weathersit: 
        - 1: Clear, Few clouds, Partly cloudy, Partly cloudy
        - 2: Mist + Cloudy, Mist + Broken clouds, Mist + Few clouds, Mist
        - 3: Light Snow, Light Rain + Thunderstorm + Scattered clouds, Light Rain + Scattered clouds
        - 4: Heavy Rain + Ice Pallets + Thunderstorm + Mist, Snow + Fog
    - temp: Normalized temperature in Celsius. The values are divided to 41 (max)
    - atemp: Normalized feeling temperature in Celsius. The values are divided to 50 (max)
    - hum: Normalized humidity. The values are divided to 100 (max)
    - windspeed: Normalized wind speed. The values are divided to 67 (max)
    - casual: count of casual users
    - registered: count of registered users
    - cnt: count of total rental bikes including both casual and registered
    '''
    st.write(text)
    st.subheader("Ucapan Terima Kasih")
    st.write('''
    Hadi Fanaee-T
    Laboratory of Artificial Intelligence and Decision Support (LIAAD), University of Porto
    INESC Porto, Campus da FEUP
    Rua Dr. Roberto Frias, 378
    4200 - 465 Porto, Portugal

    Original Source: http://capitalbikeshare.com/system-data
    Weather Information: http://www.freemeteo.com
    Holiday Schedule: http://dchr.dc.gov/page/holiday-schedule
    ''')
    st.subheader("Dataset")
    # Membuat selectbox jika user ingin melihat jenis datanya
    selected_dataset = st.selectbox("Pilih dataset:", list(datasets.keys()))

    # Display selected dataset
    st.write(datasets[selected_dataset])
    # Membuat statistika deskriptif data
    st.write("**Statistika Deskriptif Data:**")
    st.write(datasets[selected_dataset].describe())


def Soal1(data_hr,selected_chart):
    st.title("Pengaruh Cuaca")
    st.sidebar.title("Filter")
    selected_chart = st.sidebar.selectbox("Pilih chart:",["Persebaran Pengguna", "Perbandingan Jumlah Pengguna"])
    if selected_chart == "Persebaran Pengguna":
        st.subheader("Persebaran Jumlah Peminjaman Sepeda Pada Tiap Cuaca")
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.boxplot(data=data_hr, x='weathersit', y='cnt', ax=ax)
        ax.set_xlabel('Kondisi Cuaca')
        ax.set_ylabel('Jumlah Peminjaman Sepeda')
        st.pyplot(fig)
        st.write('''
        Dapat dilihat dari visualisasi diatas ini menunjukkan persebaran data Jumlah peminjam sepeda pada cuaca berbeda, dapat diliat Rata rata peminjaman paling banyak dilakukan pada cuaca clear dan juga cloudy. pada cuca light snow/rain dan juga Heavy rain memiliki rata rata jumlah peminjam paling sedikit
        ''')
    else:
        st.subheader("Jumlah Peminjam Sepeda Pada Tiap Cuaca")
        # Hitung jumlah penggunaan sepeda berdasarkan kondisi cuaca
        bike_usage_by_weather = data_hr.groupby('weathersit')['cnt'].sum().reset_index()
        st.set_option('deprecation.showPyplotGlobalUse', False)
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(data=bike_usage_by_weather, x='weathersit', y='cnt', ax=ax)
        plt.title('Peminjaman Sepeda berdasarkan Kondisi Cuaca')
        plt.xlabel('Kondisi Cuaca')
        plt.ylabel('Jumlah Peminjaman Sepeda')
        plt.xticks(rotation=45)
        plt.tight_layout()
        st.pyplot(fig)
        st.write('''
        Dari visualisasi ini juga menunjukkan hal yang sama yaitu perbandingan peminjam berdasarkan cuaca menunjukkan memang paling banyak peminjaman dilakukan saat cuaca clear.
        ''')

def soal2(data_day,selected_variabel):
    st.title("Pengaruh Hari Libur")
    st.sidebar.title("Filter")
    selected_variabel = st.sidebar.selectbox("Pilih User:",["Total Peminjam", "Peminjam Resitered", "Peminjam Casual"])
    mapping = {'workingday': {0: 'Hari Libur', 1: 'Hari Kerja'}}
    data_day.replace(mapping, inplace=True)
    if selected_variabel == "Total Peminjam":
        st.subheader("Perbedaan Total Jumlah Peminjaman Sepeda Antara Hari Libur dan Hari Kerja")
        bike_rentals_by_workingday = data_day.groupby('workingday')['cnt'].sum().reset_index()
        fig = px.bar(bike_rentals_by_workingday, x='workingday', y='cnt', color='workingday', labels={'workingday': 'Hari', 'cnt': 'Jumlah Total Peminjaman Sepeda'})
        st.plotly_chart(fig)
        st.write('''
        Didapatkan bahwasannya ternyata peminjam sepeda paling banyak ada pada Hari kerja dibandingan saat hari libur
        ''')
    if selected_variabel == "Peminjam Resitered":
        st.subheader("Perbedaan Jumlah Peminjaman Sepeda Peminjam Registered Antara Hari Libur dan Hari Kerja")
        bike_rentals_by_workingday = data_day.groupby('workingday')['registered'].sum().reset_index()
        fig = px.bar(bike_rentals_by_workingday, x='workingday', y='registered', color='workingday', labels={'workingday': 'Hari', 'registered': 'Jumlah Peminjaman Sepeda Peminjam Registered'})
        st.plotly_chart(fig)
        st.write('''
        Dapat dilihat dari visualisasi diatas ini menunjukkan bahwasannya jumlah peminjam Registered meminjam sepeda paling banyak ada pada Hari kerja dibandingan saat hari libur
        ''')
    if selected_variabel == "Peminjam Casual":
        st.subheader("Perbedaan Jumlah Peminjaman Sepeda Peminjam Casual Antara Hari Libur dan Hari Kerja")
        bike_rentals_by_workingday = data_day.groupby('workingday')['casual'].sum().reset_index()
        fig = px.bar(bike_rentals_by_workingday, x='workingday', y='casual', color='workingday', labels={'workingday': 'Hari', 'casual': 'Jumlah Peminjaman Sepeda Peminjam Casual'})
        st.plotly_chart(fig)
        st.write('''
        Dapat dilihat dari visualisasi diatas ini menunjukkan bahwasannya jumlah peminjam casual tidak terlalu berbeda jauh antara saat hari libur dan juga hari kerja
        ''')

def soal3(data_day,selected_var):
    st.title("Pola Waktu")
    st.sidebar.title("Filter")
    selected_var = st.sidebar.selectbox("Pilih :",["Peminjam 2011 dan 2012", "Trend Peminjam Pertahun", "Peminjam Perjam"])
    if selected_var == "Peminjam 2011 dan 2012":
        st.subheader("Perbandingan Total Jumlah Peminjam Sepeda Antara Tahun 2011 dan 2012")
        bike_rentals_by_year = data_day.groupby('yr')['cnt'].sum().reset_index()
        colors = ['#EE4266', '#337357']
        fig = go.Figure(data=[go.Bar(
            x=bike_rentals_by_year['yr'].map({0: '2011', 1: '2012'}),
            y=bike_rentals_by_year['cnt'],
            marker_color=colors
        )])
        fig.update_layout(
            title='Perbedaan Jumlah Peminjaman Sepeda antara Tahun 2011 dan 2012',
            xaxis=dict(title='Tahun'),
            yaxis=dict(title='Jumlah Peminjaman Sepeda'),
        )
        st.plotly_chart(fig)
        st.write('''
        Didapatkan bahwasannya terjadi peningkatan jumlah total peminjam sepeda dari tahun 2011 ke 2012 dimana dari dari 1.2 juta ke 2 juta
        ''')
    if selected_var == "Trend Peminjam Pertahun":
        st.subheader("Trend Peminjaman Sepeda")
        st.sidebar.title("Waktu")
        selected_tm = st.sidebar.selectbox("Pilih Waktu:",["2011 vs 2012", "2011", "2012"])
        data_day['mnth'] = pd.Categorical(data_day['mnth'], categories=[
            'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
            'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
        ], ordered=True)
        if selected_tm == "2011 vs 2012":
            bike_rentals_by_month = data_day.groupby(['yr', 'mnth'])['cnt'].sum().reset_index()
            bike_rentals_2011 = bike_rentals_by_month[bike_rentals_by_month['yr'] == 0]
            bike_rentals_2012 = bike_rentals_by_month[bike_rentals_by_month['yr'] == 1]
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=bike_rentals_2011['mnth'], y=bike_rentals_2011['cnt'], mode='lines', name='2011', marker_color='#7D0A0A'))
            fig.add_trace(go.Scatter(x=bike_rentals_2012['mnth'], y=bike_rentals_2012['cnt'], mode='lines', name='2012', marker_color='#59D5E0'))
            fig.update_layout(
                title='Tren Jumlah Peminjaman Sepeda per Bulan (2011 vs 2012)',
                xaxis=dict(title='Bulan'),
                yaxis=dict(title='Jumlah Peminjaman Sepeda'),
            )
            st.plotly_chart(fig)
            st.write('''
            Dapat dilihat dari tren Jumlah peminjam Sepeda perbulannya tidak terlalu beda untuk pola nya antara tahun 2011 dengan tahun 2012 dimana terjadi kenaikan peminjam sepeda pada bulan februari hingga oktober selanjutnya mengalami penurunan pada bulan november hingga januari.
            ''')
        if selected_tm == "2011":
            resample_type = st.sidebar.selectbox("Pilih Data", ["Month","Day"])
            if resample_type == "Month":
                bike_rentals_by_month = data_day.groupby(['yr', 'mnth'])['cnt'].sum().reset_index()
                bike_rentals_2011 = bike_rentals_by_month[bike_rentals_by_month['yr'] == 0]
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=bike_rentals_2011['mnth'], y=bike_rentals_2011['cnt'], mode='lines', name='2011', marker_color='#7D0A0A'))
                fig.update_layout(
                    title='Tren Jumlah Peminjaman Sepeda per Bulan Pada Tahun 2011',
                    xaxis=dict(title='Bulan'),
                    yaxis=dict(title='Jumlah Peminjaman Sepeda'),
                )
                st.plotly_chart(fig)
                st.write('''
                Dapat dilihat dari tren Jumlah peminjam Sepeda dari bulan Januari hingga Juni mengalami kenaikan jumlah yang signifikan akan tetapi menjelang akhir tahun mengalami penurunan jumlah
                ''')
            if resample_type == "Day":
                data_day['dteday'] = pd.to_datetime(data_day['dteday'])
                data_2011 = data_day[data_day['dteday'].dt.year == 2011]
                st.sidebar.title("Rentang Tanggal")
                start_date = st.sidebar.date_input("Mulai Tanggal", pd.to_datetime('2011-01-01'))
                end_date = st.sidebar.date_input("Akhir Tanggal", pd.to_datetime('2011-12-31'))
                start_date = pd.to_datetime(start_date)
                end_date = pd.to_datetime(end_date)
                filtered_data = data_2011[(data_2011['dteday'] >= start_date) & (data_2011['dteday'] <= end_date)]
                daily_rentals = filtered_data.groupby('dteday')['cnt'].sum().reset_index()
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=daily_rentals['dteday'], y=daily_rentals['cnt'], mode='lines', name='Jumlah Peminjaman Sepeda'))
                fig.update_layout(title='Tren Jumlah Peminjaman Sepeda per Hari (Tahun 2011)',
                                xaxis_title='Tanggal',
                                yaxis_title='Jumlah Peminjaman Sepeda')
                st.plotly_chart(fig)
        if selected_tm == "2012":
            resample_type = st.sidebar.selectbox("Pilih Data", ["Month","Day"])
            if resample_type == "Month":
                bike_rentals_by_month = data_day.groupby(['yr', 'mnth'])['cnt'].sum().reset_index()
                bike_rentals_2012 = bike_rentals_by_month[bike_rentals_by_month['yr'] == 1]
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=bike_rentals_2012['mnth'], y=bike_rentals_2012['cnt'], mode='lines', name='2012', marker_color='#1B3C73'))
                fig.update_layout(
                    title='Tren Jumlah Peminjaman Sepeda per Bulan Pada Tahun 2012',
                    xaxis=dict(title='Bulan'),
                    yaxis=dict(title='Jumlah Peminjaman Sepeda'),
                )
                st.plotly_chart(fig)
                st.write('''
                Dapat dilihat dari tren Jumlah peminjam Sepeda dari bulan Januari hingga September mengalami kenaikan jumlah yang signifikan akan tetapi menjelang akhir tahun mengalami penurunan jumlah
                ''')
            if resample_type == "Day":
                data_day['dteday'] = pd.to_datetime(data_day['dteday'])
                data_2012 = data_day[data_day['dteday'].dt.year == 2012]
                st.sidebar.title("Rentang Tanggal")
                start_date = st.sidebar.date_input("Mulai Tanggal", pd.to_datetime('2012-01-01'))
                end_date = st.sidebar.date_input("Akhir Tanggal", pd.to_datetime('2012-12-31'))
                start_date = pd.to_datetime(start_date)
                end_date = pd.to_datetime(end_date)
                filtered_data = data_2012[(data_2012['dteday'] >= start_date) & (data_2012['dteday'] <= end_date)]
                daily_rentals = filtered_data.groupby('dteday')['cnt'].sum().reset_index()
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=daily_rentals['dteday'], y=daily_rentals['cnt'], mode='lines', name='Jumlah Peminjaman Sepeda'))
                fig.update_layout(title='Tren Jumlah Peminjaman Sepeda per Hari (Tahun 2012)',
                                xaxis_title='Tanggal',
                                yaxis_title='Jumlah Peminjaman Sepeda')
                st.plotly_chart(fig)
            
    if selected_var == "Peminjam Perjam":
        st.subheader("Pola Peminjaman Sepeda Dilihat Dari Jumlah Total Peminjam Perjamnya")
        bike_rentals_by_hour = data_hr.groupby('hr')['cnt'].sum().reset_index()
        fig = go.Figure(data=[go.Bar(
            x=bike_rentals_by_hour['hr'],
            y=bike_rentals_by_hour['cnt'],
            marker_color='skyblue'
        )])
        fig.update_layout(
            title='Jumlah Total Penyewaan Sepeda per Jam',
            xaxis=dict(title='Jam'),
            yaxis=dict(title='Jumlah Penyewaan Sepeda'),
        )
        st.plotly_chart(fig)
        st.write('''
        Dapat dilihat dari visualisasi diatas. Didapatkan bahwasannya peminjam sepeda paling banyak meminjam pada jam 8 pagi dan juga pada jam 17-18 sore
        ''')

def soal4(data_day,selected_variabel):
    st.title("Pengaruh Musim")
    st.sidebar.title("Filter")
    selected_variabel = st.sidebar.selectbox("Pilih User:",["Resitered vs Casual", "Peminjam Resitered", "Peminjam Casual", "Total Peminjam"])
    if selected_variabel == "Resitered vs Casual":
        st.subheader("Perbandingan Jumlah Peminjam Resitered vs Casual di Berbagai Musim")
        registered_rentals_by_season = data_day.groupby(['season'])['registered'].sum().reset_index()
        casual_rentals_by_season = data_day.groupby(['season'])['casual'].sum().reset_index()
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=registered_rentals_by_season['season'],
            y=registered_rentals_by_season['registered'],
            name='Registered Users',
            marker_color = '#F3B95F'
        ))
        fig.add_trace(go.Bar(
            x=casual_rentals_by_season['season'],
            y=casual_rentals_by_season['casual'],
            name='Casual Users',
            marker_color = '#6895D2'
        ))
        fig.update_layout(
            title='Jumlah Total Penyewaan Sepeda Berdasarkan Musim dan Jenis Pelanggan',
            xaxis=dict(title='Musim'),
            yaxis=dict(title='Jumlah Penyewaan Sepeda'),
            barmode='group'
        )
        st.plotly_chart(fig)
        st.write('''
        Didapatkan bahwasannya musim tidak mempengaruhi terhadap perbandingan jumlah penyewa sepeda berdasarkan pelanggan Casual dan Registered, karena dapat dilihat pada semua musim tetap pelanggan Registered yang menyewa sepeda lebih banyak dibandingkkan penyewa casual
        ''')
    if selected_variabel == "Peminjam Resitered":
        st.subheader("Jumlah Peminjaman Sepeda Peminjam Registered Pada Tiap Musim")
        registered_rentals_by_season = data_day.groupby(['season'])['registered'].sum().reset_index()
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=registered_rentals_by_season['season'],
            y=registered_rentals_by_season['registered'],
            name='Registered Users',
            marker_color = '#416D19'
        ))
        fig.update_layout(
            title='Jumlah Total Penyewaan Sepeda oleh Peminjam Registered Berdasarkan Musim',
            xaxis=dict(title='Musim'),
            yaxis=dict(title='Jumlah Penyewaan Sepeda'),
        )
        st.plotly_chart(fig)
        st.write('''
        Dapat dilihat dari visualisasi diatas ini menunjukkan bahwasannya jumlah peminjam Registered meminjam sepeda paling sedikit ada pada musim Spring
        ''')
    if selected_variabel == "Peminjam Casual":
        st.subheader("Jumlah Peminjaman Sepeda Peminjam Casual Pada Tiap Musim")
        casual_rentals_by_season = data_day.groupby(['season'])['casual'].sum().reset_index()
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=casual_rentals_by_season['season'],
            y=casual_rentals_by_season['casual'],
            name='Casual Users',
            marker_color = '#FBA834'
        ))
        fig.update_layout(
            title='Jumlah Total Penyewaan Sepeda oleh Peminjam Casual Berdasarkan Musim',
            xaxis=dict(title='Musim'),
            yaxis=dict(title='Jumlah Penyewaan Sepeda'),
        )
        st.plotly_chart(fig)
        st.write('''
        Dapat dilihat dari visualisasi diatas ini menunjukkan bahwasannya jumlah peminjam Casual meminjam sepeda paling sedikit juga ada pada musim Spring
        ''')
    if selected_variabel == "Total Peminjam":
        st.subheader("Jumlah Total Peminjaman Sepeda Pada Tiap Musim")
        cnt_rentals_by_season = data_day.groupby(['season'])['cnt'].sum().reset_index()
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=cnt_rentals_by_season['season'],
            y=cnt_rentals_by_season['cnt'],
            name='Total Peminjam Sepeda',
            marker_color = '#AD88C6'
        ))
        fig.update_layout(
            title='Jumlah Total Penyewaan Sepeda Berdasarkan Musim',
            xaxis=dict(title='Musim'),
            yaxis=dict(title='Jumlah Penyewaan Sepeda'),
        )
        st.plotly_chart(fig)
        st.write('''
        Dapat dilihat dari visualisasi diatas ini menunjukkan bahwasannya jumlah Total Pememinjam sepeda paling sedikit memang ada pada musim Spring
        ''')

def korelasi(data_hr):
    st.title("Korelasi Antar Variabel Dalam Data")
    correlation_matrix = data_hr.corr(numeric_only=True)
    mask = np.triu(np.ones_like(correlation_matrix, dtype=bool))
    fig, ax = plt.subplots(figsize=(10,6))
    sns.heatmap(
        correlation_matrix,
        annot=True,
        mask=mask,
        cmap="coolwarm",
        center=0,
        fmt=".2f")
    plt.title("Correlation Heatmap")
    st.pyplot(fig)
    st.write('''
        Dari heatmap diatas menunjukkan hubungan korelasi antar variabel, dapat dilihat temp dan atemp memiliki korelasi yang sangat tinggi karena itu dengan hanya memilih salah satu varibel dari itu saja sudah mewakili salah satu variabel jadi salah satu variabel dapat dihapus. Lalu untuk jumlah penyewa registered seperti hasil eksplorasi sebelumnya menunjukkanhubungna yang sangat kuat untuk berdampak pada varibael cnt
        ''')
    
    # Scatter plot
    st.subheader("ScatterPlot Hubungan Tiap Variabel")
    data_var = ['hr','temp','atemp','hum','windspeed','casual','registered','cnt']
    x_variable = st.selectbox("Pilih variabel untuk sumbu x:", data_var)
    y_variable = st.selectbox("Pilih variabel untuk sumbu y:", data_var)

    scatter_fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(data_hr[x_variable], data_hr[y_variable], alpha=0.5)
    ax.set_title(f'Hubungan antara {x_variable} dan {y_variable}')
    ax.set_xlabel(f'{x_variable}')
    ax.set_ylabel(f'{y_variable}')
    ax.grid(True)
    st.pyplot(scatter_fig)


# Sidebar
st.sidebar.title("Navigasi")
page = st.sidebar.radio("", ("Deskripsi Data", "Pengaruh Cuaca", "Pengaruh Hari Libur", "Pola Waktu", "Pengaruh Musim","Korelasi"))

# Routing
if page == "Deskripsi Data":
    generate_data_description(datasets)
elif page == "Pengaruh Cuaca":
    Soal1(data_hr,"Persebaran Pengguna")  
elif page == "Pengaruh Hari Libur":
    soal2(data_day,"Total Peminjam")
elif page == "Pola Waktu":
    soal3(data_day,"Peminjam 2011 dan 2012")
elif page == "Pengaruh Musim":
    soal4(data_day,"Peminjam 2011 dan 2012")
elif page == "Korelasi":
    korelasi(data_hr)