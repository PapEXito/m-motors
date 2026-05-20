@echo off
echo ============================================
echo    M-Motors - Lancement local
echo ============================================
echo.

if not exist venv (
    echo [1/5] Creation de l'environnement virtuel...
    python -m venv venv
) else (
    echo [1/5] Environnement virtuel existant detecte.
)

call venv\Scripts\activate.bat

echo [2/5] Installation des dependances...
pip install -r requirements.txt -q

echo [3/5] Migration de la base de donnees...
python manage.py migrate --noinput

echo [4/5] Injection des donnees de demonstration...
python manage.py seed_data

echo [5/5] Demarrage du serveur...
echo.
echo  Site         : http://127.0.0.1:8000
echo  Admin Django : http://127.0.0.1:8000/admin/
echo  Identifiants : admin / Admin123!    ou    client / Client123!
echo.
echo  NOTE: En production, definir DATABASE_URL pour utiliser PostgreSQL.
echo  Localement, SQLite est utilise pour la demonstration.
echo.
start http://127.0.0.1:8000
python manage.py runserver

pause
