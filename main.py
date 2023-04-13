from data.db import init_db
from data.__init__ import create_app
from database import add_info


if __name__ == '__main__':
    init_db()
    app = create_app()
    app.run()
