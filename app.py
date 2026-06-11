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
    # On crée le PDF avec une largeur de page A4 standard
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()
    
    # Marge de 20mm pour éviter que le texte ne colle aux bords
    pdf.set_margins(20, 20, 20) 
    pdf.set_auto_page_break(auto=True, margin=20)
    
    # Zone de texte utile : 210mm (largeur A4) - 40mm (marges) = 170mm
    largeur_utile = 170

    # Gestion du logo
    if os.path.exists("logo.jpg"):
        pdf.image("logo.jpg", x=20, y=20, w=30)

    pdf.ln(30) # Espace après le logo
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(largeur_utile, 10, "CERTIFICAT MEDICAL", ln=True, align='C')
    pdf.cell(largeur_utile, 10, "DE COMPATIBILITE A LA GARDE A VUE", ln=True, align='C')
    pdf.ln(10)
    
    # Texte du certificat
    pdf.set_font("Arial", '', 11)
    intro = f"Je soussigné(e), médecin urgentiste, atteste avoir procédé ce jour à l'examen médical de {nom} {prenom}, né(e) le {date_nais} ({sexe})."
    pdf.multi_cell(largeur_utile, 7, intro)
    pdf.ln(5)
    
    # Sections
    sections = [
        ("Lieu et heure :", f"Lieu : {lieu} | Date : {date.today()} | Heure : {str(heure)}"),
        ("Observations médicales :", f"État : {obs_options}"),
        ("Précisions :", obs_details),
        ("Traitements :", traitements),
        ("CONCLUSION :", conclusion)
    ]
    
    for titre, contenu in sections:
        pdf.set_font("Arial", 'B', 11)
        pdf.multi_cell(largeur_utile, 7, titre)
        pdf.set_font("Arial", '', 11)
        pdf.multi_cell(largeur_utile, 7, contenu)
        pdf.ln(3)
    
    # Signature
    pdf.ln(10)
    pdf.set_font("Arial", '', 11)
    pdf.cell(largeur_utile, 8, f"Fait à {lieu}, le {date.today()}", ln=True, align='R')
    pdf.cell(largeur_utile, 8, "Signature et cachet du médecin :", ln=True, align='R')
    pdf.ln(15)
    pdf.cell(largeur_utile, 8, "____________________", ln=True, align='R')
    
    st.download_button("Télécharger le Certificat", bytes(pdf.output()), "Certificat_GAV.pdf", "application/pdf")