import sqlalchemy as sa
import sqlalchemy.orm as so
from app import create_app, db
from app.models.user import User
from app.models.contact import Contact

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {
        'sa': sa,
        'so': so,
        'db': db,
        'User': User,
        'Contact': Contact

    }

# this may need to be removed
app.run(debug=True)