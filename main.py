import streamlit as st
import functions
from typing import Literal
from datetime import datetime
from logger_config import get_logger
from config import CATEGORIES
from styles import MOBILE_STYLES

logger = get_logger(__name__)


# Set the page title, icon, and layout
st.set_page_config(page_title="Grocery List", page_icon="🛒", layout="wide")

# Add an anchor point at the top
st.markdown('<div id="top" style="position: relative; \
            top: -100px; margin-bottom: 100px;"></div>',
            unsafe_allow_html=True)


# Initialize data on app start
if "grocery_list" not in st.session_state:
    st.session_state["grocery_list"] = functions.get_list()
if "groceries" not in st.session_state:
    st.session_state["groceries"] = functions.get_groceries()
if "added_groceries" not in st.session_state:
    st.session_state["added_groceries"] = []
categories_col1, categories_col2, categories_col3 = \
    functions.split_categories(st.session_state["groceries"])

# Track last write time
if "last_write_time" not in st.session_state:
    st.session_state["last_write_time"] = datetime.now()


def update_groceries(mode: Literal["list", "groceries"],
                     remove: bool,
                     item: str | None = None) -> None:
    """
    Update the grocery list or groceries dictionary based on the mode.

    Arguments:
        mode -- The mode of update, either "list" or "groceries"
        remove -- Whether to remove the added groceries

    Keyword Arguments:
        item -- The item to remove from the list, default = None

    Returns:
        None
    """
    try:
        grocery_list = st.session_state["grocery_list"]
        added_groceries = st.session_state["added_groceries"]

        if mode == "list":
            if remove:
                st.session_state["grocery_list"].remove(item)
                functions.background_write_list()
            else:
                for grocery in added_groceries:
                    if grocery not in grocery_list:
                        st.session_state["grocery_list"].append(
                            grocery.title())
                functions.background_write_list()
                functions.clear_session_state()
                st.session_state["added_groceries"].clear()

        elif mode == "groceries":
            if remove:
                functions.remove_groceries()
                functions.background_write_groceries()
            else:
                functions.process_grocery_input()
                functions.background_write_groceries()

    except Exception as e:
        logger.error(f"Error in update_groceries: {e}")
        st.error(f"Error in update_groceries: {str(e)}")


# Expander to show the default grocery list and add items to the current list
with st.expander(label="Add grocery item"):
    # Drop-down menu to select the category
    category = st.selectbox("Select category",
                            (CATEGORIES),
                            index=None,
                            key="category",
                            placeholder="Select category")

    # Text input to add a new grocery item
    new_grocery_input = st.text_input(label=" ",
                                      placeholder="Add to standard grocery list",  # noqa
                                      key="tmp_grocery",
                                      on_change=update_groceries,
                                      args=("groceries", False))  # noqa

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
            functions.display_grocery_category(category)

    with col2:
        # Show the second third of the default grocery list with checkboxes
        for category in categories_col2:
            functions.display_grocery_category(category)

    with col3:
        # Show the last third of the default grocery list with checkboxes
        for category in categories_col3:
            functions.display_grocery_category(category)

    col4, col5 = st.columns([0.01, 0.01])
    with col4:
        st.button(label="Add to list", key="add_button",
                  on_click=update_groceries,
                  args=("list", False), use_container_width=False)
    with col5:
        st.button(label="Remove from standard list", key="remove_button",
                  on_click=update_groceries,
                  args=("groceries", True), use_container_width=False)

# Display the grocery list
st.title("Groceries")

for grocery in st.session_state["grocery_list"]:
    checkbox = st.checkbox(grocery, key=grocery)
    if checkbox:
        update_groceries("list", True, grocery)
