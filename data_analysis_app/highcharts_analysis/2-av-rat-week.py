import justpy as jp
import pandas as pd
from datetime import datetime
from pytz import utc

data = pd.read_csv('reviews.csv',parse_dates=['Timestamp'])
data['Week'] = data['Timestamp'].dt.strftime('%Y-%U')
week_average = data.groupby(['Week']).mean()
week_average['Rating'] = week_average['Rating'].apply(lambda x: round(x,2))

chart_def= '''
 {
    chart: {
        type: 'spline',
        inverted: false
    },
    title: {
        text: 'Average Ratings By Week'
    },
    subtitle: {
        text: 'According to the Standard Atmosphere Model'
    },
    xAxis: {
        reversed: false,
        title: {
            enabled: true,
            text: 'Date'
        },
        labels: {
            format: '{value}'
        },
        maxPadding: 0.05,
        showLastLabel: true
    },
    yAxis: {
        title: {
            text: 'Rating'
        },
        labels: {
            format: '{value}°'
        },
        lineWidth: 2
    },
    legend: {
        enabled: false
    },
    tooltip: {
        headerFormat: '<b>{series.name}</b><br/>',
        pointFormat: '{point.x}: {point.y}'
    },
    plotOptions: {
        spline: {
            marker: {
                enable: false
            }
        }
    },
    series: [{
        name: 'Rating',
        data: []
        }]
}

'''

def app():
    wp = jp.QuasarPage()
    h1 = jp.QDiv(a=wp,text='Course Analysis',classes='text-h3 text-center q-pa-md')
    p1 = jp.QDiv(a=wp,text='Analysis of course ratings and reviews', classes= 'text-center')
    hc = jp.HighCharts(a=wp,options=chart_def)
    hc.options.xAxis.categories = list(week_average.index)
    hc.options.series[0].data = list(week_average['Rating'])
    return wp

jp.justpy(app)
