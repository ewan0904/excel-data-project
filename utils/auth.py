# auth.py
import streamlit as st
import requests
from streamlit_cookies_manager import EncryptedCookieManager

# -----------------------------
# --- FIREBASE Sign In Page ---
# -----------------------------
API_KEY = st.secrets['FIREBASE_API_KEY']
FIREBASE_SIGNIN = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={API_KEY}"

# ----------------------
# --- Cookie manager ---
# ----------------------
cookies = EncryptedCookieManager(prefix="auth_", password=st.secrets["COOKIE_ENCRYPTION_KEY"])
if not cookies.ready():
    st.stop()

# ------------------
# --- Log In/Out ---
# ------------------
def login_form():
    """
    Displays a login form in Streamlit and handles authentication.
    
    If login is successful, the user's ID token and email are stored in 
    session state and cookies, and the page is reloaded. On failure, 
    an error message is shown.
    """
    with st.form("Login"):
        email = st.text_input("Email")
        password = st.text_input("Passwort", type="password")
        submitted = st.form_submit_button("Login")

        if submitted:
            result = login_user(email, password)
            if "idToken" in result:
                st.session_state["idToken"] = result["idToken"]
                st.session_state["email"] = result["email"]
                cookies["idToken"] = result["idToken"]
                cookies["email"] = result["email"]
                cookies.save()
                st.success("Logged in!")
                st.rerun()
            else:
                st.error(result.get("error", {}).get("message", "Login failed"))

def login_user(email, password):
    """
    Sends a login request to Firebase using the REST API.

    Args:
        email (str): User's email address.
        password (str): User's password.

    Returns:
        dict: JSON response from Firebase, containing either the ID token or an error.
    """
    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }
    response = requests.post(FIREBASE_SIGNIN, json=payload)
    return response.json()

def require_login():
    """
    Ensures that a user is logged in before proceeding.

    If not logged in, attempts to restore session state from cookies. 
    If no credentials are found, prompts the user to log in and stops script execution.
    """
    # Rehydrate session from cookies if needed
    if "idToken" not in st.session_state and cookies.get("idToken"):
        st.session_state["idToken"] = cookies.get("idToken")
        st.session_state["email"] = cookies.get("email")

    if "idToken" not in st.session_state:
        st.warning("Bitte logge dich erst ein.")
        login_form()
        st.stop()  # Prevent rest of the page from loading

def logout():
    """
    Logs the user out by clearing session state and cookies, then reruns the app.
    """
    for key in ["idToken", "email"]:
        st.session_state.pop(key, None)
        cookies[key] = ""
    cookies.save()
    st.rerun()