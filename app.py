import streamlit as st
from fpdf import FPDF
import os
from datetime import date

st.title("Certificat de Compatibilité à la Garde à Vue")

# --- Formulaire ---
with st.form("certificat_garde_a_vue"):
    st.subheader("1. Identité de la personne examinée")
    nom = st.text_input("Nom")
    prenom = st.text_input("Prénom")
    date_nais = st.date_input("Date de naissance")
    sexe = st.selectbox("Sexe", ["Homme", "Femme"])

    st.subheader("2. Lieu et heure de l’examen")
    lieu = st.text_input("Lieu (Commissariat / Gendarmerie)")
    heure = st.time_input("Heure de l'examen")

    st.subheader("3. Observations médicales")
    obs_options = st.radio("État de santé", [
        "Aucune blessure ni pathologie constatée",
        "Blessures légères, pas d'hospitalisation nécessaire",
        "Pathologies nécessitant un suivi particulier",
        "Autres"
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
    pdf = FPDF()
    pdf.add_page()
    pdf.set_margins(10, 10, 10)
    pdf.set_auto_page_break(auto=True, margin=15) # Important pour éviter que ça sorte en bas
    
    if os.path.exists("logo.jpg"):
        pdf.image("logo.jpg", x=10, y=10, w=30)

    pdf.ln(25) # Espace après le logo
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(190, 10, "CERTIFICAT MEDICAL DE COMPATIBILITE", ln=True, align='C')
    pdf.ln(10)
    
    # Corps du texte avec multi_cell pour gérer les retours à la ligne
    pdf.set_font("Arial", '', 12)
    intro = f"Je soussigné(e), médecin urgentiste, atteste avoir procédé ce jour à l'examen médical de {nom} {prenom}, né(e) le {date_nais} ({sexe})."
    pdf.multi_cell(190, 8, intro)
    pdf.ln(5)
    
    pdf.set_font("Arial", 'B', 12)
    pdf.multi_cell(190, 8, "Lieu et heure :")
    pdf.set_font("Arial", '', 11)
    pdf.multi_cell(190, 8, f"Lieu : {lieu} | Date : {date.today()} | Heure : {str(heure)}")
    pdf.ln(5)
    
    pdf.set_font("Arial", 'B', 12)
    pdf.multi_cell(190, 8, "Observations et conclusion :")
    pdf.set_font("Arial", '', 11)
    pdf.multi_cell(190, 8, f"État : {obs_options}")
    pdf.multi_cell(190, 8, f"Précisions : {obs_details}")
    pdf.multi_cell(190, 8, f"Traitements : {traitements}")
    pdf.ln(5)
    
    pdf.set_font("Arial", 'B', 12)
    pdf.multi_cell(190, 10, f"CONCLUSION : {conclusion}")
    
    pdf.ln(20)
    pdf.set_font("Arial", '', 12)
    pdf.multi_cell(190, 8, f"Fait à {lieu}, le {date.today()}", align='R')
    pdf.multi_cell(190, 8, "Signature et cachet du médecin : ____________________", align='R')
    
    pdf_final = bytes(pdf.output())
    st.download_button("Télécharger le Certificat", pdf_final, "Certificat_GAV.pdf", "application/pdf")