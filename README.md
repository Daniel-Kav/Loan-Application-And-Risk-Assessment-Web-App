# Loan Application & Risk Assessment Web App

A modern, full-featured Flask web application for loan management, risk assessment, and peer-to-peer business advice. The app leverages AI for loan advice, supports user registration and authentication, and provides a clean, extensible architecture.

---

## Features

- **User Registration & Login**: Secure authentication with hashed passwords.
- **Profile Management**: Users can create and manage detailed business profiles.
- **Loan Risk Assessment**: AI-powered (Google Gemini) loan advice, delivered as a downloadable PDF.
- **Peer-to-Peer Advice**: Users can post and view business advice messages.
- **Loan Application Workflow**: Submit, finalize, and monitor loan applications.
- **Market Analysis**: Placeholder for real-time market analysis.
- **Modern UI**: Responsive design with custom and framework-based CSS.

---

## Project Structure

```
.
├── run.py                  # Application entry point
├── instance/
│   └── site.db             # SQLite database (auto-generated)
├── loan/
│   ├── __init__.py         # App factory and configuration
│   ├── forms.py            # WTForms form classes
│   ├── models.py           # SQLAlchemy models
│   ├── routes.py           # Flask routes (views)
│   ├── static/             # CSS, JS, images, videos
│   └── templates/          # HTML templates
```

---

## Setup & Installation

### 1. **Clone the Repository**

```bash
git clone <your-repo-url>
cd <project-directory>
```

### 2. **Install Dependencies**

Create a virtual environment (recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

Install required packages:

```bash
pip install flask flask_sqlalchemy flask_bcrypt flask_wtf flask_login fpdf google-generativeai
```

Or, if you have a `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 3. **Set Up Environment Variables**

The app uses a Google API key for AI features.  
**For development, the key is hardcoded, but for production:**

```powershell
$env:GOOGLE_API_KEY="your-google-api-key"  # Windows PowerShell
# or
export GOOGLE_API_KEY="your-google-api-key"  # Linux/Mac
```

### 4. **Run the Application**

```bash
python run.py
```

Visit [http://127.0.0.1:5000/](http://127.0.0.1:5000/) in your browser.

---

## Usage

1. **Register** a new account.
2. **Login** and create your business profile.
3. Use the **Loan Risk Assessment** tool for AI-powered advice (PDF download).
4. **Post/view advice** in the Peer-to-Peer section.
5. **Finalize and submit** your loan application.
6. **Monitor** your application and access other features.

---

## Main Technologies

- **Flask**: Web framework
- **Flask-WTF**: Form handling & CSRF protection
- **Flask-Login**: User session management
- **Flask-Bcrypt**: Password hashing
- **Flask-SQLAlchemy**: ORM for database
- **FPDF**: PDF generation
- **Google Generative AI (Gemini)**: AI-powered loan advice
- **SQLite**: Database (auto-generated)

---

## Customization

- **UI/UX**: All templates are in `loan/templates/`. CSS is in `loan/static/`.
- **Profile Pictures**: Store in `loan/static/profilr_pics/`.
- **Branding**: Update `base.html` and CSS files for your brand.

---

## Security Notes

- Change the `SECRET_KEY` in `loan/__init__.py` for production.
- Do not hardcode sensitive keys; use environment variables.
- Use HTTPS in production.

---

## Contributing

1. Fork the repo
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request

---

## License

[MIT](LICENSE) (or specify your license)

---

## Acknowledgements

- [Flask](https://flask.palletsprojects.com/)
- [Bootstrap](https://getbootstrap.com/) or your chosen CSS framework
- [Google Generative AI](https://ai.google.dev/)

---

**For any questions or issues, please open an issue on the repository.** 