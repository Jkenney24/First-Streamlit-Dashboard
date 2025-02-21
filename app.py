#----------Import Packages----------#
import pandas as pd 
import streamlit as st 
import plotly.express as px

#set page layout
st.set_page_config(layout='wide')

#----------Import Data----------#
#import data
df = pd.read_csv(r'restaurant_sales.csv')


#----------Initial Data Wrangling----------#
#transform order date to a datetime
df["order_date"] = pd.to_datetime(df["order_date"])

#date truncing to the month for comparisons and create as new column
df["order_month"] = df["order_date"].dt.to_period('M').dt.to_timestamp().dt.date



#----------Create Streamlit App----------#

#create a title
col1, col2= st.columns([1,.25])
col1.title('Restaurant Sales Dashboard')
st.divider()

#-----Data Selector-----#
#grab unique months
months=df["order_month"].unique()

#Add in columns for formatting
_, _, col3 = st.columns([1,1,.5])

#Assign selected month to a variable
month_selected=col2.selectbox('Select Month', months)

#-----Data Filtering-----#
#filter data based on selected month
selected_month_df=df[df["order_month"]==month_selected]


#create dataframe with summed sales and count of orders
df_summed=selected_month_df.groupby("order_month").agg({'price': "sum", 'order_id': 'nunique'}).reset_index()
df_summed['AOV']=round(df_summed['price']/df_summed['order_id'],2)

#-----Metrics-----#
#create subheader and columns
st.subheader('Main Metrics', divider='blue')

#Create a container to add a border
with st.container(border=True):
    #Creating columns
    Col1, Col2, Col3=st.columns(3)
    # metrics showing: total sales, total orders, average order value
    Col1.metric('Total Revenue', "${:,.0f}".format(df_summed['price'].values[0]))
    Col2.metric('Total Orders', "{:,.0f}".format(df_summed['order_id'].values[0]))
    Col3.metric('Average Order Value', "${:,.2f}".format(df_summed['AOV'].values[0]))

st.header("") #For Spacing

#-----Metrics-----#
#create subheader and tabs
st.subheader('Graphs')

Tab1, Tab2 = st.tabs(['Category Revenue', 'Item Revenue'])

#sum sales by month and category and build tab1 bar graphs
df_by_category=selected_month_df.groupby("category")['price'].sum().reset_index()
with Tab1:
    fig= px.bar(df_by_category, x='category', y='price', title='Catergory Revenue')
    st.plotly_chart(fig, use_container_width=True)
    
#sum sales by month and item_name and build tab2 bar graphs
df_by_item= selected_month_df.groupby("item_name")['price'].sum().reset_index()
with Tab2:
    fig2= px.bar(df_by_item, x='item_name', y='price', title='Item Revenue')
    st.plotly_chart(fig2, use_container_width=True)
