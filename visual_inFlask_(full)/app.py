from flask import Flask, render_template ,jsonify ,Response,redirect,url_for
from flask_mysqldb import MySQL
import os.path
#import mysql.connector
import mysql.connector
import sqlalchemy 
import json
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


from database import load_keywords_from_db,load_keyword_all_details,fetch_commits_data_from_github,get_commits_date_from_db,get_dashboard_data,get_created_date,get_languages_data_from_db

app = Flask("__name__")


@app.route("/")
def home():
  keyword_data = load_keywords_from_db()
  #print(type(keyword_data))
  return render_template('home.html',
                        data = keyword_data,
                        company_name = "Where's My Repo"
                        )

@app.route("/tables")
def prep_tables():
  keyword_data = load_keywords_from_db()
  #print(type(keyword_data))   #list
  #keyword_data = json.dumps(keyword_data,default=str) converts data type to string
  #print(type(keyword_data))
  return jsonify(keyword_data)


@app.route("/tables/<keyword_id>/<id>")
def get_commit_data(keyword_id,id):
  fetch_commits_data_from_github(keyword_id,id)
  #return show_more_tables(keyword_id)
  return redirect(url_for("show_more_tables",keyword_id = keyword_id))


@app.route("/tables/<keyword_id>")
def show_more_tables(keyword_id):
  all_details = load_keyword_all_details(keyword_id)
  dates,count = get_created_date(keyword_id)

  dd =[]
  com_count = []
  for d in dates:
    dd.append(d)
  for c in count:
    com_count.append(c)

  print(dd,com_count)

  return render_template('show_all_details.html', 
                        details = all_details,
                        dates = json.dumps(dd),
                        counts = json.dumps(com_count),
                        company_name = "Where's My Repo")

'''
@app.route("/graphtrial.png", methods=["GET","POST"])
def graph_trial():
  fig = create_figure()
  output = io.BytesIO()
  FigureCanvas(fig).print_png(output)
  return Response(output.getvalue(), mimetype='image/png')
'''
'''id= 4332096
  labels,values = get_commits_date_from_db(id)
  #print(labels)
  return jsonify(labels)
'''

@app.route("/keyword_dashboard")
def key_dashboard():
  label,datavalue,ac_count = get_dashboard_data()
  #dates,dcount = get_commits_date_from_db(759578)
  language,lcount = get_languages_data_from_db()

  lang = []
  lang_count = []
  for l in language:
    lang.append(l)
  for lc in lcount:
    lang_count.append(lc)


  return render_template("all_graphs.html",
                          mydata = json.dumps(datavalue),
                          label = json.dumps(label),
                          ac_count = json.dumps(ac_count),
                          language = json.dumps(lang),
                          lang_count = json.dumps(lang_count))

  
@app.route("/graph/<id>" , methods=["GET","POST"])
def plot_commit_graph(id):
 # x,y = get_commits_date_from_db(id)
  dates,count = get_commits_date_from_db(id)
  dd =[]
  com_count = []
  for d in dates:
    dd.append(d)
  for c in count:
    com_count.append(c)
  return render_template("graph.html",
                          dates = json.dumps(dd),
                          count =json.dumps(com_count))
'''
  ax1 = plt.subplot2grid((3, 5), (0, 0), colspan=5)
  plt.plot(x, y)
  #ax1.xaxis.set_major_locator(mdates.YearLocator(5))
  print(x)
  print(y)
  ax1.set_ylabel("Number Of Commits")
  #ax = plt.gca()
  #ax.xaxis.set_major_locator(mdates.MonthLocator(interval=4))
  #ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y'))
  #plt.gcf().autofmt_xdate() # Rotation
  ax1.legend().set_visible(False)
  #plt.plot(x,y)
  #plt.title("Linechart")
  plt.savefig("static/plot.png" ,dpi = 2000)

  return render_template('graph.html', url = 'static/images/plot.png')
'''
''' 
  #  print("inside the function")
  left = [1, 2, 3, 4, 5]
  # heights of bars
    height = [10, 24, 36, 40, 5]
    # labels for bars
    tick_label = ['one', 'two', 'three', 'four', 'five']
    # plotting a bar chart
    plt.bar(left, height, tick_label=tick_label, width=0.8, color=['red', 'green'])

    # naming the y-axis
    plt.ylabel('y - axis')
    # naming the x-axis
    plt.xlabel('x - axis')
    # plot title
    plt.title('My bar chart!')

    plt.savefig('static/images/plot.png')

    return render_template('plot.html', url='/static/images/plot.png')

  fig = Figure()
  axis = fig.add_subplot(1, 1, 1)
  xs,ys = get_commits_date_from_db()
  axis.plot(xs, ys)
  return fig

  label, value = get_commits_date_from_db(id)
  #print(value)
  #labels = [row[0] for row in data
  return render_template('graph.html',
                          labels = label,
                          values = value)
'''
  
#get_commits_date(4332096)


@app.route("/trial")
def trial():
  render_template('show_all_details.html')
  return render_template('show_all_details.html',
                            company_name = "Where's My Repo")

if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)
