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
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    Case_number: Mapped[int] = mapped_column(Integer, nullable=False)
    name_undertrial: Mapped[str] = mapped_column(String, nullable=False)
    crime_type: Mapped[str] = mapped_column(String(500), nullable=True)
    imprisonment: Mapped[str] = mapped_column(String(200), nullable=True)
    bail_bond: Mapped[int] = mapped_column(Integer, nullable=True)
    surety: Mapped[str] = mapped_column(String(250), nullable=True)
    ever_escaped: Mapped[str] = mapped_column(String, nullable=False)
    risk_of_case: Mapped[int] = mapped_column(Integer, nullable=False)
    served_half_term: Mapped[str] = mapped_column(String, nullable=False)
    penalty_or_fine: Mapped[str] = mapped_column(String(250), nullable=False)

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
