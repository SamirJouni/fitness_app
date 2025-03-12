from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

# Funktion zum Laden der Übungen aus der JSON-Datei
def load_exercises():
    with open('exercises.json', 'r', encoding='utf-8') as f:
        return json.load(f)

# Funktion zum Speichern der Übungen in die JSON-Datei
def save_exercises(exercises):
    with open('exercises.json', 'w', encoding='utf-8') as f:
        json.dump(exercises, f, ensure_ascii=False, indent=4)

@app.route('/')
def index():
    return render_template('index.html')

# Neue Route für die Datenbankbearbeitung
@app.route('/edit_database', methods=['GET', 'POST'])
def edit_database():
    exercises = load_exercises()
    if request.method == 'POST':
        # Hier können Sie die Logik zum Speichern der Änderungen hinzufügen
        # Zum Beispiel: neue Datensätze hinzufügen oder bestehende aktualisieren
        pass
    return render_template('edit_database.html', exercises=exercises)

@app.route('/edit_exercise/<int:exercise_id>', methods=['GET', 'POST'])
def edit_exercise(exercise_id):
    exercises = load_exercises()
    exercise = next((ex for ex in exercises if ex['id'] == exercise_id), None)

    if request.method == 'POST':
        exercise['title'] = request.form['title']
        exercise['description'] = request.form['description']
        exercise['repetitions'] = int(request.form['repetitions'])
        exercise['sets'] = int(request.form['sets'])

        # Überprüfen, ob ein neues Bild hochgeladen wurde
        if 'image' in request.files:
            image = request.files['image']
            if image:
                exercise['image'] = image.filename  # Aktualisiere den Dateinamen
                image.save(f'static/images/{image.filename}')  # Speichern Sie das neue Bild

        # Speichern Sie die aktualisierten Übungen
        save_exercises(exercises)

        return redirect(url_for('edit_database'))  # Nach dem Speichern zurück zur Datenbankbearbeitung

    return render_template('edit_exercise.html', exercise=exercise)

@app.route('/add_exercise', methods=['GET', 'POST'])
def add_exercise():
    if request.method == 'POST':
        new_exercise = {
            'id': len(load_exercises()) + 1,  # Neue ID basierend auf der Anzahl der bestehenden Übungen
            'title': request.form['title'],
            'description': request.form['description'],
            'image': request.files['image'].filename,  # Hier wird der Dateiname gespeichert
            'repetitions': int(request.form['repetitions']),
            'sets': int(request.form['sets']),
            'level': 'einfach'  # Standardwert oder basierend auf einer Auswahl setzen
        }
        
        # Speichern Sie das Bild im entsprechenden Verzeichnis (optional)
        image = request.files['image']
        if image:
            image.save(f'static/images/{image.filename}')  # Speichern Sie das Bild im static/images-Verzeichnis
        
        # Übungen laden, neue Übung hinzufügen und speichern
        exercises = load_exercises()
        exercises.append(new_exercise)
        save_exercises(exercises)

        return redirect(url_for('edit_database'))  # Nach dem Speichern zurück zur Datenbankbearbeitung

    return render_template('add_exercise.html')

@app.route('/level/<level>')
def level(level):
    exercises = load_exercises()
    filtered_exercises = [ex for ex in exercises if ex['level'] == level]
    return render_template('level.html', exercises=filtered_exercises, level=level)

@app.route('/start_training', methods=['POST'])
def start_training():
    selected_exercises = request.form.getlist('selected_exercises')
    exercises_data = load_exercises()
    
    # Hier kannst du die Logik zur Verarbeitung der ausgewählten Übungen hinzufügen
    
    return render_template('countdown.html', exercises=exercises_data)

@app.route('/countdown', methods=['GET'])
def countdown():
    exercises = load_exercises()  # Laden Sie die Übungen aus der JSON-Datei
    # Hier können Sie die Übungen nach Level filtern, wenn nötig
    for exercise in exercises:
        exercise['image_url'] = url_for('static', filename='images/' + exercise['image'])  # Bild-URL hinzufügen
    return render_template('countdown.html', exercises=exercises)

@app.after_request
def after_request(response):
    response.headers.add('Content-Type', 'text/html; charset=utf-8')
    return response

if __name__ == '__main__':
    app.run(debug=True)