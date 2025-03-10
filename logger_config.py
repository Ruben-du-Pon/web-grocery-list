import logging
from datetime import datetime
from supabase import Client
from database import supabase


class SupabaseHandler(logging.Handler):
    """
    Custom logging handler that writes logs to Supabase.

    Methods:
        emit(record) -- Writes the log record to Supabase.
        format(record) -- Formats the log record.

    Attributes:
        supabase: Supabase client instance.
    """

    def __init__(self, supabase_client: Client) -> None:
        """
        Initialize the SupabaseHandler with a Supabase client instance.

        Arguments:
            supabase_client (Client) -- Supabase client instance.

        Returns:
            None

        Example:
            >>> supabase_handler = SupabaseHandler(supabase_client)
        """
        super().__init__()
        self.supabase = supabase_client

    def format(self, record: logging.LogRecord) -> str:
        """
        Format the log record into a string.

        Arguments:
            record (logging.LogRecord) -- Log record to be formatted.

        Returns:
            str -- Formatted log message.
        """
        return record.getMessage()

    def emit(self, record):
        """
        Write the log record to Supabase.

        Arguments:
            record (logging.LogRecord) -- Log record to be written.

        Returns:
            None
        """
        try:
            log_entry = {
                'timestamp': datetime.now().isoformat(),
                'level': record.levelname,
                'message': self.format(record),
                'function': record.funcName,
                'line_no': record.lineno,
                'module': record.module
            }
            self.supabase.table('log_entries').insert(log_entry).execute()
        except Exception as e:
            print(f"Failed to write log to Supabase: {e}")


# Configure root logger
logging.basicConfig(level=logging.INFO)
root_logger = logging.getLogger()

# Add Supabase handler to the root logger
supabase_handler = SupabaseHandler(supabase)
supabase_handler.setLevel(logging.ERROR)
root_logger.addHandler(supabase_handler)

# Function to get logger for each module


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
