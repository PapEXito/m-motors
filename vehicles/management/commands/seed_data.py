"""
commande `python manage.py seed_data` qui réinitialise la DB avec 25 voitures réelles + comptes admin/client
permet de démarrer une démo locale ou Railway avec un catalogue prêt en une commande indispensable au release Railway
écrit dans vehicles/models.py Marque/Vehicule, crée les User admin/client, exécuté par railway.json au déploy
"""
from decimal import Decimal

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils.text import slugify

from vehicles.models import Marque, Vehicule

"""
sources des data utilisées officielle marché pour réalisme maximum via https://www.lacentrale.fr/
j'ai copier collé un format normalisé pour chaque véhicules et via un filtre python l'importation était auto
chaque véhicules doit respecter ce format noramliser de data puur être importé automatiquement dans le catalogue
"""

VEHICULES = [
    {
        "nom_complet": "AUDI R8 II (2) 5.2 V10 FSI 620 PERFORMANCE QUATTRO S TRONIC 7",
        "marque": "Audi", "modele": "R8 II (2) 5.2 V10 FSI 620 PERFORMANCE QUATTRO S TRONIC 7",
        "annee": 2019, "kilometrage": 23118, "motorisation": "essence", "prix_vente": 184980,
        "boite": "Automatique", "portes": 2, "puissance_fiscale": "56 CV", "puissance_din": "620 ch", "consommation": "13,1 L /100 km",
    },
    {
        "nom_complet": "PEUGEOT 208 (2) 1.2 PURETECH 82 URBAN SOUL 5P",
        "marque": "Peugeot", "modele": "208 (2) 1.2 PURETECH 82 URBAN SOUL 5P",
        "annee": 2015, "kilometrage": 123400, "motorisation": "essence", "prix_vente": 3990,
        "boite": "Manuelle", "portes": 5, "puissance_fiscale": "4 CV", "puissance_din": "82 ch", "consommation": "3,9 L /100 km",
    },
    {
        "nom_complet": "BMW SERIE 1 (F20) (2) 120I 184 LOUNGE 5P BVA8",
        "marque": "BMW", "modele": "SERIE 1 (F20) (2) 120I 184 LOUNGE 5P BVA8",
        "annee": 2018, "kilometrage": 48900, "motorisation": "essence", "prix_vente": 20900,
        "boite": "Automatique", "portes": 5, "puissance_fiscale": "10 CV", "puissance_din": "184 ch", "consommation": "5,7 L /100 km",
    },
    {
        "nom_complet": "RENAULT TWINGO II 1.2 LEV 16V 75 YAHOO! ECO2",
        "marque": "Renault", "modele": "TWINGO II 1.2 LEV 16V 75 YAHOO! ECO2",
        "annee": 2011, "kilometrage": 125000, "motorisation": "essence", "prix_vente": 3990,
        "boite": "Manuelle", "portes": 3, "puissance_fiscale": "4 CV", "puissance_din": "76 ch", "consommation": "4,7 L /100 km",
    },
    {
        "nom_complet": "RENAULT CLIO III (2) 1.2 TCE 100 EXCEPTION TOMTOM 5P EURO5",
        "marque": "Renault", "modele": "CLIO III (2) 1.2 TCE 100 EXCEPTION TOMTOM 5P EURO5",
        "annee": 2012, "kilometrage": 110000, "motorisation": "essence", "prix_vente": 6290,
        "boite": "Manuelle", "portes": 5, "puissance_fiscale": "6 CV", "puissance_din": "101 ch", "consommation": "5,5 L /100 km",
    },
    {
        "nom_complet": "AUDI A1 (2) SPORTBACK 1.0 TFSI 95 ULTRA BUSINESS LINE S TRONIC",
        "marque": "Audi", "modele": "A1 (2) SPORTBACK 1.0 TFSI 95 ULTRA BUSINESS LINE S TRONIC",
        "annee": 2017, "kilometrage": 121094, "motorisation": "essence", "prix_vente": 11590,
        "boite": "Automatique", "portes": 5, "puissance_fiscale": "5 CV", "puissance_din": "95 ch", "consommation": "3,8 L /100 km",
    },
    {
        "nom_complet": "VOLKSWAGEN POLO IV (2) TDI 70 CONFORTLINE 5P",
        "marque": "Volkswagen", "modele": "POLO IV (2) TDI 70 CONFORTLINE 5P",
        "annee": 2008, "kilometrage": 347000, "motorisation": "diesel", "prix_vente": 1990,
        "boite": "Manuelle", "portes": 5, "puissance_fiscale": "4 CV", "puissance_din": "69 ch", "consommation": "3,9 L /100 km",
    },
    {
        "nom_complet": "VOLKSWAGEN GOLF VII (2) 1.5 TSI EVO 150 MATCH DSG7",
        "marque": "Volkswagen", "modele": "GOLF VII (2) 1.5 TSI EVO 150 MATCH DSG7",
        "annee": 2019, "kilometrage": 139000, "motorisation": "essence", "prix_vente": 13490,
        "boite": "Automatique", "portes": 5, "puissance_fiscale": "7 CV", "puissance_din": "150 ch", "consommation": "5,1 L /100 km",
    },
    {
        "nom_complet": "PEUGEOT 307 (2) CC 2.0 16S SPORT",
        "marque": "Peugeot", "modele": "307 (2) CC 2.0 16S SPORT",
        "annee": 2006, "kilometrage": 131000, "motorisation": "essence", "prix_vente": 3990,
        "boite": "Manuelle", "portes": 2, "puissance_fiscale": "9 CV", "puissance_din": "140 ch", "consommation": "6,2 L /100 km",
    },
    {
        "nom_complet": "BMW SERIE 1 (E87) (2) 116D 115 EDITION 5P",
        "marque": "BMW", "modele": "SERIE 1 (E87) (2) 116D 115 EDITION 5P",
        "annee": 2011, "kilometrage": 217000, "motorisation": "diesel", "prix_vente": 5990,
        "boite": "Manuelle", "portes": 5, "puissance_fiscale": "6 CV", "puissance_din": "116 ch", "consommation": "4,5 L /100 km",
    },
    {
        "nom_complet": "BMW SERIE 3 (G81) TOURING 3.0 510 M3 COMPETITION M XDRIVE BVA8",
        "marque": "BMW", "modele": "SERIE 3 (G81) TOURING 3.0 510 M3 COMPETITION M XDRIVE BVA8",
        "annee": 2023, "kilometrage": 23616, "motorisation": "essence", "prix_vente": 89900,
        "boite": "Automatique", "portes": 5, "puissance_fiscale": "41 CV", "puissance_din": "510 ch", "consommation": "10,1 L /100 km",
    },
    {
        "nom_complet": "BMW SERIE 4 (F32) COUPE 420DA 184 SPORT",
        "marque": "BMW", "modele": "SERIE 4 (F32) COUPE 420DA 184 SPORT",
        "annee": 2016, "kilometrage": 88000, "motorisation": "diesel", "prix_vente": 18300,
        "boite": "Automatique", "portes": 2, "puissance_fiscale": "10 CV", "puissance_din": "184 ch", "consommation": "4,6 L /100 km",
    },
    {
        "nom_complet": "BMW SERIE 5 (F11) TOURING 523I 204 CONFORT",
        "marque": "BMW", "modele": "SERIE 5 (F11) TOURING 523I 204 CONFORT",
        "annee": 2011, "kilometrage": 80830, "motorisation": "essence", "prix_vente": 15400,
        "boite": "Manuelle", "portes": 5, "puissance_fiscale": "12 CV", "puissance_din": "204 ch", "consommation": "7,9 L /100 km",
    },
    {
        "nom_complet": "AUDI A5 SPORTBACK 3.0 V6 TDI 240 DPF AMBITION LUXE QUATTRO S TRONIC",
        "marque": "Audi", "modele": "A5 SPORTBACK 3.0 V6 TDI 240 DPF AMBITION LUXE QUATTRO S TRONIC",
        "annee": 2010, "kilometrage": 321343, "motorisation": "diesel", "prix_vente": 5990,
        "boite": "Automatique", "portes": 5, "puissance_fiscale": "15 CV", "puissance_din": "239 ch", "consommation": "5,7 L /100 km",
    },
    {
        "nom_complet": "AUDI TT COUPE 3.2 V6 QUATTRO DSG",
        "marque": "Audi", "modele": "TT COUPE 3.2 V6 QUATTRO DSG",
        "annee": 2006, "kilometrage": 178000, "motorisation": "essence", "prix_vente": 11990,
        "boite": "Automatique", "portes": 3, "puissance_fiscale": "16 CV", "puissance_din": "250 ch", "consommation": "7,3 L /100 km",
    },
    {
        "nom_complet": "AUDI A1 SPORTBACK 1.6 TDI 90 AMBITION",
        "marque": "Audi", "modele": "A1 SPORTBACK 1.6 TDI 90 AMBITION",
        "annee": 2012, "kilometrage": 155600, "motorisation": "diesel", "prix_vente": 6990,
        "boite": "Manuelle", "portes": 5, "puissance_fiscale": "4 CV", "puissance_din": "90 ch", "consommation": "3,4 L /100 km",
    },
    {
        "nom_complet": "PEUGEOT RCZ 1.6 THP 156 BVA6",
        "marque": "Peugeot", "modele": "RCZ 1.6 THP 156 BVA6",
        "annee": 2011, "kilometrage": 150000, "motorisation": "essence", "prix_vente": 7490,
        "boite": "Automatique", "portes": 2, "puissance_fiscale": "9 CV", "puissance_din": "156 ch", "consommation": "5,5 L /100 km",
    },
    {
        "nom_complet": "PEUGEOT PARTNER II (2) 1.6 BLUEHDI 100CH PREMIUM PACK",
        "marque": "Peugeot", "modele": "PARTNER II (2) 1.6 BLUEHDI 100CH PREMIUM PACK",
        "annee": 2018, "kilometrage": 130000, "motorisation": "diesel", "prix_vente": 8490,
        "boite": "Manuelle", "portes": 4, "puissance_fiscale": "5 CV", "puissance_din": "99 ch", "consommation": "3,9 L /100 km",
    },
    {
        "nom_complet": "PEUGEOT 107 (2) 1.0 TRENDY 5P",
        "marque": "Peugeot", "modele": "107 (2) 1.0 TRENDY 5P",
        "annee": 2010, "kilometrage": 52970, "motorisation": "essence", "prix_vente": 5480,
        "boite": "Manuelle", "portes": 5, "puissance_fiscale": "4 CV", "puissance_din": "68 ch", "consommation": "3,9 L /100 km",
    },
    {
        "nom_complet": "RENAULT CLIO II (2) CAMPUS 1.2 16S 5P",
        "marque": "Renault", "modele": "CLIO II (2) CAMPUS 1.2 16S 5P",
        "annee": 2005, "kilometrage": 140000, "motorisation": "essence", "prix_vente": 3990,
        "boite": "Manuelle", "portes": 5, "puissance_fiscale": "5 CV", "puissance_din": "75 ch", "consommation": "5,9 L /100 km",
    },
    {
        "nom_complet": "RENAULT SCENIC III (3) 1.2 TCE 130 ENERGY LOUNGE",
        "marque": "Renault", "modele": "SCENIC III (3) 1.2 TCE 130 ENERGY LOUNGE",
        "annee": 2015, "kilometrage": 85000, "motorisation": "essence", "prix_vente": 7990,
        "boite": "Manuelle", "portes": 5, "puissance_fiscale": "7 CV", "puissance_din": "130 ch", "consommation": "6,6 L /100 km",
    },
    {
        "nom_complet": "RENAULT TWINGO II 1.2 TCE 100 GT",
        "marque": "Renault", "modele": "TWINGO II 1.2 TCE 100 GT",
        "annee": 2007, "kilometrage": 210000, "motorisation": "essence", "prix_vente": 2490,
        "boite": "Manuelle", "portes": 3, "puissance_fiscale": "6 CV", "puissance_din": "101 ch", "consommation": "4,9 L /100 km",
    },
    {
        "nom_complet": "VOLKSWAGEN UP! 1.0 75 WHITE UP! 3P",
        "marque": "Volkswagen", "modele": "UP! 1.0 75 WHITE UP! 3P",
        "annee": 2012, "kilometrage": 61200, "motorisation": "essence", "prix_vente": 5680,
        "boite": "Manuelle", "portes": 3, "puissance_fiscale": "4 CV", "puissance_din": "75 ch", "consommation": "4 L /100 km",
    },
    {
        "nom_complet": "VOLKSWAGEN GOLF VII (2) 1.5 TSI EVO 150 7CV BLUEMOTION TECHNOLOGY 8CV CARAT BV6 5P",
        "marque": "Volkswagen", "modele": "GOLF VII (2) 1.5 TSI EVO 150 7CV BLUEMOTION TECHNOLOGY 8CV CARAT BV6 5P",
        "annee": 2021, "kilometrage": 42000, "motorisation": "essence", "prix_vente": 22900,
        "boite": "Manuelle", "portes": 5, "puissance_fiscale": "8 CV", "puissance_din": "150 ch", "consommation": "5,7 L /100 km",
    },
    {
        "nom_complet": "VOLKSWAGEN POLO V (2) 1.2 TSI 90 BLUEMOTION TECHNOLOGY LOUNGE DSG7 5P",
        "marque": "Volkswagen", "modele": "POLO V (2) 1.2 TSI 90 BLUEMOTION TECHNOLOGY LOUNGE DSG7 5P",
        "annee": 2016, "kilometrage": 85974, "motorisation": "essence", "prix_vente": 11990,
        "boite": "Automatique", "portes": 5, "puissance_fiscale": "5 CV", "puissance_din": "90 ch", "consommation": "4,1 L /100 km",
    },
]

"""
champs communs vente/LLD extraits une fois pour éviter de répéter la liste
tout ce qui diffère (mode, prix_vente, loyer_mensuel) est ajouté par le caller

commande de management custom, lancée avec python manage.py seed_data
cette voie évite de mettre du seed dans les migrations
https://docs.djangoproject.com/en/6.0/howto/custom-management-commands/
"""

SHARED_FIELDS = ("modele", "nom_complet", "annee", "kilometrage", "motorisation",
                 "boite", "portes", "puissance_fiscale", "puissance_din", "consommation")


"""
on supprime tout, CASCADE emporte les véhicules avec. Plus simple qu'un diff,
le seed se rejoue à blanc à chaque fois.

set des marques uniques + get_or_create : pas de doublon même si la liste source en a.

petite factory locale qui construit le dict commun aux deux modes achat ET location
slugify(nom_complet) donne une clé d'image stable côté static
https://docs.djangoproject.com/en/6.0/ref/utils/#django.utils.text.slugify
"""
class Command(BaseCommand):
    help = "Réinitialise la base avec les 25 véhicules réels."

    def handle(self, *args, **options):
        Marque.objects.all().delete()
        
        marques = {
            nom: Marque.objects.get_or_create(nom=nom)[0]
            for nom in {v["marque"] for v in VEHICULES}
        }


        def base(v):
            return {
                "marque": marques[v["marque"]],
                "image_slug": slugify(v["nom_complet"]),
                **{f: v[f] for f in SHARED_FIELDS},
            }

        # passe 1 tous les véhicules en mode ACHAT avec leur prix réel
        for v in VEHICULES:
            Vehicule.objects.create(**base(v),
                mode=Vehicule.ModeChoices.ACHAT,
                prix_vente=Decimal(v["prix_vente"]))

        # passe 2 les 10 plus chers reproposés en LOCATION Choix produit : la LLD c'est
        # surtout du premium (Audi/BMW...), donc on filtre par prix ~~1.5% du prix d'achat
        # = grosse louche pour un loyer 48 mois avec valeur résiduelle ça suffit pour la démo
        top10 = sorted(VEHICULES, key=lambda v: v["prix_vente"], reverse=True)[:10]
        for v in top10:
            Vehicule.objects.create(**base(v),
                mode=Vehicule.ModeChoices.LOCATION,
                loyer_mensuel=Decimal(round(v["prix_vente"] * 0.015)))

        # comptes de démo créés seulement s'ils n'existent pas comme ça si on change un
        # mot de passe à la main entre deux seeds rien n'est pas écrasé
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser("admin", "admin@mmotors.fr", "Admin123!")
        if not User.objects.filter(username="client").exists():
            User.objects.create_user("client", "client@test.fr", "Client123!")

        self.stdout.write(self.style.SUCCESS(f"Seed OK : {len(VEHICULES)} véhicules. admin/Admin123! client/Client123!"))
