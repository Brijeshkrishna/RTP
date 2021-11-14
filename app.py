import re
from flask import Flask,render_template,request,redirect,url_for

app = Flask(__name__,static_folder='templates')
import datetime


PIRNTMESSAGE = 'Enter RTP code : '

expression = 'y+x+d+h+m'


def getComputerDict(date_time: datetime.datetime):
    date_time_ = date_time.strftime("%Y,%m,%d,%H,%M").split(",")
    return {
        'y': int(date_time_[0]),
        'x': int(date_time_[1]),
        'd': int(date_time_[2]),
        'h': int(date_time_[3]),
        'm': int(date_time_[4]),
    }


def timebasegenerator():
    date_time = datetime.datetime.now()
    print(date_time)
    return date_time


def checktime(initial: datetime.datetime, offset_s=20, offset_m=0):
    if (initial + datetime.timedelta(seconds=offset_s, minutes=offset_m)) \
            > datetime.datetime.now():
        return True
    else:
        return False


def evaluate_computer_dict(genrator_time_data):
    try:
        return eval(expression, getComputerDict(genrator_time_data))
    except NameError:
        raise("all values are not given")


def check(genrator_time_data: datetime.datetime, user_value):

    if checktime(offset_s=60, initial=genrator_time_data):
        computer_value = evaluate_computer_dict(genrator_time_data)
        if str(computer_value) == str(user_value):
            return 1
        else:
            return 2
    else:
        return 3




def style():
    data  = timebasegenerator().strftime('%Y,%m,%d,%H,%M').split(",")
    return data



@app.route('/login',methods=['GET','POST'])
def login():
    

    if request.method == 'POST':
        
        data =   request.form['code']
        
        return redirect(url_for('user_login',data=data,time_data=timebasegenerator().strftime('%Y:%m:%d - %H:%M')))
    else:
    
        msg= request.query_string.decode('utf-8').split("=")[-1]
   
        return render_template("base.html",data=style(),msg=msg)



@app.route('/<data>/<time_data>')
def user_login(data,time_data):
    data_comput = datetime.datetime.strptime(time_data, "%Y:%m:%d - %H:%M" )
    s =check(data_comput,data)
    if  s== 1 :
        return 'sucessful'

    elif s==2:
        return redirect(f'/login?h={"wroungpassword"}')
    else :
        return redirect(f'/login?h={"timeout"}')

        



