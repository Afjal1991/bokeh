""" Based on http://www.nytimes.com/interactive/2012/08/05/sports/olympics/the-100-meter-dash-one-race-every-medalist-ever.html

"""

from bokeh.models import (Arrow, ColumnDataSource, CustomJS, Label,
                          NormalHead, SingleIntervalTicker, TapTool)
from bokeh.plotting import figure, output_file, show
from bokeh.sampledata.sprint import sprint

abbrev_to_country = {
    "USA": "United States",
    "GBR": "Britain",
    "JAM": "Jamaica",
    "CAN": "Canada",
    "TRI": "Trinidad and Tobago",
    "AUS": "Australia",
    "GER": "Germany",
    "CUB": "Cuba",
    "NAM": "Namibia",
    "URS": "Soviet Union",
    "BAR": "Barbados",
    "BUL": "Bulgaria",
    "HUN": "Hungary",
    "NED": "Netherlands",
    "NZL": "New Zealand",
    "PAN": "Panama",
    "POR": "Portugal",
    "RSA": "South Africa",
    "EUA": "United Team of Germany",
}

fill_color = { "gold": "#efcf6d", "silver": "#cccccc", "bronze": "#c59e8a" }
line_color = { "gold": "#c8a850", "silver": "#b0b0b1", "bronze": "#98715d" }


def selected_name(name, medal, year):
    return name if medal == "gold" and year in [1988, 1968, 1936, 1896] else ""


t0 = sprint.Time[0]

sprint["Abbrev"]       = sprint.Country
sprint["Country"]      = sprint.Abbrev.map(lambda abbr: abbrev_to_country[abbr])
sprint["Medal"]        = sprint.Medal.map(lambda medal: medal.lower())
sprint["Speed"]        = 100.0/sprint.Time
sprint["MetersBack"]   = 100.0*(1.0 - t0/sprint.Time)
sprint["MedalFill"]    = sprint.Medal.map(lambda medal: fill_color[medal])
sprint["MedalLine"]    = sprint.Medal.map(lambda medal: line_color[medal])
sprint["SelectedName"] = sprint[["Name", "Medal", "Year"]].apply(tuple, axis=1).map(lambda args: selected_name(*args))

source = ColumnDataSource(sprint)

tooltips = """
<div>
    <span style="font-size: 15px;">@Name</span>&nbsp;
    <span style="font-size: 10px; color: #666;">(@Abbrev)</span>
</div>
<div>
    <span style="font-size: 17px; font-weight: bold;">@Time{0.00}</span>&nbsp;
    <span style="font-size: 10px; color: #666;">@Year</span>
</div>
<div style="font-size: 11px; color: #666;">@{MetersBack}{0.00} meters behind</div>
"""

plot = figure(
    x_range=(sprint.MetersBack.max()+2, 0),
    width=1000, height=600,
    toolbar_location=None,
    outline_line_color=None,
    y_axis_location="right",
    tooltips=tooltips)
plot.y_range.range_padding = 4
plot.y_range.range_padding_units = "absolute"

plot.title.text = "Usain Bolt vs. 116 years of Olympic sprinters"
plot.title.text_font_size = "19px"

plot.xaxis.ticker = SingleIntervalTicker(interval=5, num_minor_ticks=0)
plot.xaxis.axis_line_color = None
plot.xaxis.major_tick_line_color = None
plot.xgrid.grid_line_dash = "dashed"

plot.yaxis.ticker = [1900, 1912, 1924, 1936, 1952, 1964, 1976, 1988, 2000, 2012]
plot.yaxis.major_tick_in = -5
plot.yaxis.major_tick_out = 10
plot.ygrid.grid_line_color = None

medal_circle = plot.circle(x="MetersBack", y="Year", radius=dict(value=5, units="screen"),
                           fill_color="MedalFill", line_color="MedalLine", fill_alpha=0.5,
                           source=source, level="overlay")
plot.hover.renderers = [medal_circle]

plot.text(x="MetersBack", y="Year", x_offset=10, y_offset=-5, text="SelectedName",
          text_align="left", text_baseline="middle", text_font_size="12px", source=source)

no_olympics_label = Label(
    x=7.5, y=1942,
    text="No Olympics in 1940 or 1944",
    text_align="center", text_baseline="middle",
    text_font_size="12px", text_font_style="italic", text_color="silver")
plot.add_layout(no_olympics_label)

x = sprint[sprint.Year == 1900].MetersBack.min() - 0.5
arrow = Arrow(x_start=x, x_end=5, y_start=1900, y_end=1900, start=NormalHead(fill_color="black", size=6),
              end=None, line_width=1.5)
plot.add_layout(arrow)

meters_back = Label(
    x=5, x_offset=10, y=1900,
    text="Meters behind 2012 Bolt",
    text_align="left", text_baseline="middle",
    text_font_size="13px", text_font_style="bold")
plot.add_layout(meters_back)

disclaimer = Label(
    x=0, y=0, x_units="screen", y_units="screen",
    text="This chart includes medals for the United States and Australia in the \"Intermediary\" Games of 1906, which the I.O.C. does not formally recognize.",
    text_font_size="11px", text_color="silver")
plot.add_layout(disclaimer, "below")

open_url = CustomJS(args=dict(source=source), code="""
source.inspected.indices.forEach(function(index) {
    const name = source.data["Name"][index];
    const url = "http://en.wikipedia.org/wiki/" + encodeURIComponent(name);
    window.open(url);
});
""")

plot.add_tools(TapTool(callback=open_url, renderers=[medal_circle], behavior="inspect"))

output_file("sprint.html", plot.title.text)
show(plot)
