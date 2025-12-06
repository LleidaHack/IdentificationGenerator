from fastapi import FastAPI
from routers import contestants, companies, guests, mentors, organizers, volunteers

app = FastAPI()

app.include_router(contestants.router)
app.include_router(companies.router)
app.include_router(guests.router)
app.include_router(mentors.router)
app.include_router(organizers.router)
app.include_router(volunteers.router)

@app.get("/")
def read_root():
    return {"message": "Identification Generator API"}
