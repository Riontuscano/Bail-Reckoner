from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float,Boolean
import csv
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import accuracy_score, classification_report
import joblib
import random



class Base(DeclarativeBase):
  pass

app=Flask(__name__)

db = SQLAlchemy(model_class=Base)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///caseFinal12.db"
db.init_app(app)

def append_to_csv(case_data, csv_filename='a.csv'):
    # Open the file in append mode
    with open(csv_filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        
        # Convert the object's attributes to a list
        row = [
            case_data.case_number,                # Mapped[int] case_number
            case_data.statute,                    # Mapped[str] statute
            case_data.offense_category,           # Mapped[str] offense_category
            case_data.penalty,                    # Mapped[str] penalty
            case_data.imprisonment_duration_served,  # Mapped[int] imprisonment_duration_served
            case_data.risk_of_escape,             # Mapped[str] risk_of_escape
            case_data.bail_eligibility,                  # Mapped[str] bail_bond
            case_data.surety_bond_required,       # Mapped[str] surety_bond_required
            case_data.served_half_term,           # Mapped[str] served_half_term
            case_data.risk_of_influence,          # Mapped[str] risk_of_influence
            case_data.personal_bond_required,     # Mapped[str] personal_bond_required
            case_data.fines_applicable,           # Mapped[str] fines_applicable
            case_data.risk_score,                 # Mapped[int] risk_score
            case_data.penalty_severity            # Mapped[int] penalty_severity
            ]

        
        # Append the row to the CSV file
        writer.writerow(row)

class Case_predictions(db.Model):
    case_id: Mapped[int] = mapped_column(Integer, primary_key=True)  # Aligning with case_id from CSV
    bail_eligibility: Mapped[bool] = mapped_column(String, nullable=False)  # Aligning with bail_eligibility from CSV
    risk_score: Mapped[int] = mapped_column(Integer, nullable=False)  # Aligning with risk_score from CSV
    penalty_severity: Mapped[int] = mapped_column(Integer, nullable=False)  # Aligning with penalty_severity from CSV


class Case_Data(db.Model):
    case_id: Mapped[int] = mapped_column(Integer, primary_key=True)  # Aligning with case_id from CSV
    case_number: Mapped[int] = mapped_column(Integer)  # Aligning with case_id from CSV
    statute: Mapped[str] = mapped_column(String(50), nullable=False)  # Aligning with statute from CSV
    offense_category: Mapped[str] = mapped_column(String(500), nullable=True)  # Aligning with offense_category from CSV
    penalty: Mapped[str] = mapped_column(String(200), nullable=True)  # Aligning with penalty from CSV
    imprisonment_duration_served: Mapped[int] = mapped_column(Integer, nullable=True)  # Aligning with imprisonment_duration_served from CSV
    risk_of_escape: Mapped[str] = mapped_column(String, nullable=False)  # Aligning with risk_of_escape from CSV
    risk_of_influence: Mapped[str] = mapped_column(String, nullable=False)  # Aligning with risk_of_escape from CSV
    surety_bond_required: Mapped[str] = mapped_column(String, nullable=False)  # Aligning with surety_bond_required from CSV
    personal_bond_required: Mapped[str] = mapped_column(String, nullable=False)  # Aligning with surety_bond_required from CSV
    fines_applicable: Mapped[str] = mapped_column(String, nullable=False)  # Aligning with surety_bond_required from CSV
    served_half_term: Mapped[str] = mapped_column(String, nullable=False)  # Aligning with served_half_term from CSV
    bail_eligibility: Mapped[str] = mapped_column(String, nullable=True)  # Aligning with case_id from CSV
    risk_score: Mapped[int] = mapped_column(Integer, nullable=True)  # Aligning with case_id from CSV
    penalty_severity: Mapped[int] = mapped_column(Integer, nullable=True)  # Aligning with case_id from CSV
    # fines_applicable: Mapped[bool] = mapped_column(String, nullable=False)  # Aligning with fines_applicable from CSV

    def to_dataframe(self):
        return pd.DataFrame([{
            "case_id": self.case_id,
            "case_number": self.case_number,
            "statute": self.statute,
            "offense_category": self.offense_category,
            "penalty": self.penalty,
            "imprisonment_duration_served": self.imprisonment_duration_served,
            "risk_of_escape": self.risk_of_escape,
            "risk_of_influence": self.risk_of_influence,
            "surety_bond_required": self.surety_bond_required,
            "personal_bond_required": self.personal_bond_required,
            "fines_applicable": self.fines_applicable,
            "served_half_term": self.served_half_term,
            "bail_eligibility": self.bail_eligibility,
            "risk_score": self.risk_score,
            "penalty_severity": self.penalty_severity
        }])
   
with app.app_context():
    db.create_all()


@app.route("/detail")
def ui(): 
    return render_template("case_detail.html")
# imprisonment_duration_served,risk_of_escape,risk_of_influence,surety_bond_required,personal_bond_required,fines_applicable,served_half_term,

@app.route("/getData",methods=["GET","POST"])
@app.route("/getData", methods=["GET", "POST"])
def get_data():
    print("hua run")
    if request.method == "POST":
        list = ['True', 'False']
        nums = [1, 2, 3]
        form_data = Case_Data(
            case_number=int(request.form.get('Case_number')),
            statute=request.form.get('acts'),
            offense_category=request.form.get('crime_types'),
            penalty=request.form.get('penalty_or_fine'),
            imprisonment_duration_served=int(request.form.get('imprisonment')),
            risk_of_escape=random.choice(list),
            risk_of_influence=random.choice(list),
            surety_bond_required='True',
            personal_bond_required='True',
            fines_applicable='True',
            served_half_term=random.choice(list),
            bail_eligibility=random.choice(list),
            risk_score=random.choice(nums),
            penalty_severity=random.randint(20, 400)
        )
        # Append form_data to CSV and database
        db.session.add(form_data)
        append_to_csv(form_data)
        getget()
        
        db.session.commit()

        # Pass the new instance to getget

        return "Data Submitted Successfully"

@app.route('/')
def index():
   return render_template('index.html')

file_path="a.csv"
data = pd.read_csv(file_path)


@app.route("/hogaya")
def getget():
    data_encoded = pd.get_dummies(data, columns=['statute', 'offense_category', 'penalty'], drop_first=True)

# Separate input features (X) and target labels (y) for the classification task
    X = data_encoded.drop(columns=['case_id', 'bail_eligibility', 'penalty_severity'])
    y_bail_eligibility = data_encoded['bail_eligibility']  # Target 1: Bail eligibility (yes/no)

    # Split the data into train-test sets for classification
    X_train, X_test, y_train, y_test = train_test_split(X, y_bail_eligibility, test_size=0.2, random_state=42)

    # Train a Random Forest Classifier for bail eligibility
    rf_classifier = RandomForestClassifier(random_state=42)
    rf_classifier.fit(X_train, y_train)

    # Make predictions on the test set for classification
    y_pred = rf_classifier.predict(X_test)

    # Evaluate the classifier
    accuracy = accuracy_score(y_test, y_pred)
    print(f'Accuracy of Bail Eligibility Prediction: {accuracy * 100:.2f}%')
    print(classification_report(y_test, y_pred))

    # Use penalty_severity as the target for the regression task
    y_penalty_severity = data_encoded['penalty_severity']

    # Split data for regression task
    X_train_reg, X_test_reg, y_train_reg, y_test_reg = train_test_split(
        X, y_penalty_severity, test_size=0.2, random_state=42
    )

    # Train a Random Forest Regressor for penalty severity prediction
    rf_regressor = RandomForestRegressor(random_state=42)
    rf_regressor.fit(X_train_reg, y_train_reg)

    # Save the trained models for future use (optional)
    joblib.dump(rf_classifier, 'rf_classifier_model.joblib')
    joblib.dump(rf_regressor, 'rf_regressor_model.joblib')

    # Function to calculate bail percentage based on risk score
    def calculate_bail_percentage(risk_score):
        max_risk_score = 357  # Maximum risk score in the dataset
        bail_percentage = (1 - (risk_score/max_risk_score)) * 100
        return max(min(bail_percentage, 100), 0)  # Ensure percentage is between 0 and 100

    # Create a new DataFrame to store predictions and bail percentage
    output_data = data_encoded[['case_id', 'bail_eligibility', 'penalty_severity']].copy()

    # Predict bail eligibility for all data
    output_data['predicted_bail_eligibility'] = rf_classifier.predict(X)

    # Predict penalty severity for all data
    output_data['predicted_penalty_severity'] = rf_regressor.predict(X)

    # Calculate bail percentage for each row
    output_data['predicted_bail_percentage'] = output_data['predicted_penalty_severity'].apply(calculate_bail_percentage)

    # Save the output data with predictions to a new CSV file
    output_file = 'predictions_output.csv'
    output_data.to_csv(output_file, index=False)

    print(f"Predictions and bail percentages saved to {output_file}")

    return "Done"




if __name__ == '__main__':
    app.run(debug=True)

