import justpy as jp
import pandas as pd
from datetime import datetime
from pytz import utc

data = pd.read_csv('reviews.csv',parse_dates=['Timestamp'])
data['Month'] = data['Timestamp'].dt.strftime('%Y-%M')
month_average_crs = data.groupby(['Month','Course Name'])['Rating'].count().unstack()

month_average_crs.plot(figsize=(24,8))

chart_def = '''{
    chart: {
        type: 'spline'
    },
    title: {
        text: 'Ratings By Month Per Course'
    },
    legend: {
        layout: 'vertical',
        align: 'right',
        verticalAlign: 'top',
        x: 100,
        y: 50,
        floating: false,
        borderWidth: 1,
        backgroundColor:
             '#FFFFFF'
    },
    xAxis: {
        categories: [
           
        ],
        plotBands: [{ // visualize the weekend
            from: 4.5,
            to: 6.5,
            color: 'rgba(68, 170, 213, .2)'
        }]
    },
    yAxis: {
        title: {
            text: 'Course Ratings Count'
        }
    },
    tooltip: {
        shared: true,
        valueSuffix: ''
    },
    credits: {
        enabled: false
    },
    plotOptions: {
        areaspline: {
            fillOpacity: 0.5
        }
    },
    series: [{
        name: 'John',
        data: [3, 4, 3, 5, 4, 10, 12]
    }, {
        name: 'Jane',
        data: [1, 3, 4, 3, 3, 5, 4]
    }]
}
'''


def app():
    wp = jp.QuasarPage()
    h1 = jp.QDiv(a=wp,text='Course Analysis',classes='text-h3 text-center q-pa-md')
    p1 = jp.QDiv(a=wp,text='Analysis of course ratings and reviews', classes= 'text-center')
    
    hc = jp.HighCharts(a=wp,options=chart_def)
    hc.options.xAxis.categories=list(month_average_crs.index)
    hc.options.series[0].name=month_average_crs

    
    hc_data = [{'name':n,'data':[d for d in month_average_crs[n]]} for n in month_average_crs.columns]
    hc.options.series = hc_data
    return wp

jp.justpy(app)
