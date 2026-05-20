"""
Génère BachelorHETIC_GARSIGLIA_Lorenzo_B3_Python.pdf
Réponse complète au Sujet 3 — Bloc 3 Python (Développement + Déploiement)
Lancer : venv/Scripts/python generate_exam_pdf.py
"""
import os
from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    BaseDocTemplate, Frame, PageTemplate, Paragraph, Spacer,
    Table, TableStyle, PageBreak, HRFlowable, KeepTogether,
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY

# ─── Palette ──────────────────────────────────────────────────────────────────
BLUE       = colors.HexColor("#1A237E")
LIGHT_BLUE = colors.HexColor("#E8EAF6")
ACCENT     = colors.HexColor("#3949AB")
GREEN      = colors.HexColor("#2E7D32")
LIGHT_GRN  = colors.HexColor("#E8F5E9")
ORANGE     = colors.HexColor("#E65100")
GREY_BG    = colors.HexColor("#F5F5F5")
WHITE      = colors.white
BLACK      = colors.black
BORDER     = colors.HexColor("#90A4AE")

W, H = A4

# ─── Styles ───────────────────────────────────────────────────────────────────
base_styles = getSampleStyleSheet()

def S(name, parent="Normal", **kw):
    return ParagraphStyle(name, parent=base_styles[parent], **kw)

styles = {
    "cover_title":  S("cover_title",  fontSize=28, textColor=WHITE, leading=34, alignment=TA_CENTER, fontName="Helvetica-Bold"),
    "cover_sub":    S("cover_sub",    fontSize=14, textColor=LIGHT_BLUE, leading=20, alignment=TA_CENTER, fontName="Helvetica"),
    "cover_name":   S("cover_name",   fontSize=16, textColor=WHITE, leading=22, alignment=TA_CENTER, fontName="Helvetica-Bold"),
    "section":      S("section",      fontSize=15, textColor=BLUE, leading=20, fontName="Helvetica-Bold", spaceBefore=14, spaceAfter=6),
    "subsection":   S("subsection",   fontSize=12, textColor=ACCENT, leading=16, fontName="Helvetica-Bold", spaceBefore=10, spaceAfter=4),
    "body":         S("body",         fontSize=9.5, leading=14, alignment=TA_JUSTIFY, spaceAfter=4),
    "body_b":       S("body_b",       fontSize=9.5, leading=14, fontName="Helvetica-Bold"),
    "bullet":       S("bullet",       fontSize=9.5, leading=13, leftIndent=14, spaceAfter=2),
    "code":         S("code",         fontSize=8.5, fontName="Courier", leading=12, backColor=GREY_BG, leftIndent=10, rightIndent=10),
    "table_h":      S("table_h",      fontSize=9, textColor=WHITE, fontName="Helvetica-Bold", alignment=TA_CENTER),
    "table_c":      S("table_c",      fontSize=9, leading=12),
    "table_l":      S("table_l",      fontSize=9, leading=12, fontName="Helvetica-Bold"),
    "done":         S("done",         fontSize=9, textColor=GREEN, fontName="Helvetica-Bold", alignment=TA_CENTER),
    "caption":      S("caption",      fontSize=8, textColor=colors.grey, alignment=TA_CENTER, fontName="Helvetica-Oblique"),
    "h_white":      S("h_white",      fontSize=11, textColor=WHITE, fontName="Helvetica-Bold", alignment=TA_CENTER),
}

def P(text, style="body"):
    return Paragraph(text, styles[style])

def B(text):
    return Paragraph(f"• {text}", styles["bullet"])

def HR():
    return HRFlowable(width="100%", thickness=0.5, color=BORDER, spaceAfter=6, spaceBefore=6)

def SP(h=0.3):
    return Spacer(1, h * cm)

# ─── Helpers tableaux ─────────────────────────────────────────────────────────
TSTYLE_BASE = [
    ("GRID",         (0, 0), (-1, -1), 0.4, BORDER),
    ("ROWBACKGROUNDS", (0, 0), (-1, -1), [WHITE, GREY_BG]),
    ("VALIGN",       (0, 0), (-1, -1), "MIDDLE"),
    ("TOPPADDING",   (0, 0), (-1, -1), 5),
    ("BOTTOMPADDING",(0, 0), (-1, -1), 5),
    ("LEFTPADDING",  (0, 0), (-1, -1), 8),
    ("RIGHTPADDING", (0, 0), (-1, -1), 8),
]

def header_style(row=0):
    return [
        ("BACKGROUND",  (0, row), (-1, row), BLUE),
        ("TEXTCOLOR",   (0, row), (-1, row), WHITE),
        ("FONTNAME",    (0, row), (-1, row), "Helvetica-Bold"),
        ("FONTSIZE",    (0, row), (-1, row), 9),
        ("ALIGN",       (0, row), (-1, row), "CENTER"),
    ]

def make_table(data, col_widths, style_extra=None):
    ts = TableStyle(TSTYLE_BASE + header_style() + (style_extra or []))
    return Table(data, colWidths=col_widths, style=ts, repeatRows=1)

# ─── En-tête / pied de page ───────────────────────────────────────────────────
def on_page(canvas, doc):
    canvas.saveState()
    # Header
    canvas.setFillColor(BLUE)
    canvas.rect(0, H - 1.2 * cm, W, 1.2 * cm, fill=True, stroke=False)
    canvas.setFont("Helvetica-Bold", 9)
    canvas.setFillColor(WHITE)
    canvas.drawString(1.5 * cm, H - 0.85 * cm, "M-Motors — Bachelor HETIC B3 Python")
    canvas.drawRightString(W - 1.5 * cm, H - 0.85 * cm, "GARSIGLIA Lorenzo")
    # Footer
    canvas.setFillColor(LIGHT_BLUE)
    canvas.rect(0, 0, W, 0.8 * cm, fill=True, stroke=False)
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(BLUE)
    canvas.drawCentredString(W / 2, 0.25 * cm, f"Page {doc.page}")
    canvas.restoreState()

def on_cover(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(BLUE)
    canvas.rect(0, 0, W, H, fill=True, stroke=False)
    canvas.restoreState()

# ─── Document ─────────────────────────────────────────────────────────────────
# Sortie dans C:\Users\Lolo\Desktop\Studi2\ (dossier parent du repo)
OUTPUT = Path(__file__).parent.parent / "BachelorHETIC_GARSIGLIA_Lorenzo_B3_Python.pdf"
if not OUTPUT.parent.exists():
    OUTPUT = Path(__file__).parent / "BachelorHETIC_GARSIGLIA_Lorenzo_B3_Python.pdf"

doc = BaseDocTemplate(
    str(OUTPUT),
    pagesize=A4,
    leftMargin=1.8 * cm, rightMargin=1.8 * cm,
    topMargin=1.8 * cm, bottomMargin=1.8 * cm,
)

cover_frame  = Frame(0, 0, W, H, id="cover")
normal_frame = Frame(1.8*cm, 0.8*cm, W - 3.6*cm, H - 2.6*cm, id="normal")

doc.addPageTemplates([
    PageTemplate(id="Cover",  frames=[cover_frame],  onPage=on_cover),
    PageTemplate(id="Normal", frames=[normal_frame], onPage=on_page),
])

story = []

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE DE COUVERTURE
# ═══════════════════════════════════════════════════════════════════════════════
story.append(SP(5))
story.append(P("M-MOTORS", "cover_title"))
story.append(SP(0.5))
story.append(P("Application de vente et location longue durée de véhicules d'occasion", "cover_sub"))
story.append(SP(2))
story.append(HRFlowable(width="60%", thickness=1, color=ACCENT))
story.append(SP(1.5))
story.append(P("Bachelor HETIC — Bloc 3 Python", "cover_sub"))
story.append(P("Dossier de réponse à l'examen", "cover_sub"))
story.append(SP(2))
story.append(P("GARSIGLIA Lorenzo", "cover_name"))
story.append(SP(0.5))
story.append(P("Promotion B3 — 2025/2026", "cover_sub"))
story.append(SP(3))

cov_data = [
    [P("Élément", "table_h"),      P("Valeur", "table_h")],
    [P("Lien GitHub", "table_l"),  P("https://github.com/PapEXito/m-motors", "table_c")],
    [P("App déployée", "table_l"), P("https://m-motors-production.up.railway.app/", "table_c")],
    [P("Login admin", "table_l"),  P("admin / Admin123!", "table_c")],
    [P("Login client", "table_l"), P("client / Client123!", "table_c")],
    [P("Stack", "table_l"),        P("Django 5 · PostgreSQL · pytest · Railway", "table_c")],
]
cov_table = make_table(cov_data, [5*cm, 11*cm])
story.append(cov_table)
story.append(PageBreak())

# ═══════════════════════════════════════════════════════════════════════════════
# DOSSIER 1 — DÉVELOPPEMENT
# ═══════════════════════════════════════════════════════════════════════════════
story.append(P("Dossier 1 — Développement de la solution", "section"))
story.append(HR())

# ─── 1a. Git & branches ───────────────────────────────────────────────────────
story.append(P("Question 1a — Préparation Git et gestion des branches", "subsection"))
story.append(P(
    "Le projet suit le workflow <b>Git Flow</b> avec trois niveaux de branches : "
    "<b>main</b> (production stable), <b>develop</b> (intégration continue), "
    "et des <b>feature branches</b> par fonctionnalité. Les commits respectent "
    "la convention <b>Conventional Commits</b> (feat, fix, test, docs, chore).",
    "body"
))
story.append(SP(0.3))

git_data = [
    [P("Branche", "table_h"),           P("Rôle", "table_h"),                  P("Exemples de commits", "table_h")],
    [P("main", "table_l"),              P("Production — code validé et déployé. Reçoit les merges de develop via pull request.", "table_c"),
                                         P("release: v1.0.0 · release: v1.1.0", "table_c")],
    [P("develop", "table_l"),           P("Branche d'intégration. Point de départ de toutes les features.", "table_c"),
                                         P("Merge --no-ff de chaque feature", "table_c")],
    [P("feature/vehicles", "table_l"),  P("Modèles Marque/Vehicule, catalogue, seed_data, admin, tests unitaires.", "table_c"),
                                         P("feat(vehicles): add models · test(vehicles): unit tests", "table_c")],
    [P("feature/accounts", "table_l"),  P("Inscription, connexion, dashboard, InscriptionForm.", "table_c"),
                                         P("feat(accounts): add auth · test(accounts): auth tests", "table_c")],
    [P("feature/dossiers", "table_l"),  P("DossierAchat, DossierLocation, upload documents, workflow statut.", "table_c"),
                                         P("feat(dossiers): add models · test(dossiers): file validation", "table_c")],
    [P("feature/postgresql", "table_l"),P("Migration SQLite → PostgreSQL via dj-database-url.", "table_c"),
                                         P("feat(config): migrate to PostgreSQL", "table_c")],
    [P("feature/tests-fonctionnels", "table_l"), P("13 tests fonctionnels bout-en-bout, pytest.ini, conftest.py, start.bat.", "table_c"),
                                         P("test: add functional end-to-end tests", "table_c")],
]
story.append(make_table(git_data, [4*cm, 6.5*cm, 6*cm]))
story.append(SP(0.4))

story.append(P("<b>Règles appliquées :</b>", "body_b"))
story.append(B("Aucun commit direct sur <b>main</b> — tout passe par develop via merge --no-ff"))
story.append(B("Messages de commit en anglais, préfixés : feat / fix / test / docs / chore / release"))
story.append(B("Une feature branch par User Story ou groupe de fonctionnalités cohérent"))
story.append(B("Tags de version sémantique : v1.0.0 (MVP), v1.1.0 (PostgreSQL + tests fonctionnels)"))
story.append(B(".gitignore couvre : venv/, __pycache__/, .env, db.sqlite3, media/, staticfiles/"))
story.append(SP(0.4))

story.append(P("<b>Historique visible sur GitHub :</b>", "body_b"))
story.append(P(
    "→ github.com/PapEXito/m-motors — branches main, develop, feature/postgresql, "
    "feature/tests-fonctionnels. Commits conventionnels depuis le commit initial "
    "<code>chore: initial Django project setup</code>.",
    "body"
))

story.append(SP(0.6))
HR()

# ─── 1b. Démarche User Story ──────────────────────────────────────────────────
story.append(P("Question 1b — Démarche pour développer une User Story", "subsection"))
story.append(P(
    "Chaque User Story suit un cycle <b>Definition of Ready → Développement → Definition of Done</b> "
    "en 7 étapes :",
    "body"
))

us_steps = [
    ("1. Rédaction & priorisation",
     "La US est rédigée en format « En tant que <rôle>, je veux <action> afin de <bénéfice> ». "
     "Elle est estimée en points de complexité et intégrée dans le backlog."),
    ("2. Création de la branche",
     "git checkout develop && git checkout -b feature/<nom>. "
     "La branche est créée depuis develop, jamais depuis main."),
    ("3. Écriture des tests (TDD)",
     "Les tests unitaires ET fonctionnels sont écrits avant ou en parallèle du code. "
     "Ils définissent le comportement attendu (Given/When/Then)."),
    ("4. Développement",
     "Modèles → migrations → vues → templates → URLs. "
     "Chaque couche suit les conventions Django (class-based views, ModelForm, etc.)."),
    ("5. Commit(s) conventionnel(s)",
     "git add <fichiers> && git commit -m \"feat(app): description concise\". "
     "Les commits sont atomiques : un commit = une intention."),
    ("6. Merge dans develop",
     "git checkout develop && git merge --no-ff feature/<nom>. "
     "Le flag --no-ff préserve la trace du merge dans le graphe git."),
    ("7. Validation (Definition of Done)",
     "Tous les tests passent (python -m pytest -v), "
     "le comportement est vérifié manuellement dans le navigateur, "
     "la US passe en statut Done."),
]
for title, desc in us_steps:
    story.append(KeepTogether([
        P(f"<b>{title}</b>", "body_b"),
        P(desc, "bullet"),
        SP(0.15),
    ]))

story.append(SP(0.4))

# ─── 1c. Stack technique ──────────────────────────────────────────────────────
story.append(P("Question 1c — Outils et technologies utilisés", "subsection"))

tech_data = [
    [P("Couche", "table_h"),       P("Outil / Librairie", "table_h"), P("Rôle et justification du choix", "table_h")],
    [P("Back-end", "table_l"),     P("Django 5 / Python 3.12", "table_c"),
                                    P("Framework full-stack mature. ORM, admin, auth intégrés. Productivité maximale pour un monolithe MVC.", "table_c")],
    [P("Base de données", "table_l"), P("PostgreSQL (prod) + dj-database-url", "table_c"),
                                    P("Base relationnelle robuste, transactions ACID, gestion sécurisée des connexions. SQLite uniquement en développement local.", "table_c")],
    [P("Front-end", "table_l"),    P("Bootstrap 5 (CDN) + CSS custom", "table_c"),
                                    P("Templates Django natifs (Jinja-like). Aucune dépendance JS complexe. Responsive mobile-first.", "table_c")],
    [P("Upload / Médias", "table_l"), P("Pillow + FileField Django", "table_c"),
                                    P("Gestion des images véhicules et des 4 pièces justificatives. Validation taille (5 Mo) + extension (PDF/JPG/PNG).", "table_c")],
    [P("Fichiers statiques", "table_l"), P("WhiteNoise", "table_c"),
                                    P("Sert les fichiers statiques compressés depuis Python sans serveur web supplémentaire (Nginx).", "table_c")],
    [P("Tests", "table_l"),        P("pytest + pytest-django", "table_c"),
                                    P("28 tests (15 unitaires + 13 fonctionnels). Fixtures pytest pour isolation des données. Pas de dépendances externes.", "table_c")],
    [P("Serveur WSGI", "table_l"), P("Gunicorn", "table_c"),
                                    P("Serveur de production Python standard. Stable, performant, compatible Railway.", "table_c")],
    [P("Déploiement", "table_l"),  P("Railway + GitHub Actions CI", "table_c"),
                                    P("Détection automatique depuis GitHub. PostgreSQL plugin intégré. Variables d'environnement sécurisées.", "table_c")],
    [P("Versionning", "table_l"),  P("Git + GitHub (Git Flow)", "table_c"),
                                    P("Branches main/develop/feature. Conventional Commits. Tags sémantiques (v1.0.0, v1.1.0).", "table_c")],
]
story.append(make_table(tech_data, [3.5*cm, 4*cm, 9*cm]))
story.append(PageBreak())

# ─── 1d. User Stories ─────────────────────────────────────────────────────────
story.append(P("Question 1d — User Stories (toutes en statut Done)", "subsection"))
story.append(P(
    "13 User Stories développées et déployées. Chaque US est couverte par des tests "
    "unitaires et/ou fonctionnels. Toutes sont en statut <b>Done</b>.",
    "body"
))
story.append(SP(0.3))

us_data = [
    [P("ID", "table_h"), P("User Story", "table_h"), P("Critères d'acceptation", "table_h"), P("Statut", "table_h")],
    [P("US-01", "table_l"),
     P("En tant que visiteur, je veux consulter le catalogue de véhicules disponibles.", "table_c"),
     P("GET /vehicules/ retourne 200 avec la liste des véhicules disponibles. Filtre disponible=True appliqué.", "table_c"),
     P("✓ Done", "done")],
    [P("US-02", "table_l"),
     P("En tant que visiteur, je veux filtrer le catalogue par marque, mode, motorisation, prix max, km max et modèle.", "table_c"),
     P("Chaque paramètre GET est mappé à un lookup ORM via le dict FILTERS. Combinaison multiple supportée.", "table_c"),
     P("✓ Done", "done")],
    [P("US-03", "table_l"),
     P("En tant que visiteur, je veux consulter la fiche détail d'un véhicule avec ses caractéristiques complètes.", "table_c"),
     P("GET /vehicules/<pk>/ retourne 200 avec boîte, portes, puissance, consommation, prix affiché.", "table_c"),
     P("✓ Done", "done")],
    [P("US-04", "table_l"),
     P("En tant que visiteur, je veux créer un compte client pour pouvoir déposer des dossiers.", "table_c"),
     P("POST /compte/inscription/ crée le User, valide l'unicité de l'email, auto-login et redirige vers dashboard.", "table_c"),
     P("✓ Done", "done")],
    [P("US-05", "table_l"),
     P("En tant que client, je veux me connecter et me déconnecter de mon espace personnel.", "table_c"),
     P("POST /compte/connexion/ crée la session. POST /compte/deconnexion/ la détruit. Cookies sécurisés en prod.", "table_c"),
     P("✓ Done", "done")],
    [P("US-06", "table_l"),
     P("En tant que client connecté, je veux déposer un dossier d'achat avec mes 4 pièces justificatives.", "table_c"),
     P("POST /dossiers/creer/achat/<id>/ crée DossierAchat, valide 4 fichiers (5Mo max, PDF/JPG/PNG), statut=déposé.", "table_c"),
     P("✓ Done", "done")],
    [P("US-07", "table_l"),
     P("En tant que client connecté, je veux déposer un dossier de location LLD avec choix de durée et options.", "table_c"),
     P("POST /dossiers/creer/location/<id>/ crée DossierLocation. Durée 12/24/36/48 mois. Options assurance+25€, entretien+30€.", "table_c"),
     P("✓ Done", "done")],
    [P("US-08", "table_l"),
     P("En tant que client, je veux voir tous mes dossiers et leur statut depuis mon espace personnel.", "table_c"),
     P("GET /compte/dashboard/ liste dossiers achat+location du user. select_related pour éviter N+1. Pastilles de statut.", "table_c"),
     P("✓ Done", "done")],
    [P("US-09", "table_l"),
     P("En tant que client, je veux consulter le détail d'un de mes dossiers. Je ne peux pas voir celui d'un autre.", "table_c"),
     P("GET /dossiers/<type>/<pk>/ filtre client=request.user → 404 si tentative d'accès cross-user.", "table_c"),
     P("✓ Done", "done")],
    [P("US-10", "table_l"),
     P("En tant qu'admin, je veux voir tous les dossiers de tous les clients depuis le dashboard admin.", "table_c"),
     P("Si user.is_staff : aucun filtre client appliqué. Tous les dossiers achat+location visibles.", "table_c"),
     P("✓ Done", "done")],
    [P("US-11", "table_l"),
     P("En tant qu'admin, je veux changer le statut d'un dossier (en traitement / validé / refusé).", "table_c"),
     P("POST /dossiers/<type>/<pk>/ avec statut valide → update_fields=['statut']. PRG pattern pour éviter le double-submit.", "table_c"),
     P("✓ Done", "done")],
    [P("US-12", "table_l"),
     P("En tant qu'admin, je veux gérer le catalogue véhicules depuis l'interface d'administration Django.", "table_c"),
     P("/admin/vehicles/ avec VehiculeAdmin : list_filter, search_fields, list_editable(disponible). MarqueAdmin intégré.", "table_c"),
     P("✓ Done", "done")],
    [P("US-13", "table_l"),
     P("En tant qu'admin, je veux activer ou désactiver un véhicule depuis la liste du catalogue en un clic.", "table_c"),
     P("VehiculeAdmin.list_editable = ('disponible',) — modification directe depuis la liste sans ouvrir la fiche.", "table_c"),
     P("✓ Done", "done")],
]
story.append(make_table(us_data, [1.5*cm, 4.8*cm, 7.5*cm, 2.2*cm]))
story.append(PageBreak())

# ─── 1e. Tests ────────────────────────────────────────────────────────────────
story.append(P("Question 1e — Tests unitaires et fonctionnels (≥ 80 % de couverture)", "subsection"))
story.append(P(
    "Le projet comporte <b>28 tests</b> au total : 15 tests unitaires (une par composant) "
    "et 13 tests fonctionnels (scénarios bout-en-bout). "
    "Lancés via <code>python -m pytest -v</code> depuis la racine du projet.",
    "body"
))
story.append(SP(0.3))

story.append(P("<b>Tests unitaires (15 tests)</b>", "body_b"))
unit_data = [
    [P("Fichier", "table_h"), P("Test", "table_h"), P("Ce qui est vérifié", "table_h")],
    [P("vehicles/tests.py", "table_l"), P("test_str_vehicule", "table_c"), P("Représentation string du modèle Vehicule.", "table_c")],
    [P("vehicles/tests.py", "table_l"), P("test_prix_affiche", "table_c"), P("Property prix_affiche : affiche € ou €/mois selon le mode.", "table_c")],
    [P("vehicles/tests.py", "table_l"), P("test_recherche_par_mode", "table_c"), P("Filtre mode=achat exclut les véhicules location.", "table_c")],
    [P("vehicles/tests.py", "table_l"), P("test_filtre_prix_max_exclut", "table_c"), P("Filtre prix_max exclut les véhicules au-dessus du seuil.", "table_c")],
    [P("vehicles/tests.py", "table_l"), P("test_recherche_modele", "table_c"), P("Recherche textuelle icontains sur le champ modele.", "table_c")],
    [P("vehicles/tests.py", "table_l"), P("test_detail_vehicule", "table_c"), P("Vue détail retourne HTTP 200.", "table_c")],
    [P("accounts/tests.py", "table_l"), P("test_inscription_cree_un_user", "table_c"), P("POST inscription crée le User en base.", "table_c")],
    [P("accounts/tests.py", "table_l"), P("test_connexion_valide", "table_c"), P("POST connexion redirige (302) si identifiants valides.", "table_c")],
    [P("accounts/tests.py", "table_l"), P("test_dashboard_protege", "table_c"), P("Dashboard sans connexion → 302 vers login.", "table_c")],
    [P("accounts/tests.py", "table_l"), P("test_dashboard_accessible_si_connecte", "table_c"), P("Dashboard retourne 200 après login.", "table_c")],
    [P("dossiers/tests.py", "table_l"), P("test_creation_dossier_achat", "table_c"), P("POST dossier achat crée DossierAchat en base.", "table_c")],
    [P("dossiers/tests.py", "table_l"), P("test_creation_dossier_location", "table_c"), P("POST dossier location : durée et assurance persistées.", "table_c")],
    [P("dossiers/tests.py", "table_l"), P("test_fichier_trop_gros_rejete", "table_c"), P("Fichier > 5 Mo → erreur de formulaire sur le champ cni.", "table_c")],
    [P("dossiers/tests.py", "table_l"), P("test_creation_requiert_authentification", "table_c"), P("Création dossier sans login → 302.", "table_c")],
    [P("dossiers/tests.py", "table_l"), P("test_loyer_total_avec_options", "table_c"), P("loyer_total = base + 30 (assurance) + 25 (entretien).", "table_c")],
]
story.append(make_table(unit_data, [4*cm, 5*cm, 7.5*cm]))
story.append(SP(0.4))

story.append(P("<b>Tests fonctionnels bout-en-bout (13 tests — tests_fonctionnels.py)</b>", "body_b"))
story.append(P(
    "Les tests fonctionnels reproduisent des <b>scénarios utilisateur complets</b> : "
    "de la page d'accueil jusqu'à la vérification du résultat en base. "
    "Ils complètent les tests unitaires en validant l'intégration des couches.",
    "body"
))
story.append(SP(0.2))

func_data = [
    [P("Scénario", "table_h"), P("Test fonctionnel", "table_h"), P("Parcours simulé", "table_h")],
    [P("Accès public", "table_l"),    P("test_home_accessible_sans_connexion", "table_c"),  P("GET / → 200 sans être connecté.", "table_c")],
    [P("Accès public", "table_l"),    P("test_catalogue_accessible_et_affiche_vehicules", "table_c"), P("GET /vehicules/ → 200 + véhicule dans le contexte.", "table_c")],
    [P("Accès public", "table_l"),    P("test_fiche_vehicule_accessible_sans_connexion", "table_c"), P("GET /vehicules/<pk>/ → 200 + véhicule dans contexte.", "table_c")],
    [P("Inscription", "table_l"),     P("test_inscription_cree_compte_et_ouvre_session", "table_c"), P("POST inscription → compte créé + session ouverte automatiquement.", "table_c")],
    [P("Inscription", "table_l"),     P("test_inscription_redirige_vers_dashboard", "table_c"), P("POST inscription → redirection finale vers /compte/dashboard/.", "table_c")],
    [P("Parcours achat", "table_l"),  P("test_parcours_achat_complet", "table_c"), P("Login → catalogue → fiche → dossier achat → dashboard affiche le dossier.", "table_c")],
    [P("Parcours location", "table_l"), P("test_parcours_location_avec_options", "table_c"), P("Login → dossier LLD 24 mois avec assurance+entretien → loyer_total vérifié.", "table_c")],
    [P("Parcours location", "table_l"), P("test_detail_dossier_location_accessible", "table_c"), P("Création dossier location → GET détail → 200.", "table_c")],
    [P("Sécurité", "table_l"),        P("test_dashboard_redirige_si_non_connecte", "table_c"), P("GET dashboard sans session → 302 vers /compte/connexion/.", "table_c")],
    [P("Sécurité", "table_l"),        P("test_creation_dossier_exige_connexion", "table_c"), P("GET création dossier sans session → 302.", "table_c")],
    [P("Sécurité", "table_l"),        P("test_client_ne_peut_pas_voir_dossier_dautrui", "table_c"), P("Client A accède au dossier de client B → 404.", "table_c")],
    [P("Workflow admin", "table_l"),  P("test_admin_valide_un_dossier_client", "table_c"), P("Admin POST statut=valide → dossier.statut mis à jour en base.", "table_c")],
    [P("Workflow admin", "table_l"),  P("test_admin_voit_tous_les_dossiers_dans_dashboard", "table_c"), P("Admin dashboard → dossiers de tous les clients visibles.", "table_c")],
]
story.append(make_table(func_data, [3.5*cm, 5.5*cm, 7.5*cm]))
story.append(SP(0.4))

story.append(P(
    "<b>Résultat global :</b> 28/28 tests verts (<code>python -m pytest -v</code>). "
    "La couverture couvre les modèles, les vues, les formulaires, la validation de fichiers, "
    "les contrôles d'accès et les parcours utilisateur bout-en-bout.",
    "body"
))
story.append(PageBreak())

# ═══════════════════════════════════════════════════════════════════════════════
# DOSSIER 2 — DÉPLOIEMENT & SURVEILLANCE
# ═══════════════════════════════════════════════════════════════════════════════
story.append(P("Dossier 2 — Déploiement et surveillance de la solution", "section"))
story.append(HR())

# ─── 2.1. Déploiement + sécurité ─────────────────────────────────────────────
story.append(P("Question 2.1 — Déploiement et mesures de sécurité", "subsection"))

story.append(P("<b>Architecture de déploiement</b>", "body_b"))
story.append(P(
    "L'application est déployée sur <b>Railway</b> (cloud PaaS). "
    "Railway détecte automatiquement le projet Python via le <code>Procfile</code> "
    "et exécute la commande de démarrage définie dans <code>railway.json</code> :",
    "body"
))
story.append(P(
    "migrate --noinput → seed_data → collectstatic --noinput → gunicorn config.wsgi",
    "code"
))
story.append(SP(0.3))

story.append(P("<b>Base de données PostgreSQL (Railway)</b>", "body_b"))
story.append(P(
    "Railway fournit un plugin PostgreSQL qui injecte automatiquement la variable "
    "<code>DATABASE_URL</code> dans l'environnement de l'application. "
    "Le paramètre <code>dj_database_url.config()</code> dans <code>settings.py</code> "
    "parse cette URL et configure la connexion avec <code>conn_max_age=600</code> "
    "(connexions persistantes pour optimiser les performances).",
    "body"
))
story.append(SP(0.3))

story.append(P("<b>Variables d'environnement (5 variables requises en production)</b>", "body_b"))
env_data = [
    [P("Variable", "table_h"),           P("Valeur en production", "table_h"), P("Rôle", "table_h")],
    [P("SECRET_KEY", "table_l"),         P("Clé aléatoire 50+ chars", "table_c"), P("Signature des sessions et tokens CSRF. Ne jamais exposer.", "table_c")],
    [P("DEBUG", "table_l"),              P("False", "table_c"),                  P("Désactive le mode debug → pas de tracebacks exposés.", "table_c")],
    [P("ALLOWED_HOSTS", "table_l"),      P(".railway.app", "table_c"),           P("Protège contre les attaques de type Host Header Injection.", "table_c")],
    [P("CSRF_TRUSTED_ORIGINS", "table_l"), P("https://*.railway.app", "table_c"), P("Valide l'origine des POST derrière le proxy HTTPS Railway.", "table_c")],
    [P("DATABASE_URL", "table_l"),       P("postgresql://...(auto Railway)", "table_c"), P("Connexion PostgreSQL sécurisée. Injectée automatiquement.", "table_c")],
]
story.append(make_table(env_data, [4*cm, 4.5*cm, 8*cm]))
story.append(SP(0.4))

story.append(P("<b>Mesures de sécurité implémentées</b>", "body_b"))
sec_data = [
    [P("Menace / Risque", "table_h"), P("Protection mise en place", "table_h"), P("Localisation dans le code", "table_h")],
    [P("Accès non autorisé", "table_l"), P("@login_required sur toutes les vues protégées. Redirection vers /compte/connexion/.", "table_c"), P("accounts/views.py, dossiers/views.py", "table_c")],
    [P("Accès cross-user", "table_l"),   P("Filtre client=request.user dans les QuerySets. Accès au dossier d'autrui → 404.", "table_c"), P("dossiers/views.py:detail_dossier", "table_c")],
    [P("CSRF", "table_l"),               P("CsrfViewMiddleware actif. Token {% csrf_token %} dans tous les formulaires.", "table_c"), P("config/settings.py, tous les templates", "table_c")],
    [P("Injection SQL", "table_l"),      P("ORM Django — aucune requête SQL brute. Paramètres toujours échappés.", "table_c"), P("Toutes les vues (ORM uniquement)", "table_c")],
    [P("Upload malveillant", "table_l"), P("Validateur valider_document : taille ≤ 5 Mo, extension PDF/JPG/PNG uniquement.", "table_c"), P("dossiers/models.py:valider_document", "table_c")],
    [P("Fuite de session", "table_l"),   P("SESSION_COOKIE_SECURE=True + CSRF_COOKIE_SECURE=True si not DEBUG.", "table_c"), P("config/settings.py (bloc if not DEBUG)", "table_c")],
    [P("HTTPS forced", "table_l"),       P("SECURE_PROXY_SSL_HEADER lit X-Forwarded-Proto de Railway pour forcer HTTPS.", "table_c"), P("config/settings.py (bloc if not DEBUG)", "table_c")],
    [P("Mot de passe", "table_l"),       P("Django hache les mots de passe avec PBKDF2 + SHA256. Aucun stockage en clair.", "table_c"), P("django.contrib.auth (natif)", "table_c")],
    [P("Email dupliqué", "table_l"),     P("clean_email() vérifie User.objects.filter(email=email).exists() avant création.", "table_c"), P("accounts/forms.py:InscriptionForm", "table_c")],
    [P("Clé secrète exposée", "table_l"), P("SECRET_KEY lue depuis la variable d'environnement. Valeur par défaut uniquement en dev.", "table_c"), P("config/settings.py:SECRET_KEY", "table_c")],
]
story.append(make_table(sec_data, [4*cm, 7.5*cm, 5*cm]))
story.append(SP(0.4))

story.append(P("<b>Étapes de déploiement Railway (step by step)</b>", "body_b"))
deploy_steps = [
    ("1. Push GitHub", "git push origin main — Railway détecte automatiquement le push et lance le déploiement."),
    ("2. Plugin PostgreSQL", "Railway → projet → + Add → Database → Add PostgreSQL. DATABASE_URL est injectée automatiquement."),
    ("3. Variables d'environnement", "Railway → Variables → Raw Editor → ajouter SECRET_KEY, DEBUG=False, ALLOWED_HOSTS=.railway.app, CSRF_TRUSTED_ORIGINS."),
    ("4. Domaine public", "Railway → Settings → Networking → Generate Domain → récupérer l'URL publique."),
    ("5. Déploiement automatique", "railway.json exécute : migrate → seed_data → collectstatic → gunicorn. Application disponible."),
    ("6. Vérification", "Accéder au domaine → connexion admin/Admin123! → vérifier le catalogue et la création de dossier."),
]
for step, desc in deploy_steps:
    story.append(B(f"<b>{step}</b> : {desc}"))
story.append(SP(0.4))

# ─── 2.2. Surveillance & alerting ────────────────────────────────────────────
story.append(P("Question 2.2 — Surveillance, logs et gestion des erreurs", "subsection"))

story.append(P("<b>Logs applicatifs</b>", "body_b"))
story.append(P(
    "Gunicorn génère des logs de type <b>access log</b> (méthode, URL, statut HTTP, temps de réponse) "
    "et <b>error log</b> (exceptions Python, stack traces). "
    "Railway capture ces flux stdout/stderr et les centralise dans l'onglet <b>Logs</b> "
    "de chaque déploiement, accessibles en temps réel depuis le tableau de bord Railway.",
    "body"
))
story.append(SP(0.2))

story.append(P("<b>Gestion des erreurs 4xx/5xx</b>", "body_b"))
story.append(P(
    "Django lève automatiquement des exceptions HTTP standardisées :",
    "body"
))
story.append(B("<b>Http404</b> → pages introuvables ou accès cross-user refusé (dossiers/views.py)."))
story.append(B("<b>403 Forbidden</b> → protection CSRF si token invalide."))
story.append(B("<b>500 Internal Server Error</b> → exception non gérée, stacktrace dans les logs Gunicorn."))
story.append(SP(0.2))

story.append(P("<b>Configuration logging Django (settings.py)</b>", "body_b"))
story.append(P(
    "Django peut être configuré pour envoyer les erreurs par email (ADMINS + mail_admins handler) "
    "ou pour écrire dans un fichier de log. Dans notre configuration Railway, les logs Django "
    "sont envoyés vers stdout et capturés par Railway.",
    "body"
))
story.append(SP(0.2))

story.append(P("<b>Solution d'alerting — Sentry (recommandée pour la production)</b>", "body_b"))
story.append(P(
    "Pour une surveillance proactive, la mise en place de <b>Sentry</b> est recommandée :",
    "body"
))
sentry_steps = [
    "pip install sentry-sdk — ajouter à requirements.txt",
    "Ajouter SENTRY_DSN dans les variables d'environnement Railway",
    "Initialiser dans settings.py : sentry_sdk.init(dsn=os.environ.get('SENTRY_DSN'), traces_sample_rate=1.0)",
    "Sentry capture automatiquement toutes les exceptions Django avec contexte (user, URL, paramètres)",
    "Alertes email ou Slack configurables par seuil (ex : > 5 erreurs 500 en 5 minutes)",
    "Dashboard Sentry : graphiques d'erreurs, tendances, performance des vues Django",
]
for s in sentry_steps:
    story.append(B(s))
story.append(SP(0.3))

story.append(P("<b>Tableau de bord de surveillance (Railway)</b>", "body_b"))
monitor_data = [
    [P("Indicateur", "table_h"), P("Outil", "table_h"), P("Accès", "table_h")],
    [P("Logs temps réel", "table_l"),     P("Railway Logs", "table_c"),    P("Dashboard Railway → Deployments → Logs", "table_c")],
    [P("Statut des déploiements", "table_l"), P("Railway", "table_c"),     P("Déploiement OK / Failed avec historique", "table_c")],
    [P("Exceptions Python", "table_l"),   P("Sentry (SDK)", "table_c"),    P("sentry.io → Issues → Django exceptions", "table_c")],
    [P("Uptime / Disponibilité", "table_l"), P("Railway Health Check", "table_c"), P("Healthcheck automatique sur /", "table_c")],
    [P("Métriques de requêtes", "table_l"), P("Gunicorn access log", "table_c"), P("Visible dans les logs Railway", "table_c")],
    [P("Alertes critiques", "table_l"),   P("Sentry notifications", "table_c"), P("Email/Slack si seuil d'erreurs dépassé", "table_c")],
]
story.append(make_table(monitor_data, [4.5*cm, 4*cm, 8*cm]))
story.append(SP(0.4))

story.append(P("<b>Pratiques de correction de bugs</b>", "body_b"))
bug_steps = [
    ("Identification", "Lecture des logs Railway ou alertes Sentry. Le stacktrace identifie le fichier et la ligne."),
    ("Reproduction", "Créer un test unitaire ou fonctionnel qui reproduit le bug (test-first)."),
    ("Correction", "Modifier le code, vérifier que le test passe, vérifier que les 28 autres tests restent verts."),
    ("Commit", "git commit -m \"fix(<app>): description du correctif\" sur une branche fix/<description>."),
    ("Déploiement", "Merge dans develop → merge dans main → push → redéploiement automatique Railway."),
    ("Validation", "Vérifier en production que le comportement est corrigé. Le log Sentry indique zéro occurrence."),
]
for step, desc in bug_steps:
    story.append(B(f"<b>{step}</b> : {desc}"))

story.append(SP(0.6))
story.append(HR())
story.append(SP(0.3))
story.append(P(
    "<b>Lien GitHub :</b> https://github.com/PapEXito/m-motors  |  "
    "<b>App déployée :</b> https://m-motors-production.up.railway.app/  |  "
    "<b>Login :</b> admin / Admin123!",
    "caption"
))

# ─── Génération ───────────────────────────────────────────────────────────────
doc.build(story)
print(f"PDF généré : {OUTPUT}")
