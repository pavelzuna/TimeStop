# config.py

import web

from sqlalchemy import create_engine

engine = create_engine('sqlite:///timestop.db', echo=True)

view = web.template.render('templates', cache=False, globals=globals())

# end of file
