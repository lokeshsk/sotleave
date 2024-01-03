from nicegui import app, ui, events
from glob import glob


ui.label('School of Technology Timetable').classes('text-h3')
ui.label('Upload Timetable (only for Program Manager)').classes('text-h6')

def handle_upload(event: events.UploadEventArguments):
    with event.content as f:
        if "Teachers" in event.name:
            fname="Teachers.html"
        elif "Groups" in event.name:
            fname="Groups.html"
        file = open("timetable/"+fname, 'wb')
        for line in f.readlines():
            file.write(line)
        file.close()
        ui.notify("File uploaded successfully!")
ui.upload(on_upload=handle_upload).classes('max-w-full')

app.add_static_files('/timetable', 'Timetable')
ui.label('Timetable Links').classes('text-h6')
files = glob('timetable/*.html')
for i in files:
    if "Teachers" in i:
        ui.notify("hello")
        ui.link('View next week timetable faculty wise', i)
    elif "Groups" in i:
        ui.link('View next week timetable class wise', i)
    elif "Rooms" in i:
        ui.link('View next week timetable room wise', i)
    else:
        ui.label("No Timetable to show")
#ui.link('View next week timetable room wise', '/timetable/room.html')
ui.run()