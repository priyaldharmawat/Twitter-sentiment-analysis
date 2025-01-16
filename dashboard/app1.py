## flask dependencies
from flask import Flask, render_template, redirect, url_for,flash,Markup
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy  import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

## Dash dependencies
import dash
from dash.dependencies import Input, Output,State
import dash_core_components as dcc
import dash_html_components as html

##ML model dependencies
import pandas as pd
import datetime as dt
import warnings
import itertools
import numpy as np
import statsmodels.api as sm

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50))
    password = db.Column(db.String(80))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])


@app.route('/')
def index():
    return render_template('index3.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('/dash/'))
        message = Markup("<br><h1><center>No user of name {},go and <a href = '/signup'> signup </a></center></h1>".format(form.username.data))
        flash(message)
        return render_template('output.html')#'<h1>Invalid username or password</h1>'
        #return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'

    return render_template('login4.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        
        message = Markup("<br><h1><center>New user created go ahead and <a href = '/login'>log in</a> to your account</center></h1>")
        #flash()
        flash(message)
        return render_template('output.html')

    return render_template('signup1.html', form=form)

#@app.route('/dashboard')
#@login_required
#def dashboard():
#    return render_template('dashboard1.html', name=current_user.username)
server = dash.Dash(server=app, external_stylesheets=external_stylesheets,url_base_pathname='/dash/')
server.layout = html.Div([
    html.H1('PRODUCTS SALES FORECAST',style = {'textAlign' : 'center'}),
    html.Hr(),
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        #multiple=True
    ),
    html.Div(id='output-data-upload'),
    html.Div(
    dcc.Dropdown(
            id='my-dropdown',
            options=[
                {'label': 'Cakes', 'value': 'Cakes'},
                {'label': 'Pies', 'value': 'Pies'},
                {'label': 'Smoothies', 'value': 'Smoothies'},
                {'label': 'Coffee', 'value': 'Coffee'},
                {'label': 'Cookies', 'value': 'Cookies'}
            ],
            value='Cakes'
        ),style={'width': '49%', 'display': 'inline-block'}),
    html.Div(
    dcc.Dropdown(
            id='my-dropdown1',
            options=[
                {'label': '10 Days', 'value': 10},
                {'label': '20 Days', 'value': 20},
                {'label': '30 Days', 'value': 30},
                {'label': '40 Days', 'value': 40},
                {'label': '50 Days', 'value': 50}
            ],
            value=10
        ),style={'width': '49%', 'display': 'inline-block'}),
    



    html.Hr(),
    dcc.Graph(id='my-graph'),
])



    #print(type(l))
    #return l[0]#'The input value was "{}{}{}{}" and the button has been clicked'.format(
        #value,value1,value2,value3)

@server.callback(
    Output('my-graph', 'figure'),

    [Input('upload-data','children'),
    Input('my-dropdown', 'value'),
    Input('my-dropdown1', 'value')],
    [State('upload-data', 'filename')])

def update_output(filename0,selected_dropdown_value1,selected_dropdown_value2,filename):
    while(filename):
        print(filename)
        df1 = pd.read_csv('/home/shantanu/Desktop/AI Adventure/Project/dashbord/'+filename,sep = ',')
        #print(df1['Date'])
        #df1 = df1.reset_index()
        print(df1['Date'])
        df1['Date'] = df1['Date'].apply(lambda x :dt.datetime.strptime(x,"%m/%d/%Y"))
        df1 = df1.set_index('Date')
        df1['promotion'] = df1['promotion'].replace({'none': 0, 'promotion': 1})
        #df = df.resample('w').mean()   
        dat1 = round(df1.iloc[:,:6])
        print("Shape of data:",round(dat1.shape[0]*0.95))
        y  = dat1[dat1.index[round(dat1.shape[0]*0.95)]:]
        dff = y
        mod = sm.tsa.statespace.SARIMAX(dff[selected_dropdown_value1],order=(1, 1, 1),seasonal_order=(1, 1, 0, 12),enforce_stationarity=False,
            enforce_invertibility=False)
        results = mod.fit()
        pred = results.get_prediction(start=pd.to_datetime(dff.index[-1]), dynamic=False)
        pred_ci = pred.conf_int()
        y_forecasted = pred.predicted_mean
        y_truth = dff[selected_dropdown_value1][dff.index[-1]:]
        pred_uc = results.get_forecast(steps=selected_dropdown_value2)
        pred_ci = pred_uc.conf_int()
        print(pred_uc.predicted_mean.max())
        print("Last week's mean",dff[:7][selected_dropdown_value1].mean())
        #print(dff.index[0],dff.index[-1])
        #print(type(value),type(value1),value2,value3)
        """l = []
                                l.append(value)
                                l.append(value1)
                                l.append(value2)
                                l.append(value3)
                                if((value!='')&(value1!='')&(value2!='')&(value3!='')):
                                    print(l)"""
        return {
            'data': [{

                'x': pred_uc.predicted_mean.index,
                'y': list(round(pred_uc.predicted_mean).values.reshape(-1)),'name': 'Prediction',
                'line': {
                    'width': 3,
                    'shape': 'spline'

                }

            },{'x': dff[selected_dropdown_value1].index, 'y': list(round(dff[selected_dropdown_value1]).values.reshape(-1)),'name': 'previous values'}],
            'layout': {
                'margin': {
                    'l': 100,
                    'r': 100,
                    'b': 100,
                    't': 100
                }
            }
        }    



@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index3'))

if __name__ == '__main__':
    server.run_server(debug=True)