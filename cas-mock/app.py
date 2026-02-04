from flask import Flask, request, redirect, render_template_string
import logging
import os
import ldap3

app = Flask(__name__)
logger = logging.getLogger(__name__)

# Configuration LDAP
LDAP_HOST = os.getenv('LDAP_HOST', 'openldap')
LDAP_PORT = int(os.getenv('LDAP_PORT', '389'))
LDAP_BASE_DN = os.getenv('LDAP_BASE_DN', 'dc=esigelec,dc=fr')
LDAP_ADMIN_DN = os.getenv('LDAP_ADMIN_DN', 'cn=admin,dc=esigelec,dc=fr')
LDAP_ADMIN_PASSWORD = os.getenv('LDAP_ADMIN_PASSWORD', 'admin')

# Stockage temporaire des tickets
tickets = {}

def authenticate_ldap(username, password):
    """Authentifier un utilisateur contre LDAP"""
    try:
        server = ldap3.Server(f'ldap://{LDAP_HOST}:{LDAP_PORT}', get_info=ldap3.ALL)
        
        # Rechercher l'utilisateur
        conn = ldap3.Connection(server, LDAP_ADMIN_DN, LDAP_ADMIN_PASSWORD, auto_bind=True)
        conn.search(
            search_base=LDAP_BASE_DN,
            search_filter=f'(uid={username})',
            attributes=['uid', 'cn', 'sn', 'givenName', 'mail']
        )
        
        if not conn.entries:
            logger.warning(f"Utilisateur {username} non trouvé dans LDAP")
            return None
        
        entry = conn.entries[0]
        user_dn = entry.entry_dn
        
        # Tenter de se connecter avec les credentials de l'utilisateur
        user_conn = ldap3.Connection(server, user_dn, password)
        if not user_conn.bind():
            logger.warning(f"Mot de passe incorrect pour {username}")
            return None
        
        # Extraire les attributs
        user_info = {
            'username': str(entry.uid),
            'cn': str(entry.cn) if hasattr(entry, 'cn') else username,
            'sn': str(entry.sn) if hasattr(entry, 'sn') else '',
            'givenName': str(entry.givenName) if hasattr(entry, 'givenName') else '',
            'mail': str(entry.mail) if hasattr(entry, 'mail') else f'{username}@esigelec.fr'
        }

        # Chercher les groupes (groupOfNames, posixGroup)
        groups = []
        try:
            # groupOfNames : member = user DN
            conn.search(
                search_base=LDAP_BASE_DN,
                search_filter=f'(member={user_dn})',
                attributes=['cn']
            )
            for g in conn.entries:
                if hasattr(g, 'cn'):
                    groups.append(str(g.cn))
        except Exception:
            pass

        try:
            # posixGroup : memberUid = username
            conn.search(
                search_base=LDAP_BASE_DN,
                search_filter=f'(objectClass=posixGroup)',
                attributes=['cn', 'memberUid']
            )
            for g in conn.entries:
                if hasattr(g, 'memberUid') and str(username) in str(g.memberUid):
                    if hasattr(g, 'cn'):
                        groups.append(str(g.cn))
        except Exception:
            pass

        # Déduire un attribut 'groups' pour la réponse
        if groups:
            # dédupliquer
            user_info['groups'] = sorted(list(set(groups)))

        logger.info(f"✅ Authentification LDAP réussie pour {username} - groups={user_info.get('groups')}")
        return user_info
        
    except Exception as e:
        logger.error(f"❌ Erreur LDAP: {str(e)}")
        return None

LOGIN_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>CAS Login - ESIGELEC</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .login-box {
            background: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.2);
            width: 350px;
        }
        h1 {
            text-align: center;
            color: #333;
            margin-bottom: 30px;
        }
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            color: #555;
            font-weight: bold;
        }
        input[type="text"], input[type="password"] {
            width: 100%;
            padding: 12px;
            border: 2px solid #ddd;
            border-radius: 5px;
            font-size: 14px;
            box-sizing: border-box;
        }
        input[type="text"]:focus, input[type="password"]:focus {
            outline: none;
            border-color: #667eea;
        }
        button {
            width: 100%;
            padding: 12px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 5px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            transition: transform 0.2s;
        }
        button:hover {
            transform: translateY(-2px);
        }
        .error {
            background: #fee;
            color: #c33;
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 20px;
            text-align: center;
        }
        .info {
            background: #e3f2fd;
            padding: 15px;
            border-radius: 5px;
            margin-top: 20px;
            font-size: 12px;
        }
        .info strong {
            display: block;
            margin-bottom: 5px;
        }
    </style>
</head>
<body>
    <div class="login-box">
        <h1>🔐 CAS Login</h1>
        {% if error %}
        <div class="error">{{ error }}</div>
        {% endif %}
        <form method="POST">
            <div class="form-group">
                <label for="username">Identifiant</label>
                <input type="text" id="username" name="username" required autofocus>
            </div>
            <div class="form-group">
                <label for="password">Mot de passe</label>
                <input type="password" id="password" name="password" required>
            </div>
            <input type="hidden" name="service" value="{{ service }}">
            <button type="submit">Se connecter</button>
        </form>
        <div class="info">
            <strong>Comptes de test:</strong>
            • student1 / password123<br>
            • teacher1 / password123
        </div>
    </div>
</body>
</html>
"""

@app.route('/cas/login', methods=['GET'])
def cas_login():
    """Affiche le formulaire de login CAS"""
    service = request.args.get('service', '')
    error = request.args.get('error', '')
    return render_template_string(LOGIN_TEMPLATE, service=service, error=error)

@app.route('/cas/login', methods=['POST'])
def cas_login_post():
    """Traite la soumission du formulaire"""
    username = request.form.get('username')
    password = request.form.get('password')
    service = request.form.get('service')
    
    # Authentifier contre LDAP
    user_info = authenticate_ldap(username, password)
    
    if not user_info:
        return redirect(f'/cas/login?service={service}&error=Identifiants invalides')
    
    # Générer un ticket ST-xxxx
    import hashlib
    import time
    ticket = f"ST-{hashlib.md5(f'{username}{time.time()}'.encode()).hexdigest()[:16]}"
    
    # Stocker le ticket avec les infos utilisateur
    tickets[ticket] = user_info
    
    # Rediriger vers le service avec le ticket
    separator = '&' if '?' in service else '?'
    return redirect(f"{service}{separator}ticket={ticket}")

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
    
    # Vérifier le ticket
    user_info = tickets.get(ticket)
    
    if not user_info:
        return """<?xml version="1.0" encoding="UTF-8"?>
        <cas:serviceResponse xmlns:cas="http://www.yale.edu/tp/cas">
            <cas:authenticationFailure code="INVALID_TICKET">
                Ticket invalide ou expiré
            </cas:authenticationFailure>
        </cas:serviceResponse>
        """
    
    # Supprimer le ticket (usage unique)
    del tickets[ticket]

    # Préparer un éventuel champ 'groups' (CSV) si présent
    groups_xml = ''
    if 'groups' in user_info and user_info['groups']:
        groups_xml = f"\n                <cas:groups>{','.join(user_info['groups'])}</cas:groups>"

    # Retourner l'utilisateur avec attributs (ajoute <cas:groups> si disponible)
    return f"""<?xml version="1.0" encoding="UTF-8"?>
    <cas:serviceResponse xmlns:cas="http://www.yale.edu/tp/cas">
        <cas:authenticationSuccess>
            <cas:user>{user_info['username']}</cas:user>
            <cas:attributes>
                <cas:email>{user_info['mail']}</cas:email>
                <cas:nom>{user_info['sn']}</cas:nom>
                <cas:prenom>{user_info['givenName']}</cas:prenom>
                <cas:cn>{user_info['cn']}</cas:cn>{groups_xml}
            </cas:attributes>
        </cas:authenticationSuccess>
    </cas:serviceResponse>
    """

@app.route('/health')
def health():
    return {'status': 'ok', 'service': 'CAS Mock with LDAP'}

@app.route('/ldap/authenticate', methods=['POST'])
def ldap_authenticate():
    """Endpoint pour authentification LDAP directe (sans ticket CAS)"""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return {'error': 'Username and password required'}, 400
    
    # Authentifier contre LDAP
    user_info = authenticate_ldap(username, password)
    
    if not user_info:
        return {'error': 'Invalid credentials'}, 401
    
    return user_info, 200

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    app.run(host='0.0.0.0', port=8080, debug=True)
