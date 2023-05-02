import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from prettytable import PrettyTable
import plotly.figure_factory as ff
from IPython.display import display
import plotly.express as px


ppdb21= pd.read_csv("ppdb_2021.csv")
ppdb20= pd.read_csv("ppdb_2020.csv")
ppdb22= pd.read_csv("ppdb_2022.csv")



with st.container():
    # data.info()
    logo, title_text, logo1 = st.columns([1,3,1])
    
    logo.image("logo.png",width=70)
    logo1.image("logo1.png",width=70)
    
    title_text.markdown("""
    <div class="header-logo" style="display: flex; justify-content:space-around; align-items:center;">
            <img src="logo.png" alt="">
            <h3><span>PPDB</span>-<span style="color: lightskyblue;">SMKN 1 Cibinong</span></h3>
            <img src="logo1.png" alt="">
    </div>
    """,unsafe_allow_html=True)
    
    st.markdown("""
        <h1 class="title" style='text-align: center;'>Projek Kelompok NEVTIK SMKN 1 Cibinong!</h1>
        <div class="des-title" style='text-align: center;'>Projek kelompok NEVTIK ialah pengolahan data PPDB 2022 SMKN 1 Cibinong</div>
        <br><br>
    """, unsafe_allow_html=True)
    
    
    
    
    
    #hapus Unnamed
    ppdb22 = ppdb22.loc[:, ~ppdb22.columns.str.contains('^Unnamed')]
    ppdb22 = ppdb22.rename(columns={'Jarak ': 'Jarak', 'Pilihan ': 'Pilihan'})
    
    ppdb20 = ppdb20.rename(columns=lambda x: x.lower().replace(' ', '_'))
    ppdb21 = ppdb21.rename(columns=lambda x: x.lower().replace(' ', '_'))
    ppdb22 = ppdb22.rename(columns=lambda x: x.lower().replace(' ', '_'))
    
    #samain kolom
    print(set(ppdb22 == ppdb21.columns))
    print(set(ppdb22 == ppdb20.columns))
    
    #format penamaan buat rename
    rename_cols = lambda col_name : "_".join(re.split("/| ", col_name.lower()))
    
    #merubah data dll
    for year in range(20, 22):
        # exec(f"ppdb{year}.insert(2, 'tahun_diterima', {year})") # insert year column to each dataset
        exec(f"ppdb{year}.rename(rename_cols, axis='columns', inplace=True)")
        exec(f"ppdb{year}['pilihan'] = np.array([comp.split(' - ')[1] for comp in ppdb{year}.pilihan])") # reformat values of 'pilihan' column
        exec(f"ppdb{year}.loc[:, 'agama1':'skor'] = ppdb{year}.loc[:, 'agama1':'skor'].astype(float)") # convert data type
        exec(f"ppdb{year}['tanggal_lahir'] = pd.to_datetime(ppdb{year}['tanggal_lahir'])") # convert to date time type
        
    ppdb = pd.concat([ppdb20.assign(tahun_diterima=2020).copy(), ppdb21.assign(tahun_diterima=2021).copy(), ppdb22.assign(tahun_diterima=2022).copy()], ignore_index=True)
    
    #remove outliers ppdb2020
    Q1 = ppdb20['skor'].quantile(0.25)
    Q3 = ppdb20['skor'].quantile(0.75)
    IQR = Q3 - Q1
    lower_limit = Q1 - 1.5 * IQR
    upper_limit = Q3 + 1.5 * IQR
    ppdb20 = ppdb20[(ppdb20['skor'] > lower_limit) & (ppdb20['skor'] < upper_limit)]
    
    #remove outliers ppdb2021
    Q1 = ppdb21['skor'].quantile(0.25)
    Q3 = ppdb21['skor'].quantile(0.75)
    IQR = Q3 - Q1
    lower_limit = Q1 - 1.5 * IQR
    upper_limit = Q3 + 1.5 * IQR
    ppdb21 = ppdb21[(ppdb21['skor'] > lower_limit) & (ppdb21['skor'] < upper_limit)]
    
    #remove outliers ppdb2023
    Q1 = ppdb22['skor'].quantile(0.25)
    Q3 = ppdb22['skor'].quantile(0.75)
    IQR = Q3 - Q1
    lower_limit = Q1 - 1.5 * IQR
    upper_limit = Q3 + 1.5 * IQR
    ppdb22 = ppdb22[(ppdb22['skor'] > lower_limit) & (ppdb22['skor'] < upper_limit)]
    
    comp_acro = []
    for comp in ppdb.pilihan:
        clean_comp = comp.replace('DAN','').replace(',','') # remove any conjunction
        acro = ""
    
    fragments = clean_comp.split()
    for frag in fragments:
        acro += frag[0] # take first letter for each word
        if len(fragments) <= 1:
            acro *= 2
            
    comp_acro.append(acro)
    
    # ppdb['pilihan'] = comp_acro
    
    st.markdown("""
        <div class="des-title" style='text-align: center;'>Data di bawah ini merupakan data siswa-siswi yang mengikuti PPDB<br>
        dan data siswa-siswi di bawah ini merupakan data hasil gabungan PPDB 2020-2022 yang sudah diolah sedemikian rupa.</div>
        <br><br>
    """, unsafe_allow_html=True)
    
    ppdb
    
    # hitung jumlah yang daftar
    n_regs = ppdb.tahun_diterima.value_counts().reset_index()
    n_regs.columns = ['year', 'registrants']

    # pakai chart yang berbentuk lingkaran dengan plotly
    fig = px.pie(n_regs, values='registrants', names='year', color='year',
                color_discrete_sequence=['greenyellow', 'slateblue', 'red'])

    # atur title dan legend
    fig.update_layout(
        title={
            'text': "Jumlah Pendaftar Pada Tahun 2020, 2021 dan 2022",
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 16}
        },
        legend={
            'y':0.5,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'middle'
        }
    )

    #teks keterangan
    st.markdown("""
        <div class="des-title" style='text-align: center;'>Setelah melihat data di atas kini kami akan menampilkan jumlah<br>
        pendaftar dari masing-masing tahun PPDB diadakan.</div>
        <br><br>
    """, unsafe_allow_html=True)
    
    #menampilkannya dengan plotly streamlit
    st.plotly_chart(fig)
    
    #teks keterangan
    st.markdown("""
        <div class="des-title" style='text-align: center;'>Dari data di atas terdapat sebuah ketimpangan(karena banyaknya<br>
        data pendaftar pada thaun 2022)pada 2022, namun data pendaftar tahun 2020 dan 2021 tidak berbeda jauh.</div>
        <br><br>
    """, unsafe_allow_html=True)
    
    #kode untuk membuat chart jumlah pendaftar berdasarkan gender pada tahun 2020
    fig20 = px.histogram(ppdb20, x="jenis_kelamin", color="jenis_kelamin", 
                   color_discrete_sequence=["slateblue", "pink"])

    fig20.update_layout(
        title={
            'text': "Jumlah Peserta PPDB 2020 Berdasarkan gender",
            'x':0.5,
            'y':0.95,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        xaxis_title="Jenis Kelamin",
        yaxis_title="Jumlah Peserta",
        font=dict(size=12)
    )
    
    
    #kode untuk membuat chart jumlah pendaftar berdasarkan gender pada tahun 2021
    fig21 = px.histogram(ppdb21, x="jenis_kelamin", color="jenis_kelamin", 
                   color_discrete_sequence=["slateblue", "pink"])

    fig21.update_layout(
        title={
            'text': "Jumlah Peserta PPDB 2022 Berdasarkan Gender",
            'x':0.5,
            'y':0.95,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        xaxis_title="Jenis Kelamin",
        yaxis_title="Jumlah Peserta",
        font=dict(size=12)
    )
    
    #kode untuk membuat chart jumlah pendaftar berdasarkan gender pada tahun 2022
    fig22 = px.histogram(ppdb22, x="jenis_kelamin", color="jenis_kelamin", 
                   color_discrete_sequence=["slateblue", "pink"])

    fig22.update_layout(
        title={
            'text': "Jumlah Peserta PPDB 2022 Berdasarkan Gender",
            'x':0.5,
            'y':0.95,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        xaxis_title="Jenis Kelamin",
        yaxis_title="Jumlah Peserta",
        font=dict(size=12)
    )
    
    
    #teks keterangan
    st.markdown("""
        <div class="des-title" style='text-align: center;'>Selanjutnya kami akan memberikan data jumlah pendaftar berdasarkan gender<br>
        dari tahun 2020-2022.</div>
        <br><br>
    """, unsafe_allow_html=True)

    #menampilkan plot berdasarkan tahun
    st.plotly_chart(fig20)
    st.plotly_chart(fig21)
    st.plotly_chart(fig22)
    
    #kode untuk memnuat plot data pendaftar berdsarkan provinsi dari tahun 2020
    fig20 = px.histogram(ppdb20, x='provinsi', color_discrete_sequence=px.colors.qualitative.Set2)

    fig20.update_layout(
        title={
            'text': "Jumlah Peserta PPDB 2020 Berdasarkan Provinsi Asal",
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 16}
        },
        xaxis_title="Provinsi",
        yaxis_title="Jumlah Peserta",
    )
    
    #kode untuk memnuat plot data pendaftar berdsarkan provinsi dari tahun 2021
    fig21 = px.histogram(ppdb21, x='provinsi', color_discrete_sequence=px.colors.qualitative.Set2)

    fig21.update_layout(
        title={
            'text': "Jumlah Peserta PPDB 2021 Berdasarkan Provinsi Asal",
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 16}
        },
        xaxis_title="Provinsi",
        yaxis_title="Jumlah Peserta",
    )
    
    #kode untuk memnuat plot data pendaftar berdsarkan provinsi dari tahun 2022
    fig22 = px.histogram(ppdb22, x='provinsi', color_discrete_sequence=px.colors.qualitative.Set2)

    fig22.update_layout(
        title={
            'text': "Jumlah Peserta PPDB 2020 Berdasarkan Provinsi Asal",
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 16}
        },
        xaxis_title="Provinsi",
        yaxis_title="Jumlah Peserta",
    )

    #teks keterangan
    st.markdown("""
        <div class="des-title" style='text-align: center;'>Pada data ppdb para pendaftar berasal dari beberapa provinsi, berikut data jumlah pendaftar<br>
        berdasarkan provinsi.</div>
        <br><br>
    """, unsafe_allow_html=True)
    
    #menampilkan plot berdasarkan tahun
    st.plotly_chart(fig20)
    st.plotly_chart(fig21)
    st.plotly_chart(fig22)
    
    percent_saintek = {}
    percent_soshum = {}

# Group the data by pilihan (the chosen major)
    grouped = ppdb.groupby('pilihan')

# Loop through each group and calculate the percentage of SAINTEK and SOSHUM participants
    for pilihan, group in grouped.groups.items():
        kelompok = ppdb.loc[group]
        
        # Take the columns to calculate the number of saintek or soshum
        kolom_saintek = ['ipa1', 'ipa2', 'ipa3', 'ipa4', 'ipa5', 'matematika1', 'matematika2', 'matematika3', 'matematika4', 'matematika5']
        kolom_soshum = ['ips1', 'ips2', 'ips3', 'ips4', 'ips5', 'ppkn1', 'ppkn2', 'ppkn3', 'ppkn4', 'ppkn5', 'bing1', 'bing2', 'bing3', 'bing4', 'bing5', 'bindo1', 'bindo2', 'bindo3', 'bindo4', 'bindo5']
        
        # Count the number of participants who chose the SAINTEK or SOSHUM subjects in this group
        count_saintek = kelompok[kolom_saintek].sum().sum()
        count_soshum = kelompok[kolom_soshum].sum().sum()
        
        # Calculate the percentage of the number of participants who chose the SAINTEK or SOSHUM studies subject in this group
        total_peserta = len(kelompok)
        percent_saintek[pilihan] = round((count_saintek / total_peserta) * 100)
        percent_soshum[pilihan] = round((count_soshum / total_peserta) * 100)

    # Create a dataframe from the calculation results
    df_percent = pd.DataFrame({'Saintek (%)': percent_saintek, 'Soshum (%)': percent_soshum})

    # Highlight the highest value in each column
    highlighted = df_percent.style.highlight_max(axis=0)

    # Display the highlighted dataframe using Streamlit
    st.write(highlighted)
    
    
    # def send_email(subject, message, to_email):
    # # Implementasi fungsi send_email di sini

    #     def contact_us():
    #         # Tampilkan formulir kontak
    #         st.write("### Contact Us")
    #         name = st.text_input("Name")
    #         email = st.text_input("Email")
    #         message = st.text_area("Message")
    #         if st.button("Send"):
    #             # Kirim email
    #             if send_email(subject=f"Message from {name}",
    #                         message=message,
    #                         to_email="example@gmail.com"):
    #                 st.success("Your message has been sent!")
    #             else:
    #                 st.error("Oops! Something went wrong.")
                    
    # send_email(subject, message, to_email)