from database import engine, Base
import models  # necesario para que Base "conozca" los 3 modelos

Base.metadata.create_all(bind=engine)

