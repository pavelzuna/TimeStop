# timestop.py

import web
import json
import datetime

from sqlalchemy import desc

from config import view
from app.models.log import Log

class index:
    def GET(self):
        logs = web.ctx.orm.query(Log).order_by(desc(Log.date)).limit(1).all()
        if len(logs) == 0 or logs[0].type != 'STOP':
            return view.index(datetime, datetime.datetime.utcnow(), False)
        else:
            return view.index(datetime, logs[0].date, True)

class log:
    def _compute_gap(self, total_seconds):
        days = int(total_seconds / (3600 * 24))
        total_seconds -= days * 3600 * 24
        hours = int(total_seconds / 3600)
        total_seconds -= hours * 3600
        minutes = int(total_seconds / 60)
        total_seconds -= minutes * 60;
        return '%d days, %d hours, %d minutes, %d seconds' % (
            days, hours, minutes, total_seconds + 0.5
        )

    def GET(self):
        logs = web.ctx.orm.query(Log).order_by(desc(Log.date)).all()
        output = []
        total_time = datetime.timedelta(0)
        date_now = datetime.datetime.utcnow()
        for (i, l) in enumerate(logs):
            if l.type == 'STOP':
                # ignore consecutive STOPs, can happen due to race condition
                if i < (len(logs) - 1) and logs[i + 1].type == 'STOP':
                    continue
                delta = date_now - l.date 
                output.append(Log(self._compute_gap(delta.total_seconds()), l.date))
                total_time += delta
                output.append(l)
            else:
                date_now = l.date;
                output.append(l)
        return view.log(datetime, output, self._compute_gap(total_time.total_seconds()))

class check:
    def GET(self):
        logs = web.ctx.orm.query(Log).order_by(desc(Log.date)).limit(1).all()
        is_stopped = len(logs) != 0 and logs[0].type == 'STOP'
        date_now = datetime.datetime.utcnow()
        if is_stopped:
            date_now = logs[0].date;
        timestamp = (date_now - datetime.datetime.utcfromtimestamp(0)).total_seconds()
        return json.dumps({'success': True, 'data': {'is_stopped': is_stopped, 'timestamp': timestamp}});

class stop:
    def GET(self):
        web.ctx.orm.add(Log('STOP', datetime.datetime.utcnow()))
        return json.dumps({'success': True, 'data': {}});

class restart:
    def GET(self):
        web.ctx.orm.add(Log('RESTART', datetime.datetime.utcnow()))
        return json.dumps({'success': True, 'data': {}});

# end of file
