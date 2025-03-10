import logging
import streamlit as st
from supabase import create_client
from config import CATEGORIES, SUPABASE_DEFAULT_TABLE, SUPABASE_GROCERY_TABLE

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Supabase client
supabase_url = st.secrets["SUPABASE_URL"]
supabase_key = st.secrets["SUPABASE_KEY"]
supabase = create_client(supabase_url, supabase_key)


def better_title(text: str) -> str:
    """
    Custom title function that properly handles apostrophes.

    Arguments:
        text -- The text to be formatted

    Returns:
        str: The formatted text

    Example:
        >>> better_title("sam's club")
        "Sam's Club"
    """
    exceptions = ["'s", "'t", "'ll", "'re", "'ve", "'m", "'d"]
    words = text.title().split()

    for i, word in enumerate(words):
        for exception in exceptions:
            if exception.title() in word:
                words[i] = word.replace(exception.title(), exception)

    return " ".join(words)

# Core File Operation Functions


def get_list() -> list[str]:
    """
    Retrieve the grocery list from Supabase.

    Returns:
        list[str]: A list of grocery items with proper title casing.
                  Returns empty list if no data or error occurs.

    Raises:
        Shows Streamlit error message if database operation fails.

    Example:
        >>> get_list()
        ['Milk', 'Bread', 'Eggs']
    """
    try:
        with st.spinner('Loading grocery list...'):
            response = supabase.table(
                SUPABASE_GROCERY_TABLE).select("*").execute()
            if response.data:
                # Extract the "groceries" list from the JSON
                groceries = response.data[0]["groceries"]
                # Return the list with proper title casing
                return [better_title(item) for item in groceries]
            else:
                return []
    except Exception as e:
        logger.error(f"Error in get_list: {e}")
        st.error(f"Error in get_list: {str(e)}")
        return []


def write_list() -> None:
    """
    Save the grocery list to Supabase.

    Args:
        None

    Returns:
        None

    Raises:
        Shows Streamlit error message if database operation fails.
    """
    grocery_list = st.session_state["grocery_list"]
    try:
        supabase.table(SUPABASE_GROCERY_TABLE).upsert({
            'id': 1,  # Use a constant ID for the single record
            'groceries': grocery_list
        }).execute()
    except Exception as e:
        logger.error(f"Error in write_list: {e}")
        st.error(f"Error in write_list: {str(e)}")


def get_groceries() -> dict[str, list]:
    """
    Read a supabase table and return a dictionary with categories as keys and lists of grocery items as values.

    Returns:
        A dictionary with categories as keys and lists of grocery items as values.

    Raises:
        Shows Streamlit error message if database operation fails.

    Example:
        >>> get_groceries()
        {'Fresh Produce': ['Apples', 'Bananas'], 'Meat & Seafood': ['Chicken', 'Fish']}
    """  # noqa
    try:
        response = supabase.table(SUPABASE_DEFAULT_TABLE).select("*").execute()
        if response.data:
            groceries = response.data[0]['groceries']
            groceries = {cat: sorted(better_title(item) for item in items)
                         for cat, items in groceries.items()}
            return groceries
        else:
            return {}
    except Exception as e:
        logger.error(f"Error in get_groceries: {e}")
        st.error(f"Error in get_groceries: {str(e)}")
        return {}


def write_groceries() -> None:
    """
    Write the groceries dictionary to a supabase table.

    Arguments:
        None

    Returns:
        None

    Raises:
        Shows Streamlit error message if database operation fails.
    """  # noqa
    groceries = st.session_state["groceries"]
    try:
        supabase.table(SUPABASE_DEFAULT_TABLE).upsert({
            'id': 1,  # Use a constant ID for the single record
            'groceries': groceries
        }).execute()
    except Exception as e:
        logger.error(f"Error in write_groceries: {e}")
        st.error(f"Error in write_groceries: {str(e)}")


# Grocery Management Functions
def add_default_groceries() -> None:
    """
    Add a new grocery item to the default grocery list

    Arguments:
        None

    Returns:
        None
    """
    groceries = st.session_state["groceries"]
    category = st.session_state["category"]
    if "new_grocery" in st.session_state:
        grocery = st.session_state["new_grocery"]
        if not groceries[category]:
            st.session_state["groceries"][category] = []
        if grocery not in groceries[category]:
            st.session_state["groceries"][category].append(
                grocery.title())


def remove_groceries() -> None:
    """
    Remove grocery items from the default grocery list.

    Arguments:
        None

    Returns:
        None
    """
    added_groceries = st.session_state["added_groceries"]
    groceries = st.session_state["groceries"]
    for grocery in added_groceries:
        for key in groceries.keys():
            if grocery.strip() in groceries[key]:
                st.session_state["groceries"][key].remove(grocery.strip())
    st.session_state["added_groceries"].clear()


def process_grocery_input(categories: list = CATEGORIES) -> None:
    """
    Process the grocery input and add it to the default grocery list

    Keyword Arguments:
        categories: List of valid grocery categories, default: CATEGORIES

    Returns:
        None
    """
    cat = st.session_state.get("category", None)
    grocery = st.session_state.get("tmp_grocery", "").strip()

    if not grocery:
        return

    if cat not in categories:
        st.error("Please select a category")
        return

    st.session_state["new_grocery"] = grocery
    add_default_groceries()
    st.session_state["tmp_grocery"] = ""
    st.rerun()


# UI Display Functions
def display_grocery_category(category) -> None:
    """
    Display the grocery category and items as checkboxes

    Arguments:
        None

    Returns:
        None
    """
    added_groceries = st.session_state["added_groceries"]
    groceries = st.session_state["groceries"]
    if category in groceries:
        # Clean up the category name for the anchor
        anchor = clean_category_name(category)

        # Display the category name with "Back to Top" link
        st.markdown(
            f'''
            <div style="display: flex;
            justify-content: space-between;
            align-items: center;">
                <h5 style="margin: 0;" id="{anchor}">{category}</h5>
                <a href="#top" style="font-size: 0.8em;
                text-decoration: none;">Back to Top</a>
            </div>
            ''',
            unsafe_allow_html=True
        )

        # Display the grocery items
        for grocery in groceries[category]:
            checkbox = st.checkbox(grocery, key=f"{category}_{grocery}")
            if checkbox:
                added_groceries.append(grocery)


def split_categories(categories: list = CATEGORIES) -> tuple[list[str],
                                                             list[str],
                                                             list[str]]:
    """
    Split categories into three columns based on total items.

    Arguments:
        groceries -- Dictionary of groceries with category names as keys

    Keyword Arguments:
        categories -- List of category names

    Returns:
        Three lists of categories for three columns.

    Example:
        >>> groceries = {"Fresh Produce": ["Apples", "Bananas"],
                        "Meat & Seafood": ["Chicken", "Fish"]}
        >>> split_categories(groceries)
        (['Fresh Produce'], ['Meat & Seafood'])
    """
    groceries = st.session_state["groceries"]
    total_items = sum(len(groceries[cat]) for cat in categories)
    target_items = total_items // 3 + 3

    current_items = 0
    col1_categories = []
    col2_categories = []
    col3_categories = []

    for category in categories:
        items_in_category = len(groceries[category])
        if current_items < target_items:
            col1_categories.append(category)
            current_items += items_in_category
        elif current_items < 2 * target_items:
            col2_categories.append(category)
            current_items += items_in_category
        else:
            col3_categories.append(category)

    return col1_categories, col2_categories, col3_categories


# Utility Functions
def clear_session_state() -> None:
    """
    Clear the session state for added groceries.

    Arguments:
        session_state -- The Streamlit session state dictionary
        added_groceries -- List of grocery items that were added

    Returns:
        None
    """
    added_groceries = st.session_state["added_groceries"]
    keys_to_clear = [key for key in st.session_state.keys() if any(
        grocery.strip() in key for grocery in added_groceries)]
    for key in keys_to_clear:
        st.session_state[key] = False


def clean_category_name(category: str) -> str:
    """
    Clean the category name to be used as a URL path.

    Arguments:
        category: The category name to clean

    Returns:
        str: A cleaned category name with lowercase letters,
             hyphens instead of spaces, and no ampersands

    Example:
        >>> clean_category_name("Dairy & Eggs")
        'dairy-eggs'
    """
    category = category.lower()
    category = category.replace(" ", "-")
    category = category.replace("&", "")
    category = category.replace("--", "-")
    return category
