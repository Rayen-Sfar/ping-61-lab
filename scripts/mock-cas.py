 
from flask import Flask, request, redirect, render_string_template
import logging

app = Flask(__name__)
logger = logging.getLogger(__name__)

# Utilisateurs de test
TEST_USERS = {
    "student1": {
        "password": "pass123",
        "nom": "Dupont",
        "prenom": "Jean",
        "email": "student1@school.fr",
        "groupe": "2-SIO-A"
    },
    "teacher1": {
        "password": "pass123",
        "nom": "Martin",
        "prenom": "Marie",
        "email": "teacher1@school.fr",
        "groupe": "Teachers"
    }
}

@app.route('/cas/login', methods=['GET'])
def cas_login():
    """Affiche le formulaire de login CAS"""
    service = request.args.get('service', '')
    return f"""
    <html>
    <body>
        <h1>🔐 CAS Mock - Authentification</h1>
        <form method="POST">
            <input type="text" name="username" placeholder="Username" required>
            <input type="password" name="password" placeholder="Password" required>
            <input type="hidden" name="service" value="{service}">
            <button type="submit">Login</button>
        </form>
        <hr>
        <p><strong>Comptes de test :</strong></p>
        <ul>
            <li>student1 / pass123</li>
            <li>teacher1 / pass123</li>
        </ul>
    </body>
    </html>
    """

@app.route('/cas/login', methods=['POST'])
def cas_login_post():
    """Traite la soumission du formulaire"""
    username = request.form.get('username')
    password = request.form.get('password')
    service = request.form.get('service')
    
    # Valider credentials
    if username not in TEST_USERS or TEST_USERS[username]['password'] != password:
        return "❌ Identifiants invalides", 401
    
    # Générer un ticket ST-xxxx
    ticket = f"ST-{username}-{hash(username)}"
    
    # Rediriger vers le service avec le ticket
    return redirect(f"{service}?ticket={ticket}")

@app.route('/cas/validate', methods=['GET'])
def cas_validate():
    """Valide un ticket CAS"""
    ticket = request.args.get('ticket')
    service = request.args.get('service')
    
    if not ticket or not service:
        return """<?xml version="1.0" encoding="UTF-8"?>
        <cas:serviceResponse xmlns:cas="http://www.yale.edu/tp/cas">
            <cas:authenticationFailure code="INVALID_REQUEST">
                Ticket ou service manquant
            </cas:authenticationFailure>
        </cas:serviceResponse>
        """
    
    # Extraire username du ticket
    username = ticket.split('-')[1]
    
    if username not in TEST_USERS:
        return """<?xml version="1.0" encoding="UTF-8"?>
        <cas:serviceResponse xmlns:cas="http://www.yale.edu/tp/cas">
            <cas:authenticationFailure code="INVALID_TICKET">
                Ticket invalide
            </cas:authenticationFailure>
        </cas:serviceResponse>
        """
    
    user_info = TEST_USERS[username]
    
    # ✅ Retourner l'utilisateur avec attributs
    return f"""<?xml version="1.0" encoding="UTF-8"?>
    <cas:serviceResponse xmlns:cas="http://www.yale.edu/tp/cas">
        <cas:authenticationSuccess>
            <cas:user>{username}</cas:user>
            <cas:attributes>
                <cas:email>{user_info['email']}</cas:email>
                <cas:nom>{user_info['nom']}</cas:nom>
                <cas:prenom>{user_info['prenom']}</cas:prenom>
                <cas:groupe>{user_info['groupe']}</cas:groupe>
            </cas:attributes>
        </cas:authenticationSuccess>
    </cas:serviceResponse>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)