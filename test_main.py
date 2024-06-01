from app.reabilitation_app import ReabilitationApp
from db.database import Base, engine

Base.metadata.create_all(bind=engine)

app = ReabilitationApp()
app.mainloop()
