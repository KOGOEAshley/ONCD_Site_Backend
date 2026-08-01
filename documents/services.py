import io

from django.template import Context, Template
from xhtml2pdf import pisa


def rendre_modele(modele, contexte: dict) -> str:
    """
    Injecte les données (praticien, formation...) dans le HTML stocké en base.
    C'est ce qui permet à un même moteur de générer n'importe quel type
    de document, sans code spécifique par type.
    """
    template = Template(modele.corps_html)
    return template.render(Context(contexte))


def generer_pdf_depuis_html(html: str) -> bytes:
    """Convertit du HTML en PDF (bytes), réutilisable pour n'importe quel document."""
    buffer = io.BytesIO()
    resultat = pisa.CreatePDF(html, dest=buffer)
    if resultat.err:
        raise ValueError("Erreur lors de la génération du PDF.")
    return buffer.getvalue()