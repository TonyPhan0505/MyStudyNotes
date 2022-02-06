from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

views = Blueprint("views",__name__)

@views.route("/", methods = ["GET","POST"])
@login_required  # Don't let the user go to the home page unless they are logged in
def home():
	if request.method == "POST":
		note = request.form.get("note")
		subject = request.form.get("subject")
		if len(note) < 1:
			flash("Please add note!", category = "error")
		if len(subject) < 1:
			flash("Please add subject!", category = "error")
		else:
			# add new note
			new_note = Note(data=note, subject = subject, user_id=current_user.id)
			db.session.add(new_note)
			db.session.commit()
			flash("Note is added!", category = "success")
	return render_template("home.html", user = current_user)

@views.route("/notes", methods = ["GET"])
@login_required
def notes():
	return render_template("notes.html", user=current_user)

@views.route("/notes", methods = ["GET","POST"])
def filtered_notes():
	if request.method == "POST":
		criteria = request.form.get("criteria")
		user_id = current_user.id
		if len(criteria) < 1:
			flash("Please enter criteria!", category = "error")
		else:
			notes = Note.query.filter(Note.data.contains(criteria))
			flash("Successfully fitered!", category = "success")
			return render_template("filtered_notes.html", notes = notes, user = current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    return jsonify({})