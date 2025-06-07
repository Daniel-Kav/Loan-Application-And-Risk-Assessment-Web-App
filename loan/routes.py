from flask import render_template,url_for,redirect,request,flash,make_response
from loan.forms import *
from loan.models import *
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from loan import app,bcrypt,db
import re
import google.generativeai as genai
import os
from fpdf import FPDF
from io import BytesIO
from loan import app

os.environ['GOOGLE_API_KEY']="AIzaSyCy_J0XsyWwPtKCzPKhKSb0o1SKUrNSjdg"
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category='info'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/register',methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('user_account'))
    form=RegistrationForm()
    if form.validate_on_submit():
        enc_password=bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user=User(username=form.username.data,
                  email=form.email.data,
                  password=enc_password
                  )
        db.session.add(user)
        db.session.commit()
        flash('acount created succesfully!',category='success')
        return redirect(url_for('login'))
    return render_template('register.html',form=form)

@app.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('user_account'))
    form=LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user)
            flash('Logged in successfully!', 'success')
            next_page=request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('user_account'))
        flash('Invalid credentials', 'danger')
    return render_template('login.html',form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('login'))

def generate_pdf(content: str)->BytesIO:
    #generating the pdf
    pdf=FPDF()
    pdf.add_page()
    pdf.set_font('Arial',size=14)
    pdf.multi_cell(0,5,content)

    #saving the pdf to a BYtesIO object
    pdf_output=BytesIO()
    pdf_output.write(pdf.output(dest='S').encode('latin1'))
    pdf_output.seek(0)
    return pdf_output


@app.route('/user_account')
@login_required
def user_account():
    return render_template('account_info.html')


@app.route('/account')
@login_required
def account():
    return render_template("account.html")  # User account page with links to all pages

# Profile Page
@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    form = UserProfileForm()
    if form.validate_on_submit():
        # Check if the user already has a profile to avoid duplicate entries
        if current_user.profile:
            flash("Profile already exists!", "warning")
            return redirect(url_for("user_account"))
        
        # Create the profile and associate it with the logged-in user
        profile = UserProfile(
            full_names=form.full_names.data,
            monthly_income=form.monthly_income.data,
            business_type=form.business_type.data,
            business_level=form.business_level.data,
            phone_no=form.phone.data,
            country=form.country.data,
            location=form.location.data,
            user_id=current_user.id  # Link to the logged-in user
        )
        db.session.add(profile)
        db.session.commit()
        flash("Profile created successfully!", "success")
        return redirect(url_for("user_account"))
    return render_template("profile.html", form=form)


# Loan Risk Assessment Page
@app.route("/loan-risk-assessment", methods=["GET", "POST"])
@login_required
def loan_risk_assessment():
    form=LoanRiskAssessmentForm()
    if form.validate_on_submit():
        genai.configure(api_key = os.environ['GOOGLE_API_KEY'])
        generation_config = {
            "temperature": 0.3,
            "top_p": 0.95,
            "top_k": 64,
            "max_output_tokens": 8192,
            "response_mime_type": "text/plain",
            }

        model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
        ) 
        raw_response = model.generate_content(f"""advice me on what amount of 
                                              loan to apply in kenya having a monthly 
                                              income of kenya shillings {form.monthly_income.data},
                                              and {form.business_type.data} bussines at a 
                                              {form.business_level.data} level and a repayment period 
                                              of {form.repayment_period.data} months 
                                              based on the given information 
                                              recommend on how to invest on this loan,if the description of my bussiness
                                              is :{form.business_desc.data}""")
        formatted_response=re.sub(r'\*+','\n',raw_response.text)
        pdf_output=generate_pdf(formatted_response)
        response=make_response(pdf_output.read())
        response.headers['Content-Type']='application/pdf'
        response.headers['Content-Disposition']='inline;filename="loan_advice.pdf"'
        return response
    return render_template("loan-risk-assessment.html",form=form)



# Real-Time Market Analysis Page
@app.route("/real-time-market-analysis", methods=["GET"])
@login_required
def real_time_market_analysis():
    return render_template("real-time-market-analysis.html")

# Peer-to-Peer Advice Page
@app.route("/peer-to-peer-advice", methods=["GET", "POST"])
@login_required
def peer_to_peer_advice():
    form = PeerToPeerAdviceForm()
    if form.validate_on_submit():
        new_message = PeerToPeerAdvice(
            message=form.message.data
        )

        # Save the message to the database
        db.session.add(new_message)
        db.session.commit()

        flash("Your message has been posted!", "success")
        return redirect(url_for("peer_to_peer_advice"))

    # Retrieve all messages from the database to display on the page
    all_messages = PeerToPeerAdvice.query.order_by(PeerToPeerAdvice.id.desc()).all()

    return render_template("peer-advice.html", messages=all_messages)


# Finalize and Submit Loan Application Page
@app.route("/finalize-loan-application", methods=["GET", "POST"])
@login_required
def finalize_loan_application():
    form=FinalizeLoanApplicationForm()
    if form.validate_on_submit():
        return redirect(url_for("confirmation"))
    return render_template("finalize-loan-application.html")

# Confirmation Page
@app.route("/confirmation")
@login_required
def confirmation():
    return "<h1>Thank you! Your loan application has been submitted successfully.</h1>"

# Post-Loan Monitoring Page
@app.route("/post-loan-monitoring", methods=["GET"])
@login_required
def post_loan_monitoring():
    return render_template("post-loan-monitoring.html")

