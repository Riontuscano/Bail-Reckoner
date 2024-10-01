from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float,Boolean


class Base(DeclarativeBase):
  pass

app=Flask(__name__)

db = SQLAlchemy(model_class=Base)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///case_data12345.db"
db.init_app(app)

class Case_Data(db.Model):
    case_id: Mapped[int] = mapped_column(Integer, primary_key=True)  # Aligning with case_id from CSV
    statute: Mapped[str] = mapped_column(String(50), nullable=False)  # Aligning with statute from CSV
    offense_category: Mapped[str] = mapped_column(String(500), nullable=True)  # Aligning with offense_category from CSV
    penalty: Mapped[str] = mapped_column(String(200), nullable=True)  # Aligning with penalty from CSV
    imprisonment_duration_served: Mapped[int] = mapped_column(Integer, nullable=True)  # Aligning with imprisonment_duration_served from CSV
    risk_of_escape: Mapped[bool] = mapped_column(String, nullable=False)  # Aligning with risk_of_escape from CSV
    surety_bond_required: Mapped[bool] = mapped_column(String, nullable=False)  # Aligning with surety_bond_required from CSV
    # fines_applicable: Mapped[bool] = mapped_column(String, nullable=False)  # Aligning with fines_applicable from CSV
    served_half_term: Mapped[bool] = mapped_column(String, nullable=False)  # Aligning with served_half_term from CSV
    bail_eligibility: Mapped[bool] = mapped_column(String, nullable=False)  # Aligning with bail_eligibility from CSV
    risk_score: Mapped[int] = mapped_column(Integer, nullable=False)  # Aligning with risk_score from CSV
    penalty_severity: Mapped[int] = mapped_column(Integer, nullable=False)  # Aligning with penalty_severity from CSV

with app.app_context():
    db.create_all()


@app.route("/detail")
def ui():
    return render_template("case_detail.html")

@app.route("/getData",methods=["GET","POST"])
def get_data():
    if request.method == "POST":
        form_data = Case_Data(
            Case_number=int(request.form.get('Case_number')),
            name_undertrial=request.form.get('num_undertrial'),
            crime_type=request.form.get('crime_type'),
            imprisonment=request.form.get('imprisonment'),
            bail_bond=int(request.form.get('bail_bond')) if request.form.get('bail_bond') else None,
            surety=request.form.get('surety'),
            ever_escaped=request.form.get('ever_escaped'),
            risk_of_case=int(request.form.get('risk_of_case')),
            served_half_term=request.form.get('served_half_term'),
            penalty_or_fine=request.form.get('penalty_or_fine')
        )
        db.session.add(form_data)
        db.session.commit()
        return "Data Submitted Successfully"

@app.route('/')
def index():
   return render_template('index.html')




if __name__ == '__main__':
    app.run(debug=True)
