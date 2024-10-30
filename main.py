import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import json
import pprint

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

class GeoPos(BaseModel):
  latitude: float
  longitude: float
  

@app.get("/")
async def index():
    return FileResponse("static/index.html")
    
@app.post("/reverse_geocode")
async def reverse_geocode(geopos :GeoPos):
    from geopy.geocoders import Nominatim
    geolocator = Nominatim(user_agent="my_app")
    # breakpoint()
    location = geolocator.reverse((geopos.latitude, geopos.longitude), zoom=13)
    jsonData = location.raw if location else None
    pprint.pprint(jsonData, indent=2)
    return json.dumps(jsonData)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)