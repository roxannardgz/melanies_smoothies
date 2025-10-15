# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title(f"Customize your Smoothie :cup_with_straw:")
st.write(
  """Choose your favorite combination of fruits for the perfect smoothie! 🥭🍍🫐🍌
  """
)


name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be: ', name_on_order)


cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

# Multiselect for the user to select up to 5 ingredients for the smoothie
ingredients_list = st.multiselect(
    'Chose up to 5 ingredients:'
    , my_dataframe
    , max_selections=5
)

# Add order to database
if ingredients_list:
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        st.subheader(fruit_chose + 'Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """', '"""+name_on_order+"""')"""

    st.write(my_insert_stmt)

    # Button to insert into table in db
    time_to_insert = st.button('Submit order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="😬")




