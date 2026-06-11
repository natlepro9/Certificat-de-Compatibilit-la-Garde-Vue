import streamlit as st
from fpdf import FPDF
import os
import datetime
from datetime import date

st.title("Certificat de Compatibilité à la Garde à Vue")

# --- Formulaire ---
with st.form("certificat_garde_a_vue"):
    st.subheader("1. Identité de la personne examinée")
    nom = st.text_input("Nom")
    prenom = st.text_input("Prénom")
    date_nais = st.date_input("Date de naissance", min_value=datetime.date(1900, 1, 1), max_value=datetime.date.today())
    sexe = st.selectbox("Sexe", ["Homme", "Femme"])

    st.subheader("2. Lieu et heure de l’examen")
    lieu = st.text_input("Lieu (Commissariat / Gendarmerie)")
    heure = st.time_input("Heure de l'examen")

    st.subheader("3. Observations médicales")
    obs_options = st.radio("État de santé", [
        "Aucune blessure ni pathologie constatée",
        "Blessures légères, pas d'hospitalisation nécessaire",
        "Pathologies nécessitant un suivi particulier",
        "Autres",
        "Frais"
    ])
    obs_details = st.text_area("Précisions complémentaires")

    st.subheader("4. Traitements et recommandations")
    traitements = st.text_area("Prise médicamenteuse régulière ou surveillance")
    
    st.subheader("5. Conclusion médicale")
    conclusion = st.selectbox("Décision", [
        "Compatible avec une mesure de garde à vue",
        "Compatible avec une garde à vue sous réserve de soins",
        "Incompatible avec une garde à vue – Hospitalisation nécessaire"
    ])

    submit = st.form_submit_button("Générer le Certificat PDF")

# --- Génération PDF ---
if submit:
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()
    pdf.set_margins(15, 15, 15)
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Largeur de page utile (210 - 15 - 15 = 180mm)
    largeur = 180

    if os.path.exists("logo.jpg"):
        pdf.image("logo.jpg", x=15, y=15, w=30)

    pdf.ln(25)
    pdf.set_font("Arial", 'B', 16)
    pdf.multi_cell(largeur, 10, "CERTIFICAT MEDICAL\nDE COMPATIBILITE A LA GARDE A VUE", 0, 'C')
    pdf.ln(10)
    
    # Texte d'introduction
    pdf.set_font("Arial", '', 12)
    pdf.multi_cell(largeur, 8, f"Je soussigné(e), médecin urgentiste, atteste avoir procédé ce jour à l'examen médical de {nom} {prenom}, né(e) le {date_nais} ({sexe}).")
    pdf.ln(5)
    
    # Sections (Titre + Contenu)
    sections = [
        ("Lieu et heure :", f"Lieu : {lieu} | Date : {date.today()} | Heure : {str(heure)}"),
        ("Observations médicales :", f"État : {obs_options}\nPrécisions : {obs_details}"),
        ("Traitements et recommandations :", traitements),
        ("CONCLUSION :", conclusion)
    ]
    
    for titre, contenu in sections:
        pdf.set_font("Arial", 'B', 12)
        pdf.multi_cell(largeur, 8, titre)
        pdf.set_font("Arial", '', 12)
        pdf.multi_cell(largeur, 8, contenu)
        pdf.ln(3)
    
    # Signature
    pdf.ln(10)
    pdf.set_font("Arial", '', 12)
    pdf.multi_cell(largeur, 8, f"Fait à {lieu}, le {date.today()}", 0, 'R')
    pdf.multi_cell(largeur, 8, "Signature et cachet du médecin :", 0, 'R')
    pdf.ln(10)
    pdf.multi_cell(largeur, 8, "____________________", 0, 'R')
    
    st.download_button("Télécharger le Certificat", bytes(pdf.output()), "Certificat_GAV.pdf", "application/pdf")