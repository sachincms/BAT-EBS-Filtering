import streamlit as st
from utils.db_loader import load_to_mongodb
from utils.retrieve_data import retrieve

documents = retrieve()

def display_documents(documents, relevant_list):
    st.title("Document Relevance")
    st.subheader("Select relevant documents")
    st.write(f"Total documents: {len(documents)}")

    already_displayed = []
    total_inserted_count = 0
    for idx, doc in enumerate(documents):

        key = doc['article_links']
        if key in already_displayed:
            continue
        already_displayed.append(key)
        checkbox = st.checkbox(label=f"{idx}: {doc['title']}", key=f"checkbox_{idx}")
        with st.expander(label="Text"):
            st.write(doc['text'])
        if checkbox:
            relevant_list.append(idx)
    
    if st.button("Count", key="count_button"):

        st.write("Relevant list: ", relevant_list)

        relevant_documents = [doc for idx, doc in enumerate(documents) if idx in relevant_list]

        st.write(f"Relevant documents: {len(relevant_documents)}")
        irrelevant_count = len(documents) - len(relevant_documents)
        st.write(f"Irrelevant documents: \n{irrelevant_count}")
    
    st.divider()

    if st.button("Proceed", key="proceed_button"):
        relevant_documents = [doc for idx, doc in enumerate(documents) if idx in relevant_list]
        load_to_mongodb(relevant_documents)

        st.write(f"Inserted {len(relevant_documents)} documents.")
        total_inserted_count += len(relevant_documents)

        with st.container(border=True):
            st.header(f"Added a total of {len(total_inserted_count)} to the database. You may close the app now.")

relevant_list = []
display_documents(documents, relevant_list)