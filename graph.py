from bokeh.sampledata import us_states, us_counties, unemployment
from bokeh.plotting import figure, show, output_file
import math
import scratch
from datetime import date
from bokeh.models import ColumnDataSource, CustomJS, LogColorMapper
from bokeh.models.widgets import DateSlider
from bokeh.layouts import layout

us_states = us_states.data.copy()
us_counties = us_counties.data.copy()
alldata = scratch.dict
unemployment = unemployment.data

# def myround(x, prec=1, base=.5):
#   return round(base * round(float(x)/base),prec)

del us_states["HI"]
del us_states["AK"]

state_xs = [us_states[code]["lons"] for code in us_states]
state_ys = [us_states[code]["lats"] for code in us_states]

county_xs=[us_counties[code]["lons"] for code in us_counties if us_counties[code]["state"] not in ["ak", "hi", "pr", "gu", "vi", "mp", "as"]]
county_ys=[us_counties[code]["lats"] for code in us_counties if us_counties[code]["state"] not in ["ak", "hi", "pr", "gu", "vi", "mp", "as"]]

fips = scratch.fips
# mapper = linear_cmap(field_name = '4/1/20', palette="Magma256", low=1, high=1000, low_color=None, high_color=None, nan_color='black')

colors = ['#FFDBDC', '#F598C7', '#FA7DFA', '#CA56F5', '#7701FF', '#3E04FF']
#color_mapper = LogColorMapper(palette=palette)

dates=[]

for x in alldata[1003]:
     if x == "countyFIPS" or x == "County Name" or x == "State" or x == "stateFIPS":
         continue
     dates.append(x)
print(dates)

#county_colors = []
#datas = {}

bigdict=dict(x=county_xs, y=county_ys)
for d in dates:
    lst=[]

    for county_id in us_counties:
        # print(county_id)
        fip = county_id[0]*1000 + county_id[1]
        #print(fip)
        if us_counties[county_id]["state"] in ["ak", "hi", "pr", "gu", "vi", "mp", "as"]:
            continue
        try:
            rate = alldata[fip][d]
            lst.append(rate)
            #if int(rate) == 0:
                #county_colors.append('#FFFDFB')
            #else:
                #rate = math.log(rate, 10)
                #print(rate)
                #idx = min(int(rate), 5)
                #print("length is " + str(len(colors)))
                #county_colors.append(colors[idx])
                #print("done")
        except KeyError:
            lst.append(0)
    #datas[d] = lst
    #bigdict[d] = lst
    pal = []
    for l in lst:
        if int(l) == 0:
            pal.append("#FAF4FB")
        else:
            pal.append(colors[min(int(math.log(l, 10)), 5)])
    bigdict[d] = pal
    #bigdict[d] = [colors[min(int(math.log(l+1, 10)), 5)] for l in lst]
        #county_colors.append("black")
    #datecolors[d] = county_colors

#county_colors = [colors[min(int(math.log(rate+1, 10)), 5)] for rate in datas['5/19/20']]


source = ColumnDataSource(data=bigdict)
p = figure(title="US Unemployment 2009", toolbar_location="left",
    plot_width=1100, plot_height=700)

renderer = p.patches('x', 'y', fill_color='4/20/20', fill_alpha=0.7,
    line_color="white", line_width=0.5, source=source,)
p.patches(state_xs, state_ys, fill_alpha=0.0,
    line_color="white", line_width=2)

#E0DEDC
date_range_slider = DateSlider(title="Date Range: ", start=date(2020, 1, 22), end=date.today(), value=(date(2020, 1, 22)), step=1)
callback = CustomJS(args=dict(source=source, renderer=renderer),
                    code="""
                        var s = source.data;
                        var selected_date = new Date(cb_obj.value);
                        var month = selected_date.getMonth() + 1;
                        var day = selected_date.getDate();
                        var year = selected_date.getFullYear().toString().substr(-2);
                        var selected_js_date = month + "/" + day + "/" + year;
                        console.log(selected_js_date);
                        renderer.glyph.fill_color.field = selected_js_date;
                        source.change.emit();
                      """)
date_range_slider.js_on_change('value', callback)
#callback.args["selecteddate"] = date_range_slider.value_as_date.strftime('%-m/%-d/%y')
# print(date_range_slider.value_as_date.strftime('%-m/%-d/%y'))
output_file("choropleth.html", title="choropleth.py example")
#callback.args["selecteddate"] = date_range_slider



l = layout(children=[date_range_slider, p], sizing_mode='fixed')
show(l)
