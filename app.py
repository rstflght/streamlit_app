import yfinance as yf
import streamlit as st
from datetime import datetime, timedelta



def main():
    ticker = "AAPL"
    half_year = datetime.date(datetime.now() - timedelta(days=182))
    tickerData = yf.Ticker(ticker)

    st.set_page_config(layout="wide")
    st.write("## Данные о биржевых котировках компании APPLE")
    # default states


    with st.sidebar:
        with st.form("graph1"):
            st.write("Выберете для графика №1:")
            # Period for figure 1
            start_date_one = st.date_input("Начало периода", value=half_year)
            end_day_one = st.date_input("Конец периода")

            # Multichoise indicators for figure 1      
            indicator_one = tickerData.history().columns[:5]
            selection_one = st.pills("Показатели", options=indicator_one, default=indicator_one[0], selection_mode="multi")
            choise_one = ", ".join(selection_one)

            # Submit changes
            st.form_submit_button("Применить")

        with st.form("graph2"):
            st.write("Выберете для графика №2:")
            # Period for figure 2
            start_date_two = st.date_input("Начало периода", value=half_year)
            end_day_two = st.date_input("Конец периода")
            
            # Multichoise indicators for figure 2
            indicator_two = tickerData.history().columns[:5]
            selection_two = st.pills("Показатели", options=indicator_two, default=indicator_two[1], selection_mode="multi")
            choise_two = ", ".join(selection_two)
            
            # Submit changes
            st.form_submit_button("Применить")



    with st.container(border=True):
        tickerDf_first = tickerData.history(period='1d', start=start_date_one, end=end_day_one)
        st.write("## График №1: ", choise_one)
        st.write(f"С {start_date_one} по {end_day_one}")
        st.line_chart(tickerDf_first[selection_one])

        st.download_button(label="Сохранить данные графика",
                           data=tickerDf_first[selection_one].to_csv().encode("utf-8"),
                           file_name="Data_figure1.csv",
                           mime="text/csv")
        
    with st.container(border=True):
        tickerDf_second = tickerData.history(period='1d', start=start_date_two, end=end_day_two)
        st.write("## График №2: ", choise_two)
        st.write(f"С {start_date_two} по {end_day_two}")
        st.line_chart(tickerDf_second[selection_two])

        st.download_button(label="Сохранить данные графика",
                           data=tickerDf_second[selection_two].to_csv().encode("utf-8"),
                           file_name="Data_figure2.csv",
                           mime="text/csv")





if __name__ == "__main__":
    main()