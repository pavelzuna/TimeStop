#!/usr/bin/env python

import web
import config

from sqlalchemy.orm import scoped_session, sessionmaker

urls = (
    '/', 'app.controllers.timestop.index',
    '/log/', 'app.controllers.timestop.log',
    '/check', 'app.controllers.timestop.check',
    '/stop', 'app.controllers.timestop.stop',
    '/restart', 'app.controllers.timestop.restart'
)

def load_sqlalchemy(handler):
    web.ctx.orm = scoped_session(sessionmaker(bind=config.engine))
    try:
        return handler()
    except web.HTTPError:
        web.ctx.orm.commit()
        raise
    except:
        web.ctx.orm.rollback()
        raise
    finally:
        web.ctx.orm.commit()
        # web.ctx.orm.expunge_all()

app = web.application(urls, globals())
app.add_processor(load_sqlalchemy)

if __name__ == '__main__':
    app.run()

# end of file
