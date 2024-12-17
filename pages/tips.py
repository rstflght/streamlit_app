import streamlit as st
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import plotly.express as px


st.set_page_config(layout="wide")
with st.container(border=True):
    st.title("Исследование датасета Tips")

    tips = st.sidebar.file_uploader('Загрузи CSV файл', type='csv')
    with st.container(border=True):
        if tips is not None:
            st.success('##### Датасет успешно загружен!', icon="✅")
            #st.balloons()
            df = pd.read_csv(tips)
            st.table(df.head(5))
            
        else:
            st.stop()

    with st.container(border=True):
        st.success("##### Создаем столбец time_order заполняем его случайной датой в промежутке от 2023-01-01 до 2023-01-31")
        df["time_order"] = [pd.to_datetime("2023-01-"+ str(x)) for x in np.random.randint(1, 32, 244)]
        st.table(df.sample(3))

    with st.container(border=True):
        st.success("##### График показывающий динамику чаевых во времени")
        tips_time = df.groupby("time_order").agg({"tip": "sum"})
        tips_time.reset_index(inplace=True)
        tips_time.index += 1
        fig = px.line(tips_time["tip"]).update_layout(xaxis_title="Day", yaxis_title="Tip")
        st.plotly_chart(fig)
        
        st.divider()
        st.success("##### Аналогичный предыдущему график scatter")
        fig = px.scatter(tips_time, y="tip").update_layout(xaxis_title="Day", yaxis_title="Tip")
        st.plotly_chart(fig)

    with st.container(border=True):
        st.success("##### Гистограмма total_bill")
        fig = px.histogram(df, x="total_bill").update_layout(xaxis_title="Total bill", yaxis_title="Count")
        st.plotly_chart(fig)

    with st.container(border=True):
        st.success("##### Scatterplot, показывающий связь между total_bill и tip")
        fig = px.scatter(df, x="total_bill", y="tip").update_layout(xaxis_title="Total bill", yaxis_title="Tip")
        st.plotly_chart(fig)

    with st.container(border=True):
        st.success("##### График, связывающий total_bill, tip, и size")
        fig = px.scatter(df, x="total_bill", y="tip", color="size").update_layout(xaxis_title="Total bill", yaxis_title="Tip")
        st.plotly_chart(fig)
    
    with st.container(border=True):
        st.success("##### Связь между днем недели и размером счета")
        dow_bill = df.groupby(df["time_order"].dt.day_name())["total_bill"].mean()
        dow_bill = dow_bill.reindex(['Monday', 'Tuesday','Thursday','Wednesday','Friday','Saturday','Sunday'])
        fig = px.line(dow_bill).update_layout(xaxis_title="Day of week", yaxis_title="Total bill mean")
        st.plotly_chart(fig)

    with st.container(border=True):
        st.success("##### Scatter plot с днем недели по оси Y, чаевыми по оси X, и цветом по полу")
        dow_tip_sex = df.groupby(by=[df["time_order"].dt.day_name(), "sex"])["tip"].mean().reset_index()
        fig = px.scatter(dow_tip_sex, y="time_order", x="tip", color="sex").update_layout(yaxis_title="Day of week", xaxis_title="Tip mean")
        st.plotly_chart(fig)

    with st.container(border=True):
        st.success("##### Box plot c суммой всех счетов за каждый день, разбивая по time (Dinner/Lunch)")
        fig = px.box(df, y="total_bill", x="time").update_layout(yaxis_title="Total bill", xaxis_title="Time")
        st.plotly_chart(fig)

        st.divider()
        st.success("##### Violin plot c суммой всех счетов за каждый день, разбивая по time (Dinner/Lunch)")
        fig = px.violin(df, x="total_bill", y="time", color="time").update_layout(xaxis_title="Total bill", yaxis_title="Time")
        st.plotly_chart(fig)

    with st.container(border=True):
        st.success("##### Гистограммы чаевых на обед и ланч.")
        col1, col2 = st.columns(2)
        with col1:
            st.info("Dinner")

            dinner = df[df["time"] == "Dinner"]
            fig = px.histogram(dinner, x="tip", color="time").update_layout(yaxis_title="Count", xaxis_title="Tip")
            st.plotly_chart(fig)

        with col2:
            st.info("Lunch")
            dinner = df[df["time"] == "Lunch"]
            fig = px.histogram(dinner, x="tip", color="time").update_layout(yaxis_title="Count", xaxis_title="Tip")
            st.plotly_chart(fig)

    with st.container(border=True):
        st.success("##### Scatterplots связи пола, размера счета и чаевых, дополнительно по курящим/некурящим")
        col1, col2 = st.columns(2)
        with col1:
            st.info("Female")

            sex = df[df["sex"] == "Female"]
            fig = px.scatter(sex, x="total_bill", y="tip", color="smoker").update_layout(xaxis_title="Total bill", yaxis_title="Tip")
            st.plotly_chart(fig)

        with col2:
            st.info("Male")
            sex = df[df["sex"] == "Male"]
            fig = px.scatter(sex, x="total_bill", y="tip", color="smoker").update_layout(xaxis_title="Total bill", yaxis_title="Tip")
            st.plotly_chart(fig)

    with st.container(height=500, border=True):
        st.success("##### Тепловая карта зависимостей численных переменных")
        tips_mat = df.copy()
        tips_mat["sex"] = tips_mat["sex"].apply(lambda x : 1 if x=="Male" else 0)
        tips_mat["time"] = tips_mat["time"].apply(lambda x : 1 if x=="Dinner" else 0)
        tips_mat["smoker"] = tips_mat["smoker"].apply(lambda x : 1 if x=="Yes" else 0)
        tips_corr = tips_mat[["total_bill", "tip", "sex", "smoker", "time", "size"]].corr()
        fig = px.imshow(tips_corr, text_auto=True, aspect="auto")
        st.plotly_chart(fig)