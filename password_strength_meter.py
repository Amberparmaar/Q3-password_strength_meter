import streamlit as st
import re
import random
import string
import pandas as pd 
import os

def check_password_strength(password):
    score = 0
    feedback = []
    
    # Criteria checks
    if len(password) >= 8:
        score += 1
    else:
        feedback.append("Password should be at least 8 characters long.")
    
    if any(c.islower() for c in password):
        score += 1
    else:
        feedback.append("Add at least one lowercase letter.")
    
    if any(c.isupper() for c in password):
        score += 1
    else:
        feedback.append("Add at least one uppercase letter.")
    
    if any(c.isdigit() for c in password):
        score += 1
    else:
        feedback.append("Include at least one digit (0-9).")
    
    if re.search(r"[!@#$%^&*]", password):
        score += 1
    else:
        feedback.append("Use at least one special character (!@#$%^&*).")
    
    # Score classification
    if score <= 2:
        strength = "Weak"
    elif score <= 4:
        strength = "Moderate"
    else:
        strength = "Strong"
    
    return strength, feedback

def generate_strong_password(length=12):
    characters = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(random.choice(characters) for _ in range(length))

def save_password(account_name, password, strength):
    data = {"Account Name": [account_name], "Password": [password], "Strength": [strength]}
    df = pd.DataFrame(data)
    file_path = "saved_passwords.csv"
    
    if os.path.exists(file_path):
        df.to_csv(file_path, mode='a', header=False, index=False)
    else:
        df.to_csv(file_path, index=False)

# Streamlit UI with CSS
st.markdown("""
    <style>
        body {
            background-color: #000000;
        }
        .stTextInput, .stButton>button {
            font-size: 18px;
            padding: 10px;
            border-radius: 5px;
        }
        .stTextInput>div>div>input {
            border: 2px solid #4CAF50;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
        }
        .stButton>button:hover {
            background-color: #45a049;
        }
    </style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("🔧 Options")
st.sidebar.write("Use the tools below to enhance your password security.")
if st.sidebar.button("Generate Strong Password"):
    new_password = generate_strong_password()
    st.sidebar.text_input("Suggested Password:", new_password)

st.title("🔒 Password Strength Meter")
account_name = st.text_input("Enter Account Name:")
password = st.text_input("Enter your password:", type="password")

authentic_passwords = ["Admin@123", "Password@2024", "SecurePass!99"]

if password:
    if password in authentic_passwords:
        st.error("❌ This password is too common. Choose a stronger one.")
    else:
        strength, feedback = check_password_strength(password)
        st.subheader(f"Password Strength: {strength}")
        
        if strength == "Weak":
            st.warning("⚠ Your password is weak. Consider the following improvements:")
            for tip in feedback:
                st.write(f"- {tip}")
        elif strength == "Moderate":
            st.info("✅ Your password is moderate. You can improve it by following suggestions:")
            for tip in feedback:
                st.write(f"- {tip}")
        else:
            st.success("🎉 Your password is strong!")
            if st.button("Save Password"):
                save_password(account_name, password, strength)
                st.success("Password saved successfully!")

# Export Passwords
if os.path.exists("saved_passwords.csv"):
    with open("saved_passwords.csv", "rb") as file:
        st.download_button("📥 Download Saved Passwords", file, file_name="saved_passwords.csv", mime="text/csv")
