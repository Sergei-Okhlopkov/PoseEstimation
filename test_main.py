from app.reabilitation_app import ReabilitationApp
from db.database import SessionLocal
from db.database import Base, engine

Base.metadata.create_all(bind=engine)

app = ReabilitationApp(SessionLocal)
app.mainloop()
