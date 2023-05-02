from sqlalchemy.orm import Session
from app.models.Users import DB_User
from app.libraries import config
from app.api.base.libraries.hashing import Hash


def create_superadmin_account(engine):
    session = Session(bind=engine)
    existing_user = session.query(DB_User).filter_by(email=config.SUPER_ADMIN_EMAIL).first()
    if not existing_user:
        existing_user = DB_User(
            email=config.SUPER_ADMIN_EMAIL,
            password=Hash.bcrypt(config.SUPER_ADMIN_PASSWORD),
            first_name="Techincog",
            last_name=config.SUPER_ADMIN_FIRSTNAME,
            roles="superadmin",
        )
        session.add(existing_user)
        session.commit()
        session.refresh(existing_user)
        
        
        