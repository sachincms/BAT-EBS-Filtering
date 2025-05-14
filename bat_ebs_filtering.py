import streamlit as st
from utils.db_loader import load_to_mongodb
from utils.retrieve_data import retrieve
from config import CONTENT_UNAVAILABLE_MESSAGE

documents, existing_ids = retrieve()

def display_documents(documents, relevant_list):
    st.title("Document Relevance")
    st.subheader("Select relevant documents")
    st.write(f"Total documents: {len(documents)}")

    already_displayed = []
    total_inserted_count = 0
    for idx, doc in enumerate(documents):
        if idx > 0 and idx % 50 == 0:
            if st.button("Count", key=f"{idx}_count_button"):
                st.write("Relevant list: ", relevant_list)
                relevant_documents = [doc for idx, doc in enumerate(documents) if idx in relevant_list]
                irrelevant_count = len(documents) - len(relevant_documents)
                st.write("Irrelevant documents: \n" , irrelevant_count)

            if st.button("Proceed", key=f"{idx}_proceed_button"):
                relevant_documents = [doc for idx, doc in enumerate(documents) if idx in relevant_list]
                non_duplicate_documents = [doc for doc in relevant_documents if doc['_id'] not in existing_ids]
                duplicate_document_count = len(relevant_documents) - len(non_duplicate_documents)
                load_to_mongodb(non_duplicate_documents)

                st.write(f"Selected documents: {len(relevant_documents)}")
                st.write(f"Inserted documents: {len(non_duplicate_documents)}")
                if duplicate_document_count > 0:
                    st.write(f"The remaining {duplicate_document_count} documents are duplicates.")

                total_inserted_count += len(non_duplicate_documents)
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
        non_duplicate_documents = [doc for doc in relevant_documents if doc['_id'] not in existing_ids]
        duplicate_document_count = len(relevant_documents) - len(non_duplicate_documents)
        load_to_mongodb(non_duplicate_documents)

        st.write(f"Selected documents: {len(relevant_documents)}")
        st.write(f"Inserted documents: {len(non_duplicate_documents)}")
        if duplicate_document_count > 0:
            st.write(f"The remaining {duplicate_document_count} documents are duplicates.")
        total_inserted_count += len(non_duplicate_documents)

        with st.container(border=True):
            st.header(f"Added a total of {len(total_inserted_count)} to the database. You may close the app now.")

relevant_list = []
display_documents(documents, relevant_list)