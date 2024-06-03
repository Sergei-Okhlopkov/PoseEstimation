from app.reabilitation_app import ReabilitationApp
from db.crud import fill_db_data
from db.database import Base, engine

Base.metadata.create_all(bind=engine)
# fill_db_data()

app = ReabilitationApp()
app.mainloop()
