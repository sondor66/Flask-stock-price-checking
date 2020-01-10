import requests
import pandas as pd
from pandas import DataFrame
from bokeh.plotting import figure,output_file,show
from bokeh.palettes import Spectral11
from bokeh.embed import components 
from datetime import datetime, date
from flask import Flask,render_template,request,redirect,session

app = Flask(__name__)

app.vars={}



@app.route('/index', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/graph', methods=['POST'])
def graph():


    if request.method == 'POST':

        app.vars['ticker'] = request.form['ticker']


        url = 'https://www.quandl.com/api/v1/datasets/WIKI/%s.json?api_key=PQqYzRyDSiEk2WNX-7E7' % app.vars['ticker']
        r = requests.get(url)

        json = r.json()

        df = pd.DataFrame(json['data'], columns=json['column_names'])

        df['Date'] = pd.to_datetime(df['Date'])

        p = figure(title='Stock prices for %s' % app.vars['ticker'],
            x_axis_label='date',
            x_axis_type='datetime')

        if request.form.get('Close'):
            p.line(x=df['Date'].values, y=df['Close'].values,line_width=3, legend='Close')
        if request.form.get('Adj. Close'):
            p.line(x=df['Date'].values, y=df['Adj. Close'].values,line_width=3, line_color="blue", legend='Adj. Close')
        if request.form.get('Open'):
            p.line(x=df['Date'].values, y=df['Open'].values,line_width=3, line_color="orage", legend='Open')
        if request.form.get('Adj. Open'):
            p.line(x=df['Date'].values, y=df['Adj. Open'].values,line_width=3, line_color="red", legend='Adj. Open')
        #show(p)
        script, div = components(p)
        return render_template('graph.html', script=script, div=div)

@app.route('/')
def main():
  return redirect('/index')


if __name__ == '__main__':
    app.run(port=33508,debug = True)