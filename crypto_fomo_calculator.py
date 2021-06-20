"""
Author  : Maheshh Balwan
Website : maheshhbalwan.com
Github  : maheshhbalwan.github.io
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pycoingecko import CoinGeckoAPI
from datetime import datetime, timedelta
cg = CoinGeckoAPI()

st.image('data/crypto_coins_image.png', use_column_width=True)

st.write("""
# Crypto FOMO Calculator
Steps to calculate the amount you might have gained by investing in crypto at an earlier date.

- Select Crypto Currency you wish you would've bought
- Select Date you wish you would have bought the selected crypto currency
- Select the Currency type of your choice
- Select Amount you wish you would have invested
""")
st.write('---')

# select Crypto Currency
st.write('''## Choose Crypto Currency''')
selected_crypto_currency = st.radio('Select Crypto Currency', ['bitcoin','dogecoin','ethereum','binancecoin','tether','cardano','litecoin','shiba-inu','wazirx'])
st.write('You have selected',selected_crypto_currency)
id=selected_crypto_currency

# - Date you wish you would have bought the selected crypto currency
st.write('''## Choose Date and Amount''')
today = datetime.utcnow().date()
previous_day = today - timedelta(days=1)
selected_historical_date = st.date_input("Date: ", value=previous_day, min_value=datetime(2015,1,1), max_value=previous_day)
st.write('You have selected',selected_historical_date)

# Select the Currency type of your choice
st.write('''## Choose Currency Type''')
selected_currency_type = st.selectbox('Select Currency Type', ['usd'])

# Amount you wish you would have invested
selected_amount = st.number_input(selected_currency_type +" Amount: ", min_value=1, max_value=999999999)

#Load Data
crypto_current = cg.get_price(id, vs_currencies=selected_currency_type)[id][selected_currency_type]

#Reformat Historical Date for next function
selected_historical_date_reformat = selected_historical_date.strftime("%d-%m-%Y")
selected_historical_date_datetime = datetime.strptime(selected_historical_date_reformat,"%d-%m-%Y")
selected_crypto_currency_historic = cg.get_coin_history_by_id(id, vs_currencies=selected_currency_type, date=selected_historical_date_reformat)['market_data']['current_price'][selected_currency_type]
selected_crypto_currency_historic = round(selected_crypto_currency_historic, 5)

# Display Results - Historical Value
st.write('''# Results''')
st.write('''## Historic Analysis''')

if selected_crypto_currency_historic == 0:
    st.write("You would have original bought: 0",selected_crypto_currency)
else:
    st.write("You would have original bought: ", round((selected_amount/selected_crypto_currency_historic),5),selected_crypto_currency)

st.write("At a price of $", selected_crypto_currency_historic,' per',selected_crypto_currency)

# Display Results - Present Value
st.write('''## Present Effects''')
if selected_crypto_currency_historic == 0:
    total_coins = 0
else:
    total_coins = selected_amount/selected_crypto_currency_historic

current_selected_currency_type = total_coins * crypto_current
perc_change = (current_selected_currency_type - selected_amount)/(selected_amount)*100
selected_currency_type_diff = current_selected_currency_type - selected_amount

st.write("That is currently worth: $", round(current_selected_currency_type,2))
st.write("Which is a percentage change of ", round(perc_change, 2), "%")

if selected_currency_type_diff == 0:
   st.write('''# You Broke Even''')
elif selected_currency_type_diff <= 0:
   st.write('''# You Would Have Lost''')
else:
   st.write('''# You Missed Out On''') 
st.write('$', abs(round(selected_currency_type_diff,2)),"!!!")

now = datetime.now()
historical_prices = cg.get_coin_market_chart_range_by_id(id, vs_currency=selected_currency_type, from_timestamp=selected_historical_date_datetime.timestamp(), to_timestamp=now.timestamp())['prices']

dates = []
prices = []

for x,y in historical_prices:
  dates.append(x)
  prices.append(y)

dictionary = {"Prices":prices, "Dates":dates}
df = pd.DataFrame(dictionary)
df['Dates'] = pd.to_datetime(df['Dates'],unit='ms',origin='unix')

st.line_chart(df.rename(columns={"Dates":"index"}).set_index("index"))


st.write("Project Code - https://github.com/maheshhbalwan/crypto-fomo-calculator ")
# Command Line to run the file
# streamlit run your_script_location.py
# Find the project code on https://github.com/maheshhbalwan
