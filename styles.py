MOBILE_STYLES = """
<style>
    /* Make fonts smaller on mobile devices */
    @media (max-width: 600px) {
        h1 {
            font-size: 1.5rem !important;
        }
        h5 {
            font-size: 0.9rem !important;
        }
        p, span, label {
            font-size: 0.8rem !important;
        }
        .stCheckbox {
            font-size: 0.8rem !important;
        }
        .css-1s9bf49, .css-15z7xkx, .css-1v0mbdj {
            font-size: 0.8rem !important;
        }
        /* Make select box text smaller */
        .stSelectbox {
            font-size: 0.75rem !important;
        }
        /* Make input text smaller */
        .stTextInput {
            font-size: 0.75rem !important;
        }
    }

    /* Index links styling for mobile */
    @media (max-width: 600px) {
        .css-13wxj5s {
            font-size: 0.8rem !important;
            display: block;
            padding: 5px;
            line-height: 1.2;
        }
    }

    /* Adjust container width */
    .container {
        max-width: 100% !important;
    }

    /* Back to Top link styling for mobile */
    @media (max-width: 600px) {
        a[href="#"] {
            font-size: 0.6em !important;
        }
    }
    
    /* Force columns to be content-width */
    [data-testid="column"] {
        width: auto !important;
        flex: 0 0 auto !important;
        min-width: auto !important;
        padding: 0 5px !important;
    }

    /* Button styling */
    .stButton {
        width: auto !important;
        margin: 0 !important;
    }

    .stButton > button {
        width: auto !important;
        white-space: nowrap !important;
    }

    /* Mobile adjustments */
    @media (max-width: 600px) {
        [data-testid="column"] {
            width: auto !important;
            min-width: auto !important;
            flex: 0 0 auto !important;
        }
        .stButton > button {
            padding: 0.25rem 0.5rem !important;
            min-height: 35px !important;
            font-size: 0.75rem !important;
        }
    }
</style>
"""
