# Web Grocery List

A Streamlit-based web application for managing grocery lists with category organization and persistent storage using Supabase.

## Features

- Create and manage grocery lists
- Organize items by categories
- Real-time background saving to Supabase
- Mobile-responsive design
- Default grocery suggestions
- Progressive Web App (PWA) support
- Dark theme interface

## Setup

1. Clone the repository
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Set up Supabase:
   - Create a Supabase account
   - Create tables: 
     - `grocery_list`: For storing the current grocery list
     - `default_groceries`: For storing default grocery items by category
     - `log_entries`: For application logging
   - Add your Supabase credentials to `.streamlit/secrets.toml`:

     ```toml
     SUPABASE_URL = "your-url"
     SUPABASE_KEY = "your-key"
     ```

## Project Structure

```text
web_grocery_list/
├── .streamlit/
│   ├── config.toml      # Streamlit theme configuration
│   └── secrets.toml     # Supabase credentials (not in repo)
├── config.py            # Application constants and categories
├── database.py          # Supabase client configuration
├── functions.py         # Core functionality and background operations
├── logger_config.py     # Logging configuration with Supabase integration
├── main.py              # Streamlit app entry point
├── requirements.txt     # Project dependencies
└── styles.py            # CSS styles for mobile responsiveness
```

## Usage

Run the app locally:

```bash
streamlit run main.py
```

Access the app through your browser or install it as a PWA on mobile devices.
