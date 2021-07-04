import numpy as np
import pandas as pd
import streamlit as st
from pickle import load
from scipy import sparse
from db.mongo import MongoDB
from setup.configuration import get_configuration
from setup.load import load_variable

# Config
st.set_page_config(
    page_title='JobAI',
    page_icon='💸'
)

# Load variables
experience = load_variable('experience.pkl')
education = load_variable('education.pkl')
employment_type = load_variable('employment_type.pkl')
vectorizer = load_variable('vectorizer.pkl')
model = load_variable('model.pkl')

# TMP
experience.pop('')
education.pop('')


# Streamlit Page
st.title('💸 JobAI - Prédis ton salaire')

st.subheader('Formulaire')

# Job title
x_title = st.text_input('Nom du poste', 'Data Scientist')

# TODO - Job employment type requirements
x_employment_type = st.selectbox('Type de contrat', [_ for _ in employment_type.keys()])

# TODO - Job experience requirements
x_experience = st.selectbox('Expérience requis', [_ for _ in experience.keys()])

# TODO - Job education requirements
x_education = st.selectbox('Niveau scolaire requis', [_ for _ in education.keys()])

# Job description
x_description = st.text_area('Description du poste')

# Launch prediction
prediction = st.button('Prédire le salaire')

if prediction:
    # Preprocessing
    X = vectorizer.transform(np.array([x_title + ' ' + x_description]))
    X = sparse.hstack((X, np.array([education[x_education]])))
    X = sparse.hstack((X, np.array([experience[x_experience]])))
    X = sparse.hstack((X, np.array([employment_type[x_employment_type]])))
    salary = round(model.predict(X)[0])

    # Display
    st.subheader('Salaire')
    st.success(f'**{salary}**€')
