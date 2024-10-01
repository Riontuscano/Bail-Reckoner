from flask import Flask, render_template, request, send_file
from fpdf import FPDF
import os

app = Flask(__name__)

# Home route to display the form
@app.route('/')
def form():
    return render_template('form.html')

# Function to generate a well-formatted bail application PDF
def generate_pdf(court_name, accused_name, police_station, fir_no, section, custody_date, applicant_name, father_name):
    pdf = FPDF()
    pdf.add_page()
    
    # Title and subtitle formatting
    pdf.set_font("Arial", style='B', size=16)
    pdf.cell(200, 10, txt="BAIL APPLICATION", ln=True, align='C')
    
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"IN THE COURT OF {court_name.upper()}", ln=True, align='C')
    
    pdf.ln(10)  # Add some space
    
    # Add the header for the case
    pdf.set_font("Arial", style='B', size=12)
    pdf.cell(200, 10, txt="IN THE MATTER OF", ln=True, align='L')
    
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"STATE VS {accused_name.upper()}", ln=True, align='L')
    pdf.cell(200, 10, txt=f"Police Station: {police_station}", ln=True, align='L')
    pdf.cell(200, 10, txt=f"FIR No.: {fir_no}    U/S: {section}", ln=True, align='L')
    pdf.cell(200, 10, txt=f"Accused under police custody since: {custody_date}", ln=True, align='L')
    
    pdf.ln(10)  # Add some space
    
    # Application content
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt=f"""
APPLICATION UNDER SECTION 439 Cr. PC FOR GRANT OF BAIL 
ON BEHALF OF THE ACCUSED, {applicant_name.upper()}, S/O {father_name.upper()}.

MOST RESPECTFULLY SUBMITTED AS UNDER:

1. That the police has falsely implicated the applicant in the present case and have arrested him without any reason on {custody_date}, and the applicant is in police custody since then.

2. That the applicant is an innocent man and has not committed any crime as being alleged against him.

3. That the applicant is not required in any kind of investigation, nor is his custodial interrogation necessary.

4. That the applicant has very good antecedents, and there is no criminal case pending against him.

5. That the applicant is a permanent resident, and there are no chances of him absconding.

6. That the applicant undertakes to present himself before the court as and when directed.

7. That the applicant undertakes to cooperate with the police during the course of investigation.

8. That no useful purpose will be served by keeping the applicant in custody as no recovery is to be made, nor is any interrogation required.

9. That the applicant undertakes not to tamper with the evidence or the witnesses in any manner.

10. That the applicant undertakes to comply with all the conditions imposed by the court.
    
It is therefore prayed that the court may release the applicant on bail on such terms and conditions as the court may deem fit and proper in the facts and circumstances of the case.

Any other order which the court may deem fit and proper in favor of the applicant is also prayed for.
    """)
    
    pdf.ln(10)  # Add some space
    
    # Signature
    pdf.cell(200, 10, txt="APPLICANT", ln=True, align='L')
    pdf.cell(200, 10, txt="THROUGH COUNSEL", ln=True, align='L')
    
    # Save the PDF to a file
    pdf_file = f"bail_application_{accused_name}.pdf"
    pdf.output(pdf_file)
    return pdf_file

# Route to handle form submission and generate PDF
@app.route('/generate', methods=['POST'])
def generate_bail_application():
    # Get form data
    court_name = request.form['court_name']
    accused_name = request.form['accused_name']
    police_station = request.form['police_station']
    fir_no = request.form['fir_no']
    section = request.form['section']
    custody_date = request.form['custody_date']
    applicant_name = request.form['applicant_name']
    father_name = request.form['father_name']
    
    # Generate the PDF with better formatting
    pdf_file = generate_pdf(court_name, accused_name, police_station, fir_no, section, custody_date, applicant_name, father_name)
    
    # Provide the PDF for download
    return send_file(pdf_file, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
