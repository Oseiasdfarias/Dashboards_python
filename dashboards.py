import pandas as pd
import streamlit as st
import plotly.express as px


st.set_page_config(page_title="Dashboard Finanças", layout="wide",
                   page_icon="🧊", initial_sidebar_state="expanded")

df = pd.read_csv("supermarket_sales.csv", sep=";", decimal=",")
df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values(by="Date")

df["Month"] = df["Date"].apply(lambda time: f"{time.year}-{time.month}")

month = st.sidebar.selectbox("Mês", df["Month"].unique())

df_filtered = df[df["Month"] == month]

st.title("Dashboard Faturamento")

# Criando a estrutura do Dashboards
col1, col2 = st.columns(2)
col3, col4, col5 = st.columns(3)

# Faturamento por Dia
fig_date = px.bar(df_filtered, x="Date", y="Total",
                  title="Faturamento por Dia", color="City")
col1.plotly_chart(fig_date, use_container_width=True)

# Faturamento por tipo de produto
fig_products = px.bar(df_filtered, x="Date", y="Product line",
                      title="Faturamento por tipo de produto", color="City",
                      orientation="h")
col2.plotly_chart(fig_products, use_container_width=True)

# Faturamento por filial
city_total = df_filtered.groupby("City")[["Total"]].sum().reset_index()
fig_city = px.bar(city_total, x="City", y="Total",
                  title="Faturamento por filial")
col3.plotly_chart(fig_city, use_container_width=True)

# Faturamento por tipo de pagamento
fig_kind = px.pie(df_filtered, values="Total", names="Payment",
                  title="Faturamento por tipo de pagamento")
col4.plotly_chart(fig_kind, use_container_width=True)

# Avaliação
city_total = df_filtered.groupby("City")[["Rating"]].mean().reset_index()
fig_rating = px.bar(df_filtered, y="Rating", x="City", title="Avaliação")
col5.plotly_chart(fig_rating, use_container_width=True)
