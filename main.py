import streamlit as st
import functions
from datetime import datetime
from config import CATEGORIES, WRITE_INTERVAL
from styles import MOBILE_STYLES


# Set the page title, icon, and layout
st.set_page_config(page_title="Grocery List", page_icon="🛒", layout="wide")

# Add an anchor point at the top
st.markdown('<div id="top" style="position: relative; \
            top: -100px; margin-bottom: 100px;"></div>',
            unsafe_allow_html=True)


# Initialize data on app start
grocery_list = functions.get_list()
groceries = functions.get_groceries()
added_groceries = []
categories_col1, categories_col2, categories_col3 = \
    functions.split_categories(groceries)

# Track last write time
if 'last_write_time' not in st.session_state:
    st.session_state['last_write_time'] = datetime.now()

# Write the grocery list to the database every 5 minutes
if (datetime.now() - st.session_state['last_write_time']).seconds > \
        WRITE_INTERVAL:
    functions.write_list(grocery_list)
    functions.write_groceries(groceries)
    st.session_state['last_write_time'] = datetime.now()


def add_groceries() -> None:
    """
    Add grocery items to the grocery list.

    Arguments:
        added_groceries -- The list of added groceries
        grocery_list -- The grocery list
        session_state -- The Streamlit session state
    """
    for grocery in added_groceries:
        if grocery not in grocery_list:
            grocery_list.append(grocery.title())

    functions.clear_session_state(st.session_state, added_groceries)
    added_groceries.clear()


def remove_groceries() -> None:
    """
    Update the groceries dictionary by removing the added groceries.
    """
    global groceries
    groceries = functions.remove_groceries(groceries, added_groceries)


# Expander to show the default grocery list and add items to the current list
with st.expander(label="Add grocery item"):
    # Drop-down menu to select the category
    cat = st.selectbox("Select category", (CATEGORIES),
                       index=None, key="category",
                       placeholder="Select category")

    # Text input to add a new grocery item
    new_grocery_input = st.text_input(label=" ",
                                      placeholder="Add to standard grocery list",  # noqa
                                      key="tmp_grocery",
                                      on_change=functions.process_grocery_input(st.session_state, groceries))  # noqa

    # Check if a category has been selected
    if new_grocery_input:
        if cat not in CATEGORIES:
            st.error("Please select a category")
            st.stop()
        groceries = functions.add_default_groceries(cat,
                                                    st.session_state,
                                                    groceries)
        st.rerun()

    # Links to navigate the categories
    index_links = " | ".join([
        f"[{category}](#{functions.clean_category_name(category)})"
        for category in CATEGORIES])
    st.markdown(index_links)

    # Add custom CSS for mobile-friendly layout
    st.markdown(MOBILE_STYLES, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        # Show the first third of the default grocery list with checkboxes
        for category in categories_col1:
            functions.display_grocery_category(
                category, groceries, added_groceries)

    with col2:
        # Show the second third of the default grocery list with checkboxes
        for category in categories_col2:
            functions.display_grocery_category(
                category, groceries, added_groceries)

    with col3:
        # Show the last third of the default grocery list with checkboxes
        for category in categories_col3:
            functions.display_grocery_category(
                category, groceries, added_groceries)

    col4, col5 = st.columns([0.01, 0.01])
    with col4:
        st.button(label="Add to list", key="add_button",
                  on_click=add_groceries, use_container_width=False)
    with col5:
        st.button(label="Remove from standard list", key="remove_button",
                  on_click=remove_groceries, use_container_width=False)

# Display the grocery list
st.title("Groceries")

for grocery in grocery_list:
    checkbox = st.checkbox(grocery, key=grocery)
    if checkbox:
        grocery_list.remove(grocery)
        del st.session_state[grocery]
        st.rerun()
