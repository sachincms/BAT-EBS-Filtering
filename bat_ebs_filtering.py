import streamlit as st
from utils.db_loader import load_to_mongodb
from utils.retrieve_data import retrieve, count_total_documents




PAGE_SIZE = 200

if "page" not in st.session_state:
    st.session_state["page"] = 0

if "relevant_indices" not in st.session_state:
    st.session_state["relevant_indices"] = set()

if "total_docs" not in st.session_state:
    st.session_state["total_docs"] = count_total_documents()

# total pages = number of documents / page size
total_pages = st.session_state["total_docs"] // PAGE_SIZE + (1 if st.session_state.total_docs % PAGE_SIZE else 0)

# number of documents to be skipped
# for first page = 0 since page number is 0
# for second page it will be 1 * page size
# for third page it will be 2 * page size
skip = st.session_state["page"]*PAGE_SIZE


documents = retrieve(skip = skip, limit = PAGE_SIZE)


st.title("Document Relevance")
st.subheader("Select relevant documents")

st.write(f"Total documents: {st.session_state["total_docs"]}")
st.write(f"Showing page: {st.session_state["page"] + 1} of {total_pages}")




already_displayed = []
total_inserted_count = 0
for idx, doc in enumerate(documents):

    # since every page will have same number of documents retrieved, the index will be same
    # hence we will use global index
    # global index = number of documets skipped + document index
    # first page index: 0-199                first page global index: 0-199
    # second page local index: 0-199         second page global index: 200-399
    global_idx = skip + idx

    key = doc['article_links']
    if key in already_displayed:
        continue
    already_displayed.append(key)
    checkbox = st.checkbox(label=f"{global_idx}: {doc['title']}", key=f"checkbox_{global_idx}")
    with st.expander(label="Text"):
        st.write(doc['text'])

    # only global indices will be appended to session state
    if checkbox:
        st.session_state["relevant_indices"].add(global_idx)


# Navigation
col1, col2 = st.columns([1, 1])
with col1:
    if st.button("Previous") and st.session_state.page > 0:
        st.session_state.page -= 1
        st.rerun()

with col2:
    if st.button("Next") and st.session_state.page < total_pages - 1:
        st.session_state.page += 1
        st.rerun()


# Count the number of relevant documents
if st.button("Count", key="count_button"):
    st.write(f"Relevant documents: {len(st.session_state["relevant_indices"])}")
    irrelevant_count = st.session_state["total_docs"] - len(st.session_state["relevant_indices"])
    st.write(f"Irrelevant documents: \n{irrelevant_count}")

st.divider()

if st.button("Proceed", key="proceed_button"):

    relevant_documents = []
    for idx in st.session_state["relevant_indices"]:

        # for index = 5, page num = 0
        # for index = 255, page num = 1.....
        page_num = idx//PAGE_SIZE

        # offset in page is nothing but the local index since we are using skip and limit
        # if global index = 252, local index = 52
        offset_in_page = idx%PAGE_SIZE
        page_docs = retrieve(skip = page_num*PAGE_SIZE, limit = PAGE_SIZE)

        if offset_in_page < len(page_docs):
            relevant_documents.append(page_docs[offset_in_page])

    load_to_mongodb(relevant_documents)

    st.write(f"Inserted {len(relevant_documents)} documents.")
    total_inserted_count += len(relevant_documents)

    with st.container(border=True):
        st.header(f"Added a total of {total_inserted_count} to the database. You may close the app now.")






