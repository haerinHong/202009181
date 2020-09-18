from django.shortcuts import render

# Create your views here.
import pandas as pd

def main_view(request):
    df = pd.read_csv(r'C:\Users\Playdata\Downloads\covid19.csv')
    labels = list(map(str,df['stateDt'].values.tolist()[1:]))
    data =  df['new'].values.tolist()[1:]
    return render(request, 'line-chart.html', {
        'labels' : labels,
        'data' : data,

    })
