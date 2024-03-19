from app import create_app
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
from app.models.user import User
from app.models.contact import Contact
from app.models.ticket import Ticket, Ticket_Status, Ticket_Category
import os

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {
        'sa': sa,
        'so': so,
        'db': db,
        'User': User,
        'Contact': Contact,
        'Ticket': Ticket,
        'TStatus': Ticket_Status,
        'TCategory': Ticket_Category
    }

# this may need to be removed
# app.run(debug=True)
# i was right, this should have been removed.
if __name__ == "__main__":
    app.run(debug=True)