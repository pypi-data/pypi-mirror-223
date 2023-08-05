# custom application views

from datetime import date

from logilab.mtconverter import xml_escape
from logilab.common.date import date_range, todate, todatetime

from cubicweb import _
from cubicweb.predicates import adaptable, empty_rset
from cubicweb_web.view import EntityView
from cubicweb_web.views import calendar


# one day calendar view for day of conference
class OneDayCal(EntityView):
    """Render a one day calendar view"""

    __regid__ = "onedaycal"
    __select__ = empty_rset | adaptable("ICalendarable")
    paginable = False
    title = _("one day")

    def call(self):
        self._cw.add_js(("cubicweb.ajax.js", "cubicweb.calendar.js"))
        self._cw.add_css("cubicweb.calendar.css")
        task_colors = {}  # remember a color assigned to a task
        day = self.cw_extra_kwargs.get("day", date.today())
        title = self.cw_extra_kwargs.get("title", "")
        # colors here are class names defined in cubicweb.css
        colors = [f"col{i:x}" for i in range(12)]
        next_color_index = 0
        done_tasks = []
        task_descrs = []
        day = todate(day)
        for row in range(self.cw_rset.rowcount):
            task = self.cw_rset.get_entity(row, 0)
            if task.eid in done_tasks:
                continue
            done_tasks.append(task.eid)
            the_dates = []
            event = task.cw_adapt_to("ICalendarable")
            tstart = event.start
            tstop = event.stop
            if tstart:
                tstart = todate(tstart)
                if tstart != day:
                    continue
                the_dates = [tstart]
            if tstop:
                tstop = todate(tstop)
                if tstop != day:
                    continue
                the_dates = [tstop]
            if tstart and tstop:
                the_dates = date_range(max(tstart, day), min(tstop, day))
            if not the_dates:
                continue

            if task not in task_colors:
                task_colors[task] = colors[next_color_index]
                next_color_index = (next_color_index + 1) % len(colors)

            # add task description for the given day
            task_descr = calendar._TaskEntry(task, task_colors[task])
            task_descrs.append(task_descr)

        self.w('<div id="oneweekcalid">')
        # build schedule for the given day
        self._build_schedule(day, task_descrs, title)

        self.w("</div>")
        self.w('<div id="coord"></div>')
        self.w('<div id="debug">&#160;</div>')

    def _build_schedule(self, date, task_descrs, title):
        _cw = self._cw
        if "year" in _cw.form:
            year = int(_cw.form["year"])
        else:
            year = date.year
        if "week" in _cw.form:
            week = int(_cw.form["week"])
        else:
            week = date.isocalendar()[1]
        self.w('<table class="omcalendar" id="week">')
        self.w('<tr><th class="transparent"></th></tr>')

        # output header
        self.w("<tr>")
        self.w('<th class="transparent"></th>')  # column for hours
        _today = date.today()
        wdate = date
        if wdate.isocalendar() == _today.isocalendar():
            if title:
                self.w(
                    '<th class="today">%s<br/>%s %s</th>'
                    % (
                        title,
                        _cw._(calendar.WEEKDAYS[date.weekday()]),
                        _cw.format_date(wdate),
                    )
                )
            else:
                self.w(
                    '<th class="today">%s<br/>%s</th>'
                    % (_cw._(calendar.WEEKDAYS[date.weekday()]), _cw.format_date(wdate))
                )
        else:
            if title:
                self.w(
                    "<th>%s<br/>%s %s</th>"
                    % (
                        title,
                        _cw._(calendar.WEEKDAYS[date.weekday()]),
                        _cw.format_date(wdate),
                    )
                )
            else:
                self.w(
                    "<th>%s<br/>%s</th>"
                    % (_cw._(calendar.WEEKDAYS[date.weekday()]), _cw.format_date(wdate))
                )
        self.w("</tr>")

        # build day calendar
        self.w("<tr>")
        self.w('<td style="width:1%;">')  # column for hours
        extra = ""
        for h in range(8, 20):
            self.w(f'<div class="hour" {extra}>')
            self.w("%02d:00" % h)
            self.w("</div>")
        self.w("</td>")

        wdate = date
        classes = ""
        if wdate.isocalendar() == _today.isocalendar():
            classes = " today"
        self.w(
            f'<td class="column {classes}" id="{calendar.WEEKDAYS[date.weekday()]}">'
        )
        if len(self.cw_rset.column_types(0)) == 1:
            etype = list(self.cw_rset.column_types(0))[0]
            url = _cw.build_url(
                vid="creation",
                etype=etype,
                schedule=True,
                __redirectrql=self.cw_rset.printable_rql(),
                __redirectparams=_cw.build_url_params(year=year, week=week),
                __redirectvid=self.__regid__,
            )
            extra = (
                ' ondblclick="addCalendarItem(event, hmin=8, hmax=20, '
                "year=%s, month=%s, day=%s, duration=2, baseurl='%s')\""
                % (wdate.year, wdate.month, wdate.day, xml_escape(url))
            )
        else:
            extra = ""
        self.w(f'<div class="columndiv"{extra}>')
        for h in range(8, 20):
            self.w(f'<div class="hourline" style="top:{(h - 7) * 8}ex;">')
            self.w("</div>")
        self._build_calendar_cell(wdate, task_descrs)

        self.w("</div>")
        self.w("</td>")
        self.w("</tr>")
        self.w("</table>")

    def _build_calendar_cell(self, date, task_descrs):
        inday_tasks = [
            t for t in task_descrs if t.is_one_day_task() and t.in_working_hours()
        ]
        wholeday_tasks = [t for t in task_descrs if not t.is_one_day_task()]
        inday_tasks.sort(key=lambda t: t.task.cw_adapt_to("ICalendarable").start)
        sorted_tasks = []
        for i, t in enumerate(wholeday_tasks):
            t.index = i
        ncols = len(wholeday_tasks)
        while inday_tasks:
            t = inday_tasks.pop(0)
            for i, c in enumerate(sorted_tasks):
                if (
                    not c
                    or c[-1].task.cw_adapt_to("ICalendarable").stop
                    <= t.task.cw_adapt_to("ICalendarable").start
                ):
                    c.append(t)
                    t.index = i + ncols
                    break
            else:
                t.index = len(sorted_tasks) + ncols
                sorted_tasks.append([t])
        ncols += len(sorted_tasks)
        if ncols == 0:
            return

        inday_tasks = []
        for tasklist in sorted_tasks:
            inday_tasks += tasklist
        width = 100.0 / ncols
        for task_desc in wholeday_tasks + inday_tasks:
            task = task_desc.task
            start_hour = 8
            start_min = 0
            stop_hour = 20
            stop_min = 0
            event = task.cw_adapt_to("ICalendarable")
            if event.start:
                if (
                    todatetime(date)
                    < todatetime(event.start)
                    < todatetime(date + calendar.ONEDAY)
                ):
                    start_hour = max(8, event.start.hour)
                    start_min = event.start.minute
            if event.stop:
                if (
                    todatetime(date)
                    < todatetime(event.stop)
                    < todatetime(date + calendar.ONEDAY)
                ):
                    stop_hour = min(20, event.stop.hour)
                    if stop_hour < 20:
                        stop_min = event.stop.minute

            height = (
                100.0
                * (stop_hour + stop_min / 60.0 - start_hour - start_min / 60.0)
                / (20 - 8)
            )
            top = 100.0 * (start_hour + start_min / 60.0 - 8) / (20 - 8)
            left = width * task_desc.index
            style = f"height: {height}%; width: {width}%; top: {top}%; left: {left}%; "
            self.w(f'<div class="task {task_desc.color}" style="{style}">')
            task.view("calendaritem", dates=False, w=self.w)
            params = self._cw.build_url_params(
                year=date.year, week=date.isocalendar()[1]
            )
            url = task.absolute_url(
                vid="edition",
                __redirectrql=self.cw_rset.printable_rql(),
                __redirectparams=params,
                __redirectvid=self.__regid__,
            )

            self.w(
                '<div class="tooltip" ondblclick="stopPropagation(event); '
                "window.location.assign('%s'); return false;\">" % xml_escape(url)
            )
            task.view("tooltip", w=self.w)
            self.w("</div>")
            if event.start is None:
                self.w(
                    '<div class="bottommarker">'
                    '<div class="bottommarkerline" '
                    'style="margin: 0px 3px 0px 3px; height: 1px;"></div>'
                    '<div class="bottommarkerline" '
                    'style="margin: 0px 2px 0px 2px; height: 1px;"></div>'
                    '<div class="bottommarkerline" '
                    'style="margin: 0px 1px 0px 1px; height: 3ex; '
                    "color: white; font-size: x-small; vertical-align: center; "
                    'text-align: center;">end</div>'
                    "</div>"
                )
            self.w("</div>")
