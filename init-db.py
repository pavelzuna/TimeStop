#!/usr/bin/env python

import config
import app.models.log

if __name__ == '__main__':
    app.models.log.metadata.create_all(config.engine)

# end of file
