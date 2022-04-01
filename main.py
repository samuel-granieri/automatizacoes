#app libraries
from website import creat_app


#initialize method from __init__.py
app = creat_app()



if __name__ == ('__main__'):
    app.run(debug=True)
