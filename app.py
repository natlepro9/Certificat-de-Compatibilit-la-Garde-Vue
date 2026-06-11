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
    
    # Gestion du logo
    if os.path.exists("logo.jpg"):
        pdf.image("logo.jpg", x=10, y=10, w=30)

    # En-tête
    pdf.set_font("Arial", 'B', 16)
    pdf.ln(10) # Espace pour ne pas chevaucher le logo
    pdf.cell(190, 10, "CERTIFICAT MEDICAL DE COMPATIBILITE", ln=True, align='C')
    pdf.ln(10)
    
    # Contenu
    pdf.set_font("Arial", '', 12)
    pdf.multi_cell(190, 8, f"Je soussigné(e), médecin urgentiste, atteste avoir procédé ce jour à l'examen médical de {nom} {prenom}, né(e) le {date_nais} ({sexe}).")
    pdf.ln(5)
    
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(190, 8, "Lieu et heure :", ln=True)
    pdf.set_font("Arial", '', 11)
    pdf.cell(190, 8, f"Lieu : {lieu} | Date : {date.today()} | Heure : {str(heure)}", ln=True)
    pdf.ln(5)
    
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(190, 8, "Observations et conclusion :", ln=True)
    pdf.set_font("Arial", '', 11)
    pdf.multi_cell(190, 8, f"État : {obs_options}")
    pdf.multi_cell(190, 8, f"Précisions : {obs_details}")
    pdf.multi_cell(190, 8, f"Traitements : {traitements}")
    pdf.ln(5)
    
    pdf.set_font("Arial", 'B', 12)
    pdf.multi_cell(190, 10, f"CONCLUSION : {conclusion}")
    
    pdf.ln(20)
    pdf.set_font("Arial", '', 12)
    pdf.cell(190, 10, f"Fait à {lieu}, le {date.today()}", ln=True, align='R')
    pdf.cell(190, 10, "Signature et cachet du médecin : ____________________", ln=True, align='R')
    
    # Conversion finale
    pdf_final = bytes(pdf.output())
    
    st.download_button("Télécharger le Certificat", pdf_final, "Certificat_GAV.pdf", "application/pdf")