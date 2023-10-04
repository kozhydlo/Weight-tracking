from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weight.db'
db = SQLAlchemy(app)

class WeightEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    weight = db.Column(db.Float, nullable=False)

@app.route('/')
def index():
    weight_entries = WeightEntry.query.all()
    return render_template('index.html', weight_entries=weight_entries)

@app.route('/add_weight', methods=['POST'])
def add_weight():
    try:
        weight = float(request.form.get('weight'))
        if weight <= 0:
            flash('Вага повинна бути більше 0', 'danger')
        else:
            new_entry = WeightEntry(weight=weight)
            db.session.add(new_entry)
            db.session.commit()
            flash('Вага успішно додана', 'success')
    except ValueError:
        flash('Некоректні дані введені', 'danger')
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    db.create_all()
    app.secret_key = 'your_secret_key'
    app.run(debug=True)
