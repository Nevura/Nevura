from fastapi import Request, HTTPException
from fastapi.responses import RedirectResponse
from ..services.session import revoke_all_sessions, create_session, find_session
from ..services.mail import send_security_alert_email
from ..utils.geoip import get_geoip_info  # à créer ou utiliser une API externe
from jose import jwt
from ..utils.security import encrypt_token
import logging

@router.get("/oauth/callback")
async def oauth_callback(request: Request, code: str):
    ip = request.client.host
    user_agent = request.headers.get("user-agent", "unknown")

    tokens = await exchange_code_for_tokens(code)
    id_token = tokens.get("id_token")
    access_token = tokens.get("access_token")
    refresh_token = tokens.get("refresh_token")

    claims = jwt.get_unverified_claims(id_token)
    email = claims.get("email")
    if not email:
        raise HTTPException(status_code=400, detail="Email non fourni")

    user = await get_user_by_email(email)
    if not user:
        # créer user
        user = User(username=email.split("@")[0], email=email, hashed_password="", is_admin=False)

    with get_db_session() as db:
        # Vérifier session existante
        existing_session = find_session(db, user.id, user_agent, ip)

        if not existing_session:
            # Nouvelle session inconnue -> Révoquer toutes les sessions et tokens OAuth
            revoke_all_sessions(db, user.id)
            user.oauth_access_token = None
            user.oauth_refresh_token = None
            db.add(user)
            db.commit()

            # Envoi notification alerte intrusion
            geo_info = get_geoip_info(ip)
            subject = "Alerte de sécurité : tentative d'intrusion"
            html_content = f"""
                <p>Une tentative d'intrusion a été détectée sur votre compte :</p>
                <ul>
                    <li><b>IP :</b> {ip}</li>
                    <li><b>Localisation approximative :</b> {geo_info}</li>
                    <li><b>Navigateur :</b> {user_agent}</li>
                    <li><b>Date :</b> {datetime.utcnow()}</li>
                </ul>
                <p>Veuillez contacter immédiatement l'administrateur et changer vos mots de passe rapidement</p>
            """
            try:
                await send_security_alert_email(user.email, subject, html_content)
            except Exception as e:
                logging.error(f"Erreur envoi mail alerte sécurité: {e}")

        # Encrypt tokens et sauvegarder
        user.oauth_access_token = encrypt_token(access_token)
        user.oauth_refresh_token = encrypt_token(refresh_token)
        db.add(user)
        db.commit()

        # Créer JWT
        jwt_token = create_access_token({"sub": str(user.id), "email": user.email})

        # Créer nouvelle session
        create_session(db, user.id, user_agent, ip, jwt_token)

    return RedirectResponse(url=f"/?token={jwt_token}")

async def notify_admins(session: Session, target_user: User, ip: str, geo_info: str, user_agent: str):
    statement = select(User).where(User.is_admin == True, User.email != None)
    admins = session.exec(statement).all()
    subject = f"[Sécurité] Tentative d'intrusion détectée sur le compte {target_user.username}"
    html_content = f"""
        <p>Une tentative d'intrusion a été détectée sur le compte utilisateur <b>{target_user.username}</b> ({target_user.email}):</p>
        <ul>
            <li><b>IP :</b> {ip}</li>
            <li><b>Localisation approximative :</b> {geo_info}</li>
            <li><b>Navigateur et OS :</b> {user_agent}</li>
            <li><b>Date :</b> {datetime.utcnow()}</li>
        </ul>
        <p>Merci de contacter l'utilisateur pour l'aider à sécuriser son compte.</p>
    """
    for admin in admins:
        try:
            await send_security_alert_email(admin.email, subject, html_content)
        except Exception as e:
            # log erreur
            print(f"Erreur envoi mail admin {admin.email}: {e}")