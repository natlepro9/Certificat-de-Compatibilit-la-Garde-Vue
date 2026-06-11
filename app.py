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
    # Paramètres de page A4 standard
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()
    
    # Définit des marges pour éviter le débordement
    # Marge de 10mm à gauche, en haut, et à droite
    pdf.set_margins(10, 10, 10) 
    pdf.set_auto_page_break(auto=True, margin=10)

    # Zone de texte utile : 210mm (A4) - 20mm (marges) = 190mm
    largeur_utile = 190

    # Gestion du logo
    if os.path.exists("logo.jpg"):
        pdf.image("logo.jpg", x=10, y=10, w=30)

    pdf.ln(30) # Espace après le logo
    pdf.set_font("Arial", 'B', 16)
    pdf.multi_cell(largeur_utile, 10, "CERTIFICAT MEDICAL", 0, 'C')
    pdf.multi_cell(largeur_utile, 10, "DE COMPATIBILITE A LA GARDE A VUE", 0, 'C')
    pdf.ln(10)
    
    # Texte d'introduction
    pdf.set_font("Arial", '', 11)
    intro_text = f"Je soussigné(e), médecin urgentiste, atteste avoir procédé ce jour à l'examen médical de {nom} {prenom}, né(e) le {date_nais} ({sexe})."
    pdf.multi_cell(largeur_utile, 7, intro_text)
    pdf.ln(5)
    
    # --- Agencement en colonnes pour les sections ---
    # Nous utilisons une largeur fixe pour les titres de section afin de forcer l'alignement
    largeur_titre_section = 60
    largeur_contenu_section = largeur_utile - largeur_titre_section

    sections = [
        ("Lieu et heure :", f"Lieu : {lieu} | Date : {date.today()} | Heure : {str(heure)}"),
        ("Observations médicales :", f"État : {obs_options}"),
        ("Précisions :", obs_details),
        ("Traitements :", traitements),
        ("CONCLUSION :", conclusion)
    ]
    
    # Pour chaque section, nous créons deux cellules de largeur fixe
    for titre, contenu in sections:
        pdf.set_font("Arial", 'B', 11)
        pdf.multi_cell(largeur_titre_section, 7, titre)
        
        pdf.set_font("Arial", '', 11)
        # multi_cell ici forcera le retour à la ligne si le texte est trop long
        pdf.multi_cell(largeur_contenu_section, 7, contenu)
        pdf.ln(3) # Espace entre les sections
    
    # Signature
    pdf.ln(10)
    pdf.set_font("Arial", '', 11)
    pdf.multi_cell(largeur_utile, 8, f"Fait à {lieu}, le {date.today()}", 0, 'R')
    pdf.multi_cell(largeur_utile, 8, "Signature et cachet du médecin :", 0, 'R')
    pdf.ln(15)
    pdf.multi_cell(largeur_utile, 8, "____________________", 0, 'R')
    
    # Conversion finale
    pdf_final = bytes(pdf.output())
    
    st.download_button("Télécharger le Certificat", pdf_final, "Certificat_GAV.pdf", "application/pdf")