import streamlit as st
from fpdf import FPDF
import os
import datetime
from datetime import date

st.title("Certificat de Compatibilité à la Garde à Vue")

# --- Formulaire ---
with st.form("certificat_gav"):
    st.subheader("1. Identité de la personne examinée")
    nom = st.text_input("Nom")
    prenom = st.text_input("Prénom")
    date_nais = st.date_input("Date de naissance", min_value=datetime.date(1900, 1, 1), max_value=date.today())
    sexe = st.selectbox("Sexe", ["Homme", "Femme"])

    st.subheader("2. Lieu et heure de l'examen")
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
    
    nom_medecin = st.text_input("Nom du Médecin")
    submit = st.form_submit_button("Générer le Certificat PDF")

# --- Génération PDF ---
if submit:
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()
    pdf.set_margins(15, 15, 15)
    pdf.set_auto_page_break(auto=True, margin=15)
    
    largeur = 180 

    if os.path.exists("logo.jpg"):
        pdf.image("logo.jpg", x=15, y=15, w=30)

    pdf.ln(25)
    pdf.set_font("Arial", 'B', 16)
    pdf.set_x(15)
    pdf.multi_cell(largeur, 10, "CERTIFICAT MEDICAL\nDE COMPATIBILITE A LA GARDE A VUE".encode('latin-1', 'replace').decode('latin-1'), 0, 'C')
    pdf.ln(10)
    
    # Texte d'introduction
    pdf.set_font("Arial", '', 12)
    pdf.set_x(15)
    intro = f"Je soussigné(e), médecin urgentiste, atteste avoir procédé ce jour à l'examen médical de {nom} {prenom}, né(e) le {date_nais} ({sexe})."
    pdf.multi_cell(largeur, 8, intro.encode('latin-1', 'replace').decode('latin-1'), 0, 'L')
    pdf.ln(5)
    
    # Sections
    sections = [
        ("Lieu et heure :", f"Lieu : {lieu} | Date : {date.today()} | Heure : {str(heure)}"),
        ("Observations médicales :", f"État : {obs_options}\nPrécisions : {obs_details}"),
        ("Traitements et recommandations :", traitements),
        ("CONCLUSION :", conclusion)
    ]
    
    for titre, contenu in sections:
        pdf.set_x(15)
        pdf.set_font("Arial", 'B', 12)
        pdf.multi_cell(largeur, 8, titre.encode('latin-1', 'replace').decode('latin-1'), 0, 'L')
        pdf.set_x(15)
        pdf.set_font("Arial", '', 12)
        pdf.multi_cell(largeur, 8, (contenu if contenu else "").encode('latin-1', 'replace').decode('latin-1'), 0, 'L')
        pdf.ln(3)
    
    # Signature
    pdf.ln(10)
    pdf.set_x(15)
    pdf.set_font("Arial", '', 12)
    pdf.multi_cell(largeur, 8, f"Fait à {lieu}, le {date.today()}".encode('latin-1', 'replace').decode('latin-1'), 0, 'R')
    pdf.set_x(15)
    pdf.multi_cell(largeur, 8, f"Médecin : {nom_medecin}".encode('latin-1', 'replace').decode('latin-1'), 0, 'R')
    pdf.set_x(15)
    pdf.multi_cell(largeur, 8, "Signature et cachet : ____________________".encode('latin-1', 'replace').decode('latin-1'), 0, 'R')
    
    st.download_button("Télécharger le Certificat", bytes(pdf.output()), "Certificat_GAV.pdf", "application/pdf")