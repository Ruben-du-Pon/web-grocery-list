MOBILE_STYLES = """
<style>
    /* Make fonts smaller on mobile devices */
    @media (max-width: 600px) {
        h1 {
            font-size: 1.8rem !important;
        }
        h5 {
            font-size: 1rem !important;
        }
        p, span, label {
            font-size: 0.9rem !important;
        }
        .stCheckbox {
            font-size: 0.9rem !important;
        }
        .css-1s9bf49, .css-15z7xkx, .css-1v0mbdj {
            font-size: 0.9rem !important;
        }
        /* Make select box text smaller */
        .stSelectbox {
            font-size: 0.9rem !important;
        }
        /* Make input text smaller */
        .stTextInput {
            font-size: 0.9rem !important;
        }
    }

    /* Index links styling for mobile */
    @media (max-width: 600px) {
        .css-13wxj5s {
            font-size: 0.9rem !important;
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
            font-size: 0.7em !important;
        }
    }
    
    /* Button container styling */
    .stButton {
        display: inline-block;
        margin-right: 0 !important;
    }

    /* Adjust button spacing on mobile */
    @media (max-width: 600px) {
        .stButton {
            margin: 0 !important;
            padding: 0 !important;
        }
        .stButton > button {
            padding: 0.25rem 0.5rem !important;
            min-height: 35px !important;
        }
    }
</style>
"""
