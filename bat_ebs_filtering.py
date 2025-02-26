import streamlit as st
from datetime import datetime
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from config import MONGODB_URI, MONGODB_DATABASE, MONGODB_SCRAPED_COLLECTION, MONGODB_PROCESSED_COLLECTION

client = MongoClient(MONGODB_URI, server_api=ServerApi('1'))
db = client[MONGODB_DATABASE]
scraped_collection = db[MONGODB_SCRAPED_COLLECTION]
processed_collection = db[MONGODB_PROCESSED_COLLECTION]

start_date = datetime.strptime('25/02/2025 00:00:00.0', '%d/%m/%Y %H:%M:%S.%f')
end_date = datetime.today()

query = {
    'scraped_date': {
        '$gte': start_date,
        '$lte': end_date
    }
}
documents = scraped_collection.find(query)
documents = list(documents)

def display_documents(documents, relevant_list):
    st.title("Document Relevance")
    st.subheader("Select relevant documents")

    already_displayed = []
    for idx, doc in enumerate(documents):
        if doc['scraped_from'] == 'Bangalore Mirror':
            continue
        if idx > 0 and idx % 50 == 0:
            if st.button("Count", key=f"{idx}_count_button"):
                st.write("Relevant list: ", relevant_list)
                relevant_documents = [doc for idx, doc in enumerate(documents) if idx in relevant_list]
                irrelevant_count = len(documents) - len(relevant_documents)
                st.write("Irrelevant documents: \n" , irrelevant_count)

            if st.button("Proceed", key=f"{idx}_proceed_button"):
                relevant_documents = [doc for idx, doc in enumerate(documents) if idx in relevant_list]
                for doc in relevant_documents:

                    try:
                        existing_doc = processed_collection.find_one({'_id': doc['_id']})
                        if existing_doc is None:
                            processed_collection.insert_one(doc)
                    except Exception as ex:
                        print(ex)
                        continue
                st.write(f"Inserted {len(relevant_documents)} relevant documents")
                relevant_list = []
            
            st.divider()

        key = doc['title'] if doc['title'] != 'Content Unavailable' else ''
        if key in already_displayed:
            continue
        already_displayed.append(key)
        checkbox = st.checkbox(label=f"{idx}: {doc['title']}", key=f"checkbox_{idx}")
        with st.expander(label="Text"):
            st.write(doc['text'])
        if checkbox:
            relevant_list.append(idx)
    
    if st.button("Count", key="final_count_button"):

        st.write("Relevant list: ", relevant_list)

        relevant_documents = [doc for idx, doc in enumerate(documents) if idx in relevant_list]

        irrelevant_count = len(documents) - len(relevant_documents)
        st.write("Irrelevant documents: \n" , irrelevant_count)
    
    st.divider()

    if st.button("Proceed", key="final_proceed_button"):
        relevant_documents = [doc for idx, doc in enumerate(documents) if idx in relevant_list]
        for doc in relevant_documents:
            existing_doc = processed_collection.find_one({'_id': doc['_id']})
            if existing_doc is None:
                processed_collection.insert_one(doc)
        with st.container(border=True):
            st.header(f"Added {len(relevant_documents)} to the database. You may close the app now.")

relevant_list = []
display_documents(documents, relevant_list)