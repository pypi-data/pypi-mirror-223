
from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.responses import FileResponse

from meeting_roles.meeting_manager import MeetingManager
from pathlib import Path
from fastapi.staticfiles import StaticFiles
from datetime import datetime
import configparser
import os 

current_directory = os.path.dirname(os.path.abspath(__file__))
config_file_path = os.path.join(current_directory, 'config.ini')
config = configparser.ConfigParser()
config.read(config_file_path)
db_path = config['database']['db_path']

app = FastAPI()
app.mount("/static", StaticFiles(directory="meeting_roles/static"), name="static")
meeting_manager = MeetingManager(db_path=db_path)
templates_dir = Path(__file__).parent / "templates"
html_template_path = templates_dir / "home.html"
error_template_path = templates_dir / "error.html"
help_template_path = templates_dir / "help.html"
update_person_form_template_path = templates_dir / "update_person_form.html"

def format_time_ago(original_datetime):
    # Convertir la cadena a un objeto datetime
    meeting_datetime_obj = datetime.fromisoformat(original_datetime)

    # Obtener la diferencia de tiempo entre ahora y la fecha y hora de la reunión
    time_difference = datetime.now() - meeting_datetime_obj

    # Calcular la diferencia en días y horas
    days_difference = time_difference.days
    hours_difference = time_difference.seconds // 3600

    # Formatear la fecha y hora en el formato deseado
    formatted_meeting_datetime = meeting_datetime_obj.strftime("%A, %d %B %Y @ %Hh")

    # Construir la cadena de salida
    if days_difference > 0:
        meeting_datetime = f"{days_difference} days ago ({formatted_meeting_datetime})"
    else:
        meeting_datetime = f"{hours_difference} hours ago ({formatted_meeting_datetime})"
    return meeting_datetime

def generate_home_page():
    acta_person, dynamizer_person,meeting_datetime, previous_acta_person_name,previous_dynamizer_person_name, previous_meeting_time = meeting_manager.get_current_meeting()
    people_list = meeting_manager.get_people()

    meeting_datetime = format_time_ago(meeting_datetime)  if meeting_datetime else "N/A"
    previous_datetime = format_time_ago(previous_meeting_time) if previous_meeting_time else "N/A"
    people_html = ""
    for person in people_list:
        actions = f'<a href="/update_person_form/{person[0]}">Update</a> | <a href="javascript:void(0);" onclick="confirmDelete({person[0]});">Delete</a> | <a href="/toggle_active/{person[0]}">{"Pause" if person[2] else "Unpause"}</a>'
        people_html += f'<tr><td>{person[0]}</td><td>{person[1]}</td><td>{"Active" if person[2] else "Inactive"}</td><td>{actions}</td></tr>'
    with open(html_template_path, 'r') as html_file:
        html_template = html_file.read()
    html_content = html_template.format(
        acta_person_name=acta_person[0] if acta_person else "N/A",
        dynamizer_person_name=dynamizer_person[0] if dynamizer_person else "N/A",
        meeting_datetime=meeting_datetime if meeting_datetime else "N/A",
        previous_acta_person_name=previous_acta_person_name,
        previous_dynamizer_person_name=previous_dynamizer_person_name,
        previous_meeting_time = previous_datetime,
        people_html=people_html)
    return HTMLResponse(content=html_content)

def generate_error_page(error_message):
    with open(error_template_path, 'r') as html_file:
        html_template = html_file.read()
    html_content = html_template.format(error_message=error_message)
    return HTMLResponse(content=html_content)

@app.get("/", response_class=HTMLResponse)
def home():
    return generate_home_page()

@app.post("/add_person", response_class=HTMLResponse)
def add_person(name: str = Form(...), active: str = Form("on")):
    try:
        meeting_manager.add_person(name, active == "on")
        return generate_home_page()
    except Exception as e:
        error_message = str(e)
        return generate_error_page(error_message)

@app.get("/update_person_form/{person_id}", response_class=HTMLResponse)
def update_person_form(person_id: int):
    try:
        person = meeting_manager.get_person(person_id)
        if not person:
            raise HTTPException(status_code=404, detail="Person not found")
        with open(update_person_form_template_path, 'r') as html_file:
            html_template = html_file.read()
        html_content = html_template.format(person_id=person_id, person_name=person[0], active_checked="checked" if person[1] else "")
        return HTMLResponse(content=html_content)
    except Exception as e:
        error_message = str(e)
        return generate_error_page(error_message)

@app.post("/update_person/{person_id}", response_class=HTMLResponse)
def update_person(person_id: int, name: str = Form(...), active: str = Form("off")):
    try:
        meeting_manager.update_person(person_id, name, active == "on")
        return generate_home_page()
    except Exception as e:
        error_message = str(e)
        return generate_error_page(error_message)

@app.get("/delete_person/{person_id}", response_class=HTMLResponse)
def delete_person(person_id: int):
    try:
        meeting_manager.delete_person(person_id)
        return generate_home_page()
    except Exception as e:
        error_message = str(e)
        return generate_error_page(error_message)

@app.get("/toggle_active/{person_id}", response_class=HTMLResponse)
def toggle_active(person_id: int):
    try:
        meeting_manager.toggle_active(person_id)
        return generate_home_page()
    except Exception as e:
        error_message = str(e)
        return generate_error_page(error_message)

@app.post("/next_meeting", response_class=HTMLResponse)
def next_meeting():
    try:
        meeting_manager.next_meeting()
        return generate_home_page()
    except Exception as e:
        error_message = str(e)
        return generate_error_page(error_message)

@app.get("/delete_most_recent_meeting", response_class=HTMLResponse)
def delete_most_recent_meeting():
    try:
        meeting_manager.delete_most_recent_meeting()
        return generate_home_page()
    except Exception as e:
        error_message = str(e)
        return generate_error_page(error_message)

@app.get("/help", response_class=HTMLResponse)
def help_page():
    return FileResponse(help_template_path)
