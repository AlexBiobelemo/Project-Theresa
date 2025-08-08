def test_index_page(client):
    """Test that the index page loads correctly."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Automated Resume Customizer" in response.data


def test_auth_pages(client):
    """Test that the login and register pages load correctly."""
    response = client.get('/login')
    assert response.status_code == 200
    assert b"Sign In" in response.data

    response = client.get('/register')
    assert response.status_code == 200
    assert b"Create an Account" in response.data


def test_api_analyze_with_mocking(client, mocker):
    """
    Test the /api/analyze route by mocking the AI call and file parsing.
    """
    # 1. Define a fake, successful response from our AI function
    mock_ai_response = {
        "analysis_results": {
            "match_score": 95,
            "missing_keywords": ["synergy"],
            "resume_suggestions": [],
            "cover_letter_themes": []
        },
        "structured_resume": {
            "full_name": "Test User"
        }
    }

    # 2. Use the 'mocker' fixture to patch our external calls
    mocker.patch('app.routes.get_combined_ai_data', return_value=mock_ai_response)


    mocker.patch('app.routes.get_text_from_file', return_value="This is the mocked resume text.")

    # 3. Simulate a file upload and form submission
    import io
    data = {
        'resume': (io.BytesIO(b"fake file content"), 'test.pdf'),
        'job_description': 'A test job description.'
    }

    # 4. Make the POST request to our API endpoint
    response = client.post('/api/analyze', data=data, content_type='multipart/form-data')

    # 5. Assert that the request was successful and returned the correct data
    assert response.status_code == 200
    json_response = response.get_json()
    assert json_response['analysis_results']['match_score'] == 95
    assert json_response['structured_resume']['full_name'] == "Test User"