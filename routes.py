from flask import render_template, request, redirect
from blog import app
from blog.forms import EntryForm
from blog.models import Entry, db

@app.route('/')
def homepage():
    posts = Entry.query.filter_by(is_published=True).order_by(Entry.pub_date.desc())
    return render_template('index.html', posts=posts)

@app.route('/addpost', methods=["GET","POST"])
def create_entry():
    form = EntryForm()
    errors = None
    if request.method == 'POST':
        if form.validate_on_submit():
            entry = Entry(
                title=form.title.data,
                body=form.body.data,
                is_published=form.is_published.data
            )
            db.session.add(entry)
            db.session.commit()
        else:
            errors=form.errors
    return render_template('entry_form.html', form=form, errors=errors)

@app.route('/editpost/<int:entry_id>', methods=["GET", "POST"])
def edit_entry(entry_id):
    entry = Entry.query.filter_by(id=entry_id).first_or_404()
    form = EntryForm(obj=entry)
    errors = None
    if request.method == 'POST':
        if form.validate_on_submit():
            form.populate_obj(entry)
            db.session.commit()
            return redirect('index.html')
        else:
            errors = form.errors
    return render_template("entry_form.html", form=form, errors=errors)