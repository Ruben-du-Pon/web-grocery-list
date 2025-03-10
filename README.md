# Web Grocery List

A Streamlit-based web application for managing grocery lists with category organization and persistent storage using Supabase.

## Features

- Create and manage grocery lists
- Organize items by categories
- Persistent storage with Supabase
- Mobile-responsive design
- Default grocery suggestions

## Setup

1. Clone the repository
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Set up Supabase:
   - Create a Supabase account
   - Create tables: `grocery_list` and `default_groceries`
   - Add your Supabase credentials to `.streamlit/secrets.toml`:

     ```toml
     SUPABASE_URL = "your-url"
     SUPABASE_KEY = "your-key"
     ```

## Project Structure

```text
web_grocery_list/
├── .streamlit/
│   ├── config.toml      # Streamlit configuration
│   └── secrets.toml     # Secrets (not in repo)
├── config.py            # Application constants
├── functions.py         # Core functionality
├── main.py              # Streamlit app entry point
├── requirements.txt     # Project dependencies
└── styles.py            # CSS styles
```

## Usage

Run the app locally:

```bash
streamlit run main.py
```
