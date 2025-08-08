# Gemini-Powered Resume & Cover Letter Customizer

An intelligent, full-stack web application designed to help job seekers tailor their resumes and cover letters for specific job applications. This tool leverages the power of the Google Gemini API to perform deep analysis, structural parsing, and content generation, guiding users to create perfectly optimized, ATS-friendly documents.



## ✨ Features

This application is packed with features to provide a complete, end-to-end resume customization experience:

* **🤖 AI-Powered Analysis:**
    * Upload a base resume (`.pdf` or `.docx`) and paste a job description.
    * Receives an ATS-style **match score**.
    * Identifies **missing keywords** from the job description.
    * Generates **rewritten bullet points** for the resume, tailored for impact.
    * Provides key **themes** to focus on for a cover letter.

* **📄 Structural Resume Parsing:** The AI intelligently parses the entire resume into a structured format, identifying sections like contact info, summary, work experience, and education.

* **🎨 Multi-Template Designer:**
    * Choose from **8 professional templates**, including creative designs and several highly ATS-optimized layouts.
    * A template chooser page provides descriptions and color palettes for each design.

* **✍️ Live WYSIWYG Editor:**
    * The selected resume design is rendered in a live, in-browser editor powered by TinyMCE.
    * Users can make final edits and tweaks to their designed resume in real-time.

* **🚀 Multiple Export Options:**
    * **Save as PDF:** A high-fidelity, pixel-perfect "Print to PDF" feature using the browser's built-in rendering engine.

* **✉️ AI Cover Letter Generator:**
    * With one click, generate a complete, professional cover letter based on the user's resume and the target job description.

* **👤 User Accounts & Persistence:**
    * Secure user registration and login functionality.
    * All analyzed resumes and their corresponding analyses are automatically saved to the user's account.

* **🖥️ User Dashboard:**
    * A personal dashboard where users can view a list of all their saved resumes and the analyses performed on them.

* **⚡ Modern User Experience:**
    * The main analysis workflow is built as a Single-Page Application (SPA), providing a fast, responsive experience without full-page reloads.

* **🧪 Comprehensive Test Suite:**
    * The backend logic is supported by a suite of automated tests written with `pytest` and `pytest-mock`, ensuring reliability and maintainability.


## 🛠️ Tech Stack

* **Backend:** Python 3, Flask
* **Database:** SQLite with Flask-SQLAlchemy & Flask-Migrate
* **Authentication:** Flask-Login
* **Forms:** Flask-WTF
* **AI:** Google Gemini API (`gemini-1.5-flash`)
* **Document Parsing:** `python-docx`, `pdfplumber`
* **Frontend:** HTML5, CSS3, JavaScript
* **CSS Framework:** Pico.css (classless)
* **Live Editor:** TinyMCE
* **Testing:** `pytest`, `pytest-mock`


## ⚙️ Local Setup and Installation

To run this project on your local machine, please follow these steps:

**1. Prerequisites:**
* Python 3.9+
* Git

**2. Clone the Repository:**
```bash
git clone https://github.com/AlexBiobelemo/Project-Theresa
cd resume-customizer
```

**3. Create and Activate a Virtual Environment:**
* **Windows:**
    ```bash
    python -m venv venv
    venv\Scripts\activate
    ```
* **macOS / Linux:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

**4. Install Dependencies:**
```bash
pip install -r requirements.txt
```

**5. Configure Environment Variables:**
* Create a file named `.env` in the root directory of the project.
* Add your secret keys to this file. This file is included in `.gitignore` and should never be committed to version control.
    ```
    # .env file
    SECRET_KEY="<your-generated-secret-key>"
    GEMINI_API_KEY="<your-google-gemini-api-key>"
    ```
* You will also need a TinyMCE API key for the live editor. Get one from [tiny.cloud](https://www.tiny.cloud) and paste it into the placeholder in the `app/templates/designs/designer_layout.html` file.

**6. Initialize the Database:**
* First, set the `FLASK_APP` environment variable:
    * **Windows (PowerShell):** `$env:FLASK_APP="run.py"`
    * **Windows (cmd.exe):** `set FLASK_APP=run.py`
    * **macOS / Linux:** `export FLASK_APP=run.py`

* Then, run the database migration commands:
    ```bash
    flask db init      # Run only the very first time
    flask db migrate -m "Initial migration"
    flask db upgrade
    ```

**7. Run the Application:**
```bash
python run.py
```
The application will be available at `http://127.0.0.1:5000`.


## 🚀 Usage

1.  Navigate to the application and **Register** for a new account, then **Login**.
2.  On the homepage, **upload your resume** and **paste a job description**.
3.  Click **"Analyze Now"**. The results will appear on the same page.
4.  To create a designed version, click **"Design This Resume"**.
5.  On the **Chooser Page**, select a template that fits your style.
6.  You will be taken to the **Designer Page**, where you can make live edits to the text.
7.  Use your browser's print function to get a perfect **PDF**.


## 🧪 Running the Tests

A comprehensive test suite is included. To run the tests, navigate to the project's root directory and run:
```bash
pytest
```
