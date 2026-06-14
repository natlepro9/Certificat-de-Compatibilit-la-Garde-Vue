import streamlit as st
from fpdf import FPDF
import datetime
from datetime import date

st.title("Certificat de Compatibilité à la Garde à Vue")

# --- Formulaire ---
with st.form("certificat_garde_a_vue"):
    nom = st.text_input("Nom")
    prenom = st.text_input("Prénom")
    date_nais = st.date_input("Date de naissance", min_value=datetime.date(1900, 1, 1), max_value=date.today())
    sexe = st.selectbox("Sexe", ["Homme", "Femme"])
    lieu = st.text_input("Lieu (Commissariat / Gendarmerie)")
    heure = st.time_input("Heure de l'examen")
    obs_options = st.radio("État de santé", ["Aucune blessure", "Blessures légères", "Pathologies", "Autres"])
    obs_details = st.text_area("Précisions")
    traitements = st.text_area("Traitements")
    conclusion = st.selectbox("Décision", ["Compatible", "Compatible sous réserve", "Incompatible"])
    submit = st.form_submit_button("Générer le Certificat PDF")

# --- Génération PDF ---
if submit:
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()
    
    # Largeur fixe 180mm (210mm A4 - 15mm marge gauche - 15mm marge droite)
    largeur = 180 
    
    # Titre
    pdf.set_font("Arial", 'B', 16)
    pdf.set_x(15) 
    pdf.multi_cell(largeur, 10, "CERTIFICAT MEDICAL DE COMPATIBILITE", 0, 'C')
    pdf.ln(10)
    
    # Texte fixe avec alignement forcé
    def ecrire_ligne(titre, texte):
        pdf.set_x(15)
        pdf.set_font("Arial", 'B', 12)
        pdf.multi_cell(largeur, 8, titre.encode('latin-1', 'replace').decode('latin-1'), 0, 'L')
        pdf.set_x(15)
        pdf.set_font("Arial", '', 12)
        pdf.multi_cell(largeur, 8, texte.encode('latin-1', 'replace').decode('latin-1'), 0, 'L')
        pdf.ln(2)

    ecrire_ligne("Identité :", f"{nom} {prenom}, né(e) le {date_nais} ({sexe})")
    ecrire_ligne("Lieu et heure :", f"{lieu} à {heure}")
    ecrire_ligne("Observations :", f"{obs_options} - {obs_details}")
    ecrire_ligne("Traitements :", traitements)
    ecrire_ligne("Conclusion :", conclusion)
    
    # Signature
    pdf.ln(10)
    pdf.set_x(15)
    pdf.multi_cell(largeur, 8, f"Fait le {date.today()} à {lieu}".encode('latin-1', 'replace').decode('latin-1'), 0, 'R')
    pdf.set_x(15)
    pdf.multi_cell(largeur, 8, "Signature et cachet : ____________________".encode('latin-1', 'replace').decode('latin-1'), 0, 'R')
    
    st.download_button("Télécharger le Certificat", bytes(pdf.output()), "Certificat.pdf", "application/pdf")