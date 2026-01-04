 
import httpx
import logging
from typing import Optional, Dict
from urllib.parse import urlencode, parse_qs, urlparse

logger = logging.getLogger(__name__)

class CASService:
    """
    Service d'intégration CAS selon le protocole CAS v2/v3
    Documentation : https://apereo.github.io/cas/
    """
    
    def __init__(
        self,
        cas_server_url: str,
        service_url: str,
        validate_path: str = "/cas/validate"
    ):
        self.cas_server_url = cas_server_url.rstrip('/')
        self.service_url = service_url
        self.validate_path = validate_path
        self.validate_url = f"{self.cas_server_url}{validate_path}"
        
    async def validate_ticket(self, ticket: str) -> Optional[Dict]:
        """
        ✅ Étape 2 du flux CAS : Valider le ticket auprès du serveur CAS
        
        Paramètres :
            ticket : Le ticket CAS reçu en URL (ST-xxxxx)
        
        Retour :
            {
                "username": "student@school.fr",
                "attributes": {
                    "nom": "Dupont",
                    "prenom": "Jean",
                    "groupe": "2-SIO-A",
                    "email": "student@school.fr"
                }
            }
        """
        
        try:
            params = {
                'service': self.service_url,
                'ticket': ticket
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    self.validate_url,
                    params=params,
                    timeout=10
                )
            
            if response.status_code != 200:
                logger.error(f"❌ CAS validation failed: {response.status_code}")
                return None
            
            # Parse CAS response (format CAS 2.0)
            user_data = self._parse_cas_response(response.text)
            
            if user_data:
                logger.info(f"✅ CAS validation successful for {user_data['username']}")
            else:
                logger.warning("❌ Invalid CAS response format")
            
            return user_data
            
        except Exception as e:
            logger.error(f"❌ CAS validation error: {str(e)}")
            return None
    
    def _parse_cas_response(self, response_text: str) -> Optional[Dict]:
        """
        Parse la réponse XML du serveur CAS
        
        Format attendu :
        <cas:serviceResponse>
          <cas:authenticationSuccess>
            <cas:user>student@school.fr</cas:user>
            <cas:attributes>
              <cas:nom>Dupont</cas:nom>
              <cas:prenom>Jean</cas:prenom>
            </cas:attributes>
          </cas:authenticationSuccess>
        </cas:serviceResponse>
        """
        
        try:
            import xml.etree.ElementTree as ET
            
            root = ET.fromstring(response_text)
            
            # Namespace CAS
            ns = {
                'cas': 'http://www.yale.edu/tp/cas'
            }
            
            # Chercher le nœud authenticationSuccess
            success_node = root.find('.//cas:authenticationSuccess', ns)
            
            if success_node is None:
                return None
            
            # Extraire username
            user_elem = success_node.find('cas:user', ns)
            username = user_elem.text if user_elem is not None else None
            
            if not username:
                return None
            
            # Extraire attributs
            attributes = {}
            attr_node = success_node.find('cas:attributes', ns)
            
            if attr_node is not None:
                for attr in attr_node:
                    key = attr.tag.replace('{http://www.yale.edu/tp/cas}', '')
                    attributes[key] = attr.text
            
            return {
                "username": username,
                "attributes": attributes
            }
            
        except Exception as e:
            logger.error(f"❌ Error parsing CAS response: {str(e)}")
            return None