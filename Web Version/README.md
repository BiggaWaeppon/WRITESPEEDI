# WriteSpeedi - Web Version

A professional web-based typing speed tester with modern UI and real-time feedback.

## Features

- User authentication and login
- Real-time typing speed feedback
- Detailed statistics and analytics
- Progress tracking
- Beautiful and responsive design

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```
   python -m venv venv
   ```
3. Activate the virtual environment:
   - Windows:
     ```
     venv\Scripts\activate
     ```
4. Install dependencies:
   ```
   pip install -r requirements_web.txt
   ```
5. Copy the example environment file:
   ```bash
   copy .env.example .env
   ```
6. Edit the `.env` file with your configuration:
   - Set a secure `SECRET_KEY`
   - Configure database settings
   - Adjust other settings as needed

## Running the Application

```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Configuration

The application uses environment variables for configuration. You can find an example configuration in [.env.example](.env.example). Copy this file to `.env` and modify the values as needed.

## Usage

1. Open your web browser and navigate to `http://localhost:5000`
2. Register or login to your account
3. Start a new typing test
4. View your progress and statistics

## Project Structure

```
Web Version/
├── app.py              # Flask application
├── main.py             # Main application logic
├── requirements_web.txt # Project dependencies
├── uml_diagram.puml    # UML diagrams
├── static/             # Static files (CSS, JS, images)
└── templates/          # HTML templates
```

## Development

For development purposes, ensure that `FLASK_ENV=development` in your `.env` file. This will enable debug mode and hot reloading.

## Security

- Never commit your `.env` file to version control
- Use a strong and unique `SECRET_KEY`
- Keep your database credentials secure

## Contributing

Please read [CONTRIBUTING.md](../../CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](../../LICENSE) file for details.
