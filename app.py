import streamlit as st
from fpdf import FPDF
import datetime
from datetime import date
import os

st.title("Dossier de Visite Médicale")

# --- 1. Formulaire ---
with st.expander("1. Informations personnelles", expanded=True):
    nom = st.text_input("Nom")
    prenom = st.text_input("Prénom")
    date_nais = st.date_input("Date de naissance", min_value=datetime.date(1900, 1, 1), max_value=date.today())
    sexe = st.selectbox("Sexe", ["Masculin", "Féminin", "Autre"])
    adresse = st.text_area("Adresse")
    tel = st.text_input("Téléphone")
    urgence = st.text_input("Contact d'urgence")
    tel_urgence = st.text_input("Tel urgence")

nom_medecin = st.text_input("Nom du Médecin")
motif = st.text_area("2. Motif de la consultation")
maladies = st.text_input("3. Maladies chroniques")
chir = st.text_input("Chirurgies")
allergies = st.text_input("Allergies")
traitements = st.text_input("Traitements en cours")
diabete = st.text_input("Diabète")
ht = st.text_input("Hypertension")
habitudes = st.text_area("4. Habitudes de vie")

with st.expander("5. Examen clinique"):
    taille = st.number_input("Taille (cm)", value=170.0)
    poids = st.number_input("Poids (kg)", value=70.0)
    tension = st.text_input("Tension artérielle")
    frequence = st.text_input("Fréquence cardiaque")
    temp = st.text_input("Température")
    obs_clinique = st.text_area("Observations médicales")

examens = st.text_area("6. Examens complémentaires")
diagnostic = st.text_area("7. Diagnostic")
traitement = st.text_area("8. Traitement")
recommandations = st.text_area("9. Recommandations médicales")
suivi = st.text_area("10. Suivi médical")

# --- 2. Génération PDF ---
if st.button("Générer le Dossier Médical"):
    imc_val = round(poids / ((taille / 100) ** 2), 1) if taille > 0 else 0
    
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    largeur = 180 
    
    if os.path.exists("logo.jpg"):
        pdf.image("logo.jpg", x=15, y=15, w=30)
    
    pdf.ln(25)
    pdf.set_font("Arial", 'B', 16)
    pdf.set_x(15)
    pdf.cell(largeur, 10, "DOSSIER DE VISITE MEDICALE", ln=True, align='C')
    pdf.ln(10)
    
    sections = [
        ("1. INFOS PERSONNELLES", f"Nom: {nom} {prenom} | Né le: {date_nais} | Sexe: {sexe}\nAdresse: {adresse}\nTel: {tel}\nUrgence: {urgence} ({tel_urgence})"),
        ("2. MOTIF", motif),
        ("3. ANTECEDENTS", f"Maladies: {maladies}, Chir: {chir}, Allergies: {allergies}, Traitements: {traitements}, Diabète: {diabete}, Hypertension: {ht}"),
        ("4. HABITUDES DE VIE", habitudes),
        ("5. EXAMEN CLINIQUE", f"Taille: {taille}cm, Poids: {poids}kg, IMC: {imc_val}, Tension: {tension}, Fréq: {frequence}, Temp: {temp}\nObs: {obs_clinique}"),
        ("6. EXAMENS COMPLEMENTAIRES", examens),
        ("7. DIAGNOSTIC", diagnostic),
        ("8. TRAITEMENT", traitement),
        ("9. RECOMMANDATIONS", recommandations),
        ("10. SUIVI MEDICAL", suivi)
    ]
    
    for titre, contenu in sections:
        pdf.set_x(15)
        pdf.set_font("Arial", 'B', 12)
        pdf.multi_cell(largeur, 8, titre.encode('latin-1', 'replace').decode('latin-1'), 0, 'L')
        pdf.set_x(15)
        pdf.set_font("Arial", '', 11)
        pdf.multi_cell(largeur, 7, (contenu if contenu else "").encode('latin-1', 'replace').decode('latin-1'), 0, 'L')
        pdf.ln(2)
    
    pdf.ln(10)
    pdf.set_x(15)
    pdf.set_font("Arial", 'B', 12)
    pdf.multi_cell(largeur, 8, f"Médecin : {nom_medecin}".encode('latin-1', 'replace').decode('latin-1'), 0, 'R')
    pdf.set_x(15)
    pdf.multi_cell(largeur, 8, "Signature : ____________________", 0, 'R')
    
    st.download_button("Télécharger le Dossier", bytes(pdf.output()), "Dossier_Medical.pdf", "application/pdf")