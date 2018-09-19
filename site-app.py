from app import create_app
from app.main.config import headers
from app.main.routes import ALL_US_CATEGORIES_URL, getJSON

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'headers': headers, 'url': ALL_US_CATEGORIES_URL, 'getJSON':getJSON}
