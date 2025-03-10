import streamlit as st
from supabase import create_client, Client
from typing import Optional


class SupabaseClient:
    """
    Singleton class for Supabase client.
    """
    _instance: Optional[Client] = None

    @classmethod
    def get_client(cls) -> Client:
        """
        Get or create Supabase client instance.

        Arguments:
            None

        Returns:
            Client -- Supabase client instance.
        """
        if cls._instance is None:
            supabase_url: str = st.secrets["SUPABASE_URL"]
            supabase_key: str = st.secrets["SUPABASE_KEY"]
            cls._instance = create_client(supabase_url, supabase_key)
        return cls._instance


# Create a single instance to be imported by other modules
supabase = SupabaseClient.get_client()
