# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f"Zena's Amazing Athleisure catalog")


# Get the current credentials
session = get_active_session()

my_dataframe = session.table("zenas_athleisure_db.products.catalog_for_website").select(col('COLOR_OR_STYLE'))

choose_color = st.selectbox("Pick as sweatsuit color or style",my_dataframe)
#st.write(my_dataframe)

selected_image = session.table("zenas_athleisure_db.products.catalog_for_website")\
    .filter(col('COLOR_OR_STYLE')==choose_color)\
    .select(col('FILE_URL')  ).collect()
st.image(selected_image[0],width=400,caption="Our warm, comfortable, "+choose_color+ " sweatsuit!",use_container_width=True)


price_sweatsuit = session.table("zenas_athleisure_db.products.catalog_for_website")\
    .filter(col('COLOR_OR_STYLE')==choose_color)\
    .select(col('PRICE'),col('SIZE_LIST'),col('UPSELL_PRODUCT_DESC')  ).collect()
 
price = price_sweatsuit[0]['PRICE']
size_list= price_sweatsuit[0]['SIZE_LIST']
bonus = price_sweatsuit[0]['UPSELL_PRODUCT_DESC']

st.write("Price:",price)
st.write("Sizes Available:",size_list)
st.write(bonus.replace("Consider: ","Also Consider: "))
