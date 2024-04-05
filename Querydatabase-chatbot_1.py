
# I am using this version of the openAI for this but preferably use the latest one
#pip install openai==0.28.0
#pip3 show openai

import streamlit as st
import pymysql
import openai
import pandas as pd

# OpenAI API key -- Use your Key here
###openai.api_key = 'YOUR KEY'

# Database connection settings
DB_HOST = 'ms.itversity.com'
DB_USER = 'retail_user'
DB_PASS = 'itversity'
DB_NAME = 'retail_db'


def get_db_connection():
    return pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASS, db=DB_NAME,
                           cursorclass=pymysql.cursors.DictCursor)


def query_database(query):
    connection = get_db_connection()
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
    return result

def extract_sql_query(response_text):
    # Simple approach: Extract SQL query from a known response pattern
    # This example assumes the SQL query is enclosed in a markdown code block (```sql)
    # Adjust the logic based on the actual format of your OpenAI response
    if '```sql' in response_text:
        start = response_text.find('```sql') + len('```sql\n')
        end = response_text.find('```', start)
        sql_query = response_text[start:end].strip()
        return sql_query
    return response_text  # Fallback to returning the full response if pattern not found






st.subheader('Database Query Interface')

user_query = st.text_area('Enter your query:', '')

if st.button('Submit'):
    # Using OpenAI to interpret the query (This is a placeholder; in a real app, you'd need to process the response to form a SQL query)
    try:
        # response = client.chat.completions.create(
        #           model="gpt-3.5-turbo",
        #           prompt="Translate this to SQL: {user_query}",
        #           temperature=0.3,
        #           max_tokens=150
        # )
        # sql_query = response.choices[0].text.strip()
        # st.text(f"Generated SQL Query: {sql_query}")
        # response = client.chat.completions.create(
        #     model="text-davinci-003",
        #     prompt=f"Translate this English sentence to an SQL query: '{user_query}'",
        #     temperature=0.3,
        #     max_tokens=64
        # ).choices[0].text.strip()
        # response = openai.ChatCompletion.create(
        #     model="gpt-3.5-turbo",
        #     messages=[
        #         {"role": "system", "content": "You are a helpful assistant."},
        #         {"role": "user", "content": f"Translate this English sentence to an SQL query: '{user_query}'"},
        #     ]
        # )
        #
        # sql_query = response.choices[0].message['content'].strip()
        # response = openai.completions.create(
        #     model="gpt-3.5-turbo",  # or "gpt-3.5-turbo" based on your preference and available models
        #     prompt=f"Translate this English sentence to an SQL query: '{user_query}'",
        #     temperature=0.3,
        #     max_tokens=64
        # )
        # # Extracting the text from the response
        # sql_query = response.choices[0].text.strip()
        # print(sql_query)
        response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = [
                {"role": "system", "content": "You are a helpful technical SQL assistant."},
                {"role": "user", "content": f"Translate this English sentence to an SQL query: '{user_query}'"}
            ]
        )

        sql_query = response.choices[0].message['content'].strip()
        print(sql_query)
        st.write(f"Interpreted SQL Query: {sql_query}")
        # Example usage
        sql_query = extract_sql_query(sql_query)
        print("Extracted SQL Query:", sql_query)
        # Now, use the extracted SQL query to interact with the database
        #query_result = query_database(sql_query)
        # Querying the database
        # WARNING: Directly using user input can lead to SQL injection. Always validate/parameterize inputs in a real application.
        results = query_database(sql_query)
        print(results)

        if results:
            st.write(results)
        else:
            st.write("No results found.")
        # Convert the data to a pandas DataFrame
        df = pd.DataFrame(results)
        # Title for your app
        st.subheader('Display Data in Tabular Format')

        # Display the DataFrame as a table
        st.write(df)
    except Exception as e:
        st.error(f"An error occurred: {e}")

#select all records from the 'departments' table in 'retail_db' database.
#select Product_ID, Product_Name, Quantity_Sold, Vendor_ID, Sale_Date, sum(Sale_Amount) as Total_Sale_amount, Sale_Currency, Vendor_Name, sum(Amount_USD) as Total_USD_amount   from the 'SalesdataReady_poc' table in 'retail_export' database.
#select Product_ID, Product_Name, Quantity_Sold, Vendor_ID, Sale_Date, sum(Sale_Amount) as Total_Sale_amount, Sale_Currency, Vendor_Name, sum(Amount_USD) as Total_USD_amount   from the 'SalesdataReady_poc' table in 'retail_export' database. Use the relevent group by clause
#Select data for this requirement
#Table : SalesdataReady_poc
#database : retail_export
#Columns : Product_ID, Product_Name, Quantity_Sold, Vendor_ID, Sale_Date, sum(Sale_Amount) as Total_Sale_amount, Sale_Currency, Vendor_Name, sum(Amount_USD) as Total_USD_amount
#Use the  relevent group by clause
#tell me the topt 10 product_name  from products by product_price