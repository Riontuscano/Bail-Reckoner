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






class Base(DeclarativeBase):
  pass

app=Flask(__name__)

db = SQLAlchemy(model_class=Base)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///caseFinal.db"
db.init_app(app)

def append_to_csv(case_data, csv_filename='a.csv'):
    # Open the file in append mode
    with open(csv_filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        
        # Convert the object's attributes to a list
        row = [
            
            case_data.case_number,
            case_data.statute,
            case_data.offense_category,
            case_data.penalty,
            int(case_data.imprisonment_duration_served),
            case_data.risk_of_escape,
            case_data.bail_bond,
            case_data.surety_bond_required,
            case_data.served_half_term,
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
    risk_of_escape: Mapped[bool] = mapped_column(String, nullable=False)  # Aligning with risk_of_escape from CSV
    bail_bond: Mapped[int] = mapped_column(Integer, primary_key=False)  # Aligning with case_id from CSV
    surety_bond_required: Mapped[bool] = mapped_column(String, nullable=False)  # Aligning with surety_bond_required from CSV
    # fines_applicable: Mapped[bool] = mapped_column(String, nullable=False)  # Aligning with fines_applicable from CSV
    served_half_term: Mapped[bool] = mapped_column(String, nullable=False)  # Aligning with served_half_term from CSV
   
with app.app_context():
    db.create_all()


@app.route("/detail")
def ui():
    
    return render_template("case_detail.html")

@app.route("/getData",methods=["GET","POST"])
def get_data():
    getget()
    print("hua run")
    if request.method == "POST":
        form_data = Case_Data(
        case_number=int(request.form.get('Case_number')),
        statute=request.form.get('acts'),
        offense_category=request.form.get('crime_types'),
        penalty=request.form.get('penalty_or_fine'),
        imprisonment_duration_served=int(request.form.get('imprisonment')),  # Imprisonment duration field
        risk_of_escape=request.form.get('ever_escaped') == 'True',  # Risk of escape boolean
        bail_bond=int(request.form.get('bail_bond')) if request.form.get('bail_bond') else None,
        surety_bond_required=request.form.get('suretybond') == 'True',  # Surety bond boolean
        served_half_term=request.form.get('served_half_term') == 'True',  # Served half term boolean
        )
        db.session.add(form_data)
        db.session.commit()
        append_to_csv(form_data)

        return "Data Submitted Successfully"


@app.route('/')
def index():
   return render_template('index.html')


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
    # getget()
    return "Generated"


if __name__ == '__main__':
    app.run(debug=True)
    getget()

