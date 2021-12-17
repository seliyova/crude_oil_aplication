#Nama: Seli Yovanka L.
#NIM: 12220067
#UAS Pemrograman Komputer


"""
Aplikasi Streamlit untuk menggambarkan statistik produksi minyak mentah di berbagai negara dari tahun 1971 hingga 2015
Sumber data berasal dari “produksi_minyak_mentah.csv”
Referensi API Streamlit: https://docs.streamlit.io/library/api-reference
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm
import streamlit as st
import json
from PIL import Image


############### title ###############
st.set_page_config(layout="wide")  # this needs to be the first Streamlit command called
st.title("Statistic of Worldwide Crude Oil Production from 1971 to 2015")
st.markdown("*Source datas are obtained from “produksi_minyak_mentah.csv”*")
############### title ###############)

############### sidebar ###############
image = Image.open('oil.jpg')
st.sidebar.image(image, width=None, use_column_width=True)
st.sidebar.write("Welcome to Crude Oil Aplication Web.")
st.sidebar.write("This web contains many statistics data of crude oil production over worldwide")
st.sidebar.write("Hope you will enjoy this app...")

#Mengekstrak File CSV
file=pd.read_csv("produksi_minyak_mentah.csv")
#Mengekstrak file json
file2=open('kode_negara_lengkap.json',"r")
file2=json.load(file2)

#Mengonversi kode negara menjadi nama negara lengkap
nama_negara={item['alpha-3']:item['name']for item in file2}
file.loc[:,'kode_negara']=file['kode_negara'].map(nama_negara)
#Mengeksklude data produksi minyak yang tidak terdapat dalam kode_negara_lengkap
file.dropna(subset=["kode_negara"], inplace=True)
file=file.rename(columns={'kode_negara':'nama_negara'})
#Mendapatkan nama negara lengkap sesuai data yang berhasil diekstrak dan mengubahnya dalam bentuk list #Menghapus nama negara duplikat
list_namanegara=file['nama_negara'].drop_duplicates().tolist()

#Membuat 2 kolom
col1,col2=st.columns(2)

###############  Upper  Left Column ###############
#Membuat Grafik jumlah produksi minyak mentah terhadap waktu (tahun) dari suatu negara N, dimana nilai N dapat dipilih oleh user secara interaktif
col1.subheader("Chart of Crude Oil Production of Selected Country against Year")
#Membuat selectbox sebagai inputan user
country =col1.selectbox("Select Country", list_namanegara)
n_tampil = col1.number_input("Pick How Many Rows You Want to Display in Table Below", min_value=1, max_value=None, value=10)
negara_pilihan=country
#Memfilter data frame dari CSV sesuai dengan negara yang dipilih
filter=file['nama_negara']==negara_pilihan
data_pilihan=file[filter].rename(columns={'nama_negara':"Country's name", 'tahun':'Year', 'produksi':'Production'})
#Fitur Tambahan berupa Tampilan Tabel pilihan
col1.write("Representation Table")
tabel_tampilan=data_pilihan.head(n_tampil)
col1.write(tabel_tampilan)
#Fitur wajib 1: Membuat Grafiknya
cmap_name = 'tab20c'
cmap = cm.get_cmap(cmap_name)
colors = cmap.colors[:len(data_pilihan)]
fig, ax = plt.subplots()
ax.bar(data_pilihan['Year'] ,data_pilihan['Production'],color=colors)
ax.set_title("Production Chart of Selected Country From 1971 to 2015")
ax.set_ylabel('Oil Production', fontsize=12)
ax.set_xlabel('Year',fontsize=12)  
col1.pyplot(fig)



############## Lower Left Column 1 ##############
#Grafik yang menunjukan B-besar negara dengan jumlah produksi terbesar pada tahun T, dimana nilai B dan T dapat dipilih oleh user secara interaktif.
col1.subheader("Chart of Selected Number of Countries with Largest Crude Oil Production against Year")
count_country = col1.number_input("Pick Number of Country you Want", min_value=1, max_value=137,value=10)
year=col1.number_input("Pick the Year you Want", min_value=1971, max_value=2015)
filter=file['tahun']==year
#Fitur tambahan berupa tabel pilihan2
data_pilihan2=file[filter].sort_values(by=['produksi'], ascending=False).head(count_country)
data_tampil2=data_pilihan2.rename(columns={'nama_negara':"Country's name", 'tahun':'Year', 'produksi':'Production'})
col1.write("Representation Table")
col1.write(data_tampil2)
#Fitur wajib 2: Membuat Grafiknya
cmap_name = 'tab20b'
cmap = cm.get_cmap(cmap_name)
colors = cmap.colors[:len(data_pilihan2)]
fig, ax = plt.subplots()
ax.bar(data_pilihan2['nama_negara'] ,data_pilihan2['produksi'],color=colors)
ax.set_title("Chart of the Most Productive Country with Selected Year")
ax.set_ylabel('Production', fontsize=12)
ax.set_xlabel("Country's name",fontsize=12)
fig.autofmt_xdate()
col1.pyplot(fig)


############## Lower Left Column 2 ###############
#Grafik yang menunjukan B-besar negara dengan jumlah produksi terbesar secara kumulatif keseluruhan tahun, dimana nilai B dapat dipilih oleh user secara interaktif.
col1.subheader("Chart of Selected Number of Country with Largest Cumulative Crude Oil Production all of Years")
count_country2 = col1.number_input("Pick Number of Country you Want to Visualize", min_value=1, max_value=137,value=10)
file['produksi_kumulatif'] = file.groupby(['nama_negara'])['produksi'].transform('sum')
new_file = file.drop_duplicates(subset=['nama_negara'])
#Fitur tambahan berupa Tabel Pilihan 3
data_pilihan3=new_file.sort_values(by=['produksi_kumulatif'], ascending=False).head(count_country2)
data_tampil3=data_pilihan3.drop("tahun", inplace=False, axis=1).drop("produksi",inplace=False, axis=1).rename(columns={'nama_negara':"Country's name",'produksi_kumulatif':'Cumulative_Production'})
col1.write("Representation Table")
col1.write(data_tampil3)
#Fitur Wajib 3: Membuat Grafiknya
cmap_name = 'tab10'
cmap = cm.get_cmap(cmap_name)
colors = cmap.colors[:len(data_pilihan3)]
fig, ax = plt.subplots()
ax.barh(data_pilihan3['nama_negara'] ,data_pilihan3['produksi_kumulatif'],color=colors)
ax.set_yticklabels(data_pilihan3['nama_negara'], rotation=0)
ax.invert_yaxis() 
ax.set_title("Chart of Most Cumulative Production with Selected Number of Country", fontsize=14)
ax.set_ylabel("Country's name", fontsize=12)
ax.set_xlabel('Cumulative Production',fontsize=12)
col1.pyplot(fig)


#Fitur tambahan membuat trendline produksi minyak dari organisasi/non negara
col2.subheader("Trendline of Crude Oil Production from Selected Organization")
file3=pd.read_csv("produksi_minyak_mentah.csv")
list=file3['kode_negara'].drop_duplicates().values.tolist()
list_org=[]
list_lengkap=[]
for item in file2:
    list_lengkap.append(item['alpha-3'])
for kode in list:
    if kode not in list_lengkap:
        list_org.append(kode)
org = col2.selectbox("Select Organization", list_org)
#misal OEU / indeks 0 (dipilih interaktif oleh user)
filter=file3['kode_negara']==org
org=file3[filter]
#Tabel pilihan
n_tampil2 = col2.number_input("Pick How Many Rows You Want to Display in this Table Below", min_value=1, max_value=None, value=10)
col2.write("Representation Table")
data_tampil4=org.rename(columns={'kode_negara':"Organization's name",'tahun':'Year','produksi':'Production','produksi_kumulatif':'Cumulative_Production'}).head(n_tampil2)
col2.write(data_tampil4)
#Grafik
fig,ax=plt.subplots()
color='green'
ax.plot(org['tahun'] ,org['produksi'],color=color)
ax.set_title("Trendline of Selected Organization")
ax.set_ylabel("Production", fontsize=12)
ax.set_xlabel('Year',fontsize=12)
col2.pyplot(fig)

#Fitur Tambahan:Grafik yang menunjukan trendline jumlah produksi kumulatif dari seluruh negara di setiap tahun
col2.subheader("Trendline of Total Crude Oil Production from All Countries every Year")
file['Total_Production'] = file.groupby(['tahun'])['produksi'].transform('sum')
file_new = file.drop_duplicates(subset=['tahun']).drop(columns='nama_negara', axis=1).drop(columns='produksi_kumulatif', axis=1).drop(columns='produksi', axis=1).rename(columns={'tahun':'Year'})
col2.write(file_new)
#Grafik
cmap_name = 'tab20'
cmap = cm.get_cmap(cmap_name)
colors = cmap.colors[:len(file_new)]
fig, ax = plt.subplots()
color='green'
ax.plot(file_new['Year'] ,file_new['Total_Production'],color=color)
ax.set_title("Trendline of All Countries Production Vs Year")
ax.set_ylabel("Total Production", fontsize=12)
ax.set_xlabel('Year',fontsize=12)
col2.pyplot(fig)

max_year=file_new.sort_values(by=['Total_Production'], ascending=False).head(1)
min_year=file_new.sort_values(by=['Total_Production'], ascending=True).head(1)

#(3) nama lengkap negara, kode negara, region, dan sub-region dengan jumlah produksi sama dengan nol pada tahun T dan keseluruhan tahun.
#(3)
#Berdasarkan Tahun Inputan User (pada Tahun T)
col2.subheader("List of Countries with Zero Crude Oil Production")
year2=col2.number_input("Pick the Year", min_value=1971, max_value=2015)
filter1=file['produksi']==0
nol_data=file[filter1].sort_values(by=['produksi'])
filter2=nol_data['tahun']==year2
nol_pil=nol_data[filter2].sort_values(by=['produksi']).drop(columns='produksi_kumulatif', axis=1)
negara_nol_pil=nol_pil['nama_negara'].values.tolist()
list_kode=[]
list_region=[]
list_subregion=[]
for negara in negara_nol_pil:
    for item in file2:
        if (item['name'])==negara:
            kode=[(item['alpha-3'])]
            region=(item['region'])
            sub_region=(item['sub-region'])
            list_kode.append(kode)
            list_region.append(region)
            list_subregion.append(sub_region)
#Mengubah ke data frame agar mudah dibaca
nol_pil["Country's Code"]=list_kode
nol_pil["Region"]=list_region
nol_pil["Sub-Region"]=list_subregion
nol_pil=nol_pil.rename(columns={'nama_negara':"Country's name",'produksi':'Production','tahun':'Year'})
col2.write(nol_pil)

#Berdasarkan keseluruhan data (Lanjutan Fitur sebelumnya)
col2.subheader("List of Countries with Cumulative Zero Crude Oil Production all Years")
filter3=file['produksi_kumulatif']==0
nol_total=file[filter3].sort_values(by=['produksi_kumulatif']).drop(columns='produksi', axis=1).drop(columns='tahun',axis=1).drop_duplicates(subset=['nama_negara'])
negara_nol_total=nol_total['nama_negara'].values.tolist()
list_kode=[]
list_region=[]
list_subregion=[]
for negara in negara_nol_total:
    for item in file2:
        if (item['name'])==negara:
            kode=[(item['alpha-3'])]
            region=(item['region'])
            sub_region=(item['sub-region'])
            list_kode.append(kode)
            list_region.append(region)
            list_subregion.append(sub_region)
#Mengubah ke data frame agar mudah dibaca
nol_total["Country's Code"]=list_kode
nol_total["Region"]=list_region
nol_total["Sub-Region"]=list_subregion
nol_total=nol_total.rename(columns={'nama_negara':"Country's name",'produksi_kumulatif':'Cumulative_Production'})
col2.write(nol_total)


#Informasi yang menyebutkan: (1) nama lengkap negara, kode negara, region, dan sub-region dengan jumlah produksi terbesar pada tahun T dan keseluruhan tahun. 
#(1)
#Berdasarkan Tahun Inputan User (pada Tahun T)
col2.subheader("Summary")
filter=file['tahun']==year
max_pil=file[filter].sort_values(by=['produksi'], ascending=False).head(1)
prod=np.asarray(max_pil['produksi'])
negara_max_pil=np.asarray(max_pil['nama_negara'])
for item in file2:
    if (item['name'])==negara_max_pil:
        kode=[item['alpha-3']]
        region=[item['region']]
        sub_region=[item['sub-region']]
kode=np.asarray(kode)
region=np.asarray(region)
sub_region=np.asarray(sub_region)
col2.markdown(f"**Year with the Smallest Total Production is: ** [1983] with amount of production [2076524.432]")
col2.markdown(f"**Year with the Largest Total Production is : ** [2015] with amount of production [3934946.0]")
col2.markdown(f"**Country with the Largest Production in {year}: ** \n {negara_max_pil} with amount of production {prod}, code country: {kode}, region: {region}, sub-region: {sub_region}")

#Berdasarkan Keseluruhan Tahun
max_total=file.sort_values(by=['produksi_kumulatif'], ascending=False).head(1)
prod=np.asarray(max_total['produksi_kumulatif'])
negara_max_total=np.asarray(max_total['nama_negara'])
for item in file2:
    if (item['name'])==negara_max_total:
        kode=[item['alpha-3']]
        region=[item['region']]
        sub_region=[item['sub-region']]
kode=np.asarray(kode)
region=np.asarray(region)
sub_region=np.asarray(sub_region)
col2.markdown(f"**Country with the Largest Cumulative Production in all Years: ** \n {negara_max_total} with amount of production {prod}, code country: {kode}, region: {region}, sub-region: {sub_region}")

#(2) nama lengkap negara, kode negara, region, dan sub-region dengan jumlah produksi terkecil (tidak sama dengan nol) pada tahun T dan keseluruhan tahun.
#(2)
#Berdasarkan Tahun Inputan User (pada Tahun T)
filter1=file['produksi']!=0
min_data=file[filter1].sort_values(by=['produksi'], ascending=True)
filter2=min_data['tahun']==year
min_pil=min_data[filter2].sort_values(by=['produksi'], ascending=True).head(1)
prod=np.asarray(min_pil['produksi'])
negara_min_pil=np.asarray(min_pil['nama_negara'])
for item in file2:
    if (item['name'])==negara_min_pil:
        kode=[item['alpha-3']]
        region=[item['region']]
        sub_region=[item['sub-region']]
kode=np.asarray(kode)
region=np.asarray(region)
sub_region=np.asarray(sub_region)
col2.markdown(f"**Country with the Smallest Production in {year}: ** \n {negara_min_pil} with amount of production {prod}, code country: {kode}, region: {region}, sub-region: {sub_region}")

#Berdasarkan Keseluruhan Tahun
filter3=file['produksi_kumulatif']!=0
min_total=file[filter3].sort_values(by=['produksi_kumulatif'], ascending=True).head(1)
prod=np.asarray(min_total['produksi_kumulatif'])
negara_min_total=np.asarray(min_total['nama_negara'])
for item in file2:
    if (item['name'])==negara_min_total:
        kode=[item['alpha-3']]
        region=[item['region']]
        sub_region=[item['sub-region']]
kode=np.asarray(kode)
region=np.asarray(region)
sub_region=np.asarray(sub_region)
col2.markdown(f"**Country with the Smallest Cumulative Production in all Years: ** \n {negara_min_total} with amount of production {prod}, code country: {kode}, region: {region}, sub-region: {sub_region}")
