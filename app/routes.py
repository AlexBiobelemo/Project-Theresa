from flask import Blueprint, render_template, request, flash, redirect, url_for, session, Response, jsonify, abort
from .utils import get_text_from_file, allowed_file
from .nlp_processor import get_ai_analysis, generate_full_cover_letter, get_structured_resume, get_combined_ai_data
from .forms import RegistrationForm, LoginForm
from .models import User, Resume, Analysis
from app import db
import io, json
from html2docx import Html2Docx
from flask_login import current_user, login_user, logout_user, login_required

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/api/analyze', methods=['POST'])
def api_analyze():
    if 'resume' not in request.files or 'job_description' not in request.form:
        return jsonify({'error': 'Missing form data.'}), 400

    resume_file = request.files['resume']
    jd_text = request.form.get('job_description', '').strip()

    if resume_file.filename == '' or not jd_text:
        return jsonify({'error': 'Resume file and job description are required.'}), 400

    if not allowed_file(resume_file.filename):
        return jsonify({'error': 'Invalid file type. Please upload a .pdf or .docx file.'}), 400

    try:
        resume_text = get_text_from_file(resume_file)
        if not resume_text:
            return jsonify({'error': 'Could not parse the resume file.'}), 400

        # --- ONE EFFICIENT AI CALL ---
        full_data = get_combined_ai_data(resume_text, jd_text)

        if 'error' in full_data:
            return jsonify({'error': 'An error occurred during AI processing.'}), 500

        # Extract the two parts from the response
        analysis_results = full_data.get('analysis_results', {})
        structured_data = full_data.get('structured_resume', {})

        if current_user.is_authenticated:
            new_resume = Resume(
                original_filename=resume_file.filename,
                structured_data_json=json.dumps(structured_data),
                author=current_user
            )
            db.session.add(new_resume)
            new_analysis = Analysis(
                job_description=jd_text,
                analysis_data_json=json.dumps(analysis_results),
                resume=new_resume
            )
            db.session.add(new_analysis)
            db.session.commit()

        # We now return the nested structure
        session['structured_resume'] = structured_data
        session['original_resume_text'] = resume_text
        session['original_jd_text'] = jd_text

        return jsonify(full_data)

    except Exception as e:
        print(f"An unexpected error in /api/analyze: {e}")
        return jsonify({'error': f'An unexpected server error occurred: {e}'}), 500


@main.route('/generate-cover-letter', methods=['POST'])
def generate_cover_letter():
    resume_text = session.get('original_resume_text')
    jd_text = session.get('original_jd_text')
    if not resume_text or not jd_text:
        flash("Your session may have expired. Please analyze a resume again.")
        return redirect(url_for('main.index'))
    cover_letter_text = generate_full_cover_letter(resume_text, jd_text)
    if isinstance(cover_letter_text, dict) and 'error' in cover_letter_text:
        flash(f"An AI error occurred: {cover_letter_text['error']}")
        return redirect(url_for('main.index'))
    return render_template('cover_letter.html', cover_letter=cover_letter_text)


@main.route('/choose-template')
def choose_template():
    if 'structured_resume' not in session:
        flash("Please analyze a resume first before choosing a template.")
        return redirect(url_for('main.index'))
    return render_template('template_chooser.html')


@main.route('/designer/<template_name>')
def designer(template_name):
    structured_data = session.get('structured_resume', None)
    if not structured_data:
        flash("Please analyze a resume first before accessing the designer.")
        return redirect(url_for('main.index'))
    session['last_template'] = template_name
    template_path = f"designs/{template_name}.html"
    return render_template(template_path, resume=structured_data)


@main.route('/export/docx', methods=['POST'])
def export_docx():
    data = request.get_json()
    html_content = data.get('html', '')
    if not html_content:
        return jsonify({'error': 'No HTML content received.'}), 400
    try:
        parser = Html2Docx()
        parser.parse_html_string(html_content)
        file_stream = io.BytesIO()
        parser.save(file_stream)
        file_stream.seek(0)
        return Response(
            file_stream,
            mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            headers={"Content-Disposition": "attachment;filename=resume_edited.docx"}
        )
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"; print(f"Error generating DOCX: {error_message}")
        return jsonify({'error': error_message}), 500

# The user's dashboard page
@main.route('/dashboard')
@login_required # This decorator protects the page, requiring login
def dashboard():
    # Query the database for all resumes belonging to the current user
    # Order them by most recent first
    resumes = Resume.query.filter_by(author=current_user).order_by(Resume.timestamp.desc()).all()
    return render_template('dashboard.html', resumes=resumes)


@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('main.login'))
        login_user(user, remember=form.remember_me.data)
        flash('You have been logged in successfully!')
        next_page = request.args.get('next')
        if not next_page:
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@main.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('main.login'))
    return render_template('register.html', title='Register', form=form)


@main.route('/analysis/<int:analysis_id>')
@login_required
def view_analysis(analysis_id):
    # Fetch the analysis by its ID, or return a 404 error if not found
    analysis = Analysis.query.get_or_404(analysis_id)

    # SECURITY CHECK: Ensure the analysis belongs to the currently logged-in user
    if analysis.resume.author != current_user:
        abort(403)  # Forbidden error

    return render_template('view_analysis.html', analysis=analysis)