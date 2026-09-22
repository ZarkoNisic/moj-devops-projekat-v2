import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Konfiguracija baze podataka preko environment varijabli (koje ćemo definisati u Docker Compose-u)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://moj_korisnik:moja_lozinka@db:5432/moja_baza')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Model za testbazu
class Visit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    count = db.Column(db.Integer, nullable=False)

@app.route('/')
def home():
    # Kreiramo tabelu ako ne postoji i dodajemo posjetu
    try:
        with app.app_context():
            db.create_all()
            visit = Visit.query.first()
            if not visit:
                visit = Visit(count=1)
                db.session.add(visit)
            else:
                visit.count += 1
            db.session.commit()
            count_val = visit.count
    except Exception as e:
        count_val = f"Greška sa bazom: {e}"

    return render_template('index.html', count=count_val)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)