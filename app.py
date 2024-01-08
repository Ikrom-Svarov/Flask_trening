from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# создаем объект для доступа ко всем функциям flask
app  = Flask(__name__)

# подключаем базу данных
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'

# создаем обьект для доступа к базе данных
db = SQLAlchemy(app)



# создаем таблицу базы данных
class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False) 
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"Article {self.id}"

with app.app_context():
    db.create_all()
         
     


#создаем страницу 
@app.route('/')
@app.route('/houm') # два url на одной функции
def index():
        return render_template("index.html") 


#создаем страницу 
@app.route('/about')
def about():
    return render_template("about.html")


#создаем страницу для отображения записей базы данных
@app.route('/posts', methods=['GET'])
def posts():
    articles = Article.query.order_by(Article.date.desc()).all()
    
    return render_template("posts.html", articles=articles)


#создаем страницу для отображения одной записи из  базы данных
@app.route('/posts/<int:id>', methods=['GET'])
def post_detail(id):
    article= Article.query.get(id)
    return render_template("post-detail.html", article=article)


#создаем функцию для удаления записи
@app.route('/posts/<int:id>/del', methods=['POST', 'GET'])
def post_delete(id):
    article = Article.query.get_or_404(id)

    if request.method == 'POST':

        try:
            db.session.delete(article)
            db.session.commit()
            return redirect('/posts')

        except:
            return 'Error'
        
    return render_template("post-delete.html", article=article)




#создаем страницу для добавления статьи
@app.route('/create-article', methods=['POST', 'GET'])
def create_article():
    if request.method == "POST":
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        article = Article(title=title, intro=intro, text=text)
        
        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/posts')
        except:
            return "Error"

    else:
        return render_template("create-article.html")
    



#создаем страницу для обнавления статьи
@app.route('/posts/<int:id>/update', methods=['POST', 'GET'])
def post_update(id):
    article = Article.query.get(id)
    
    if request.method == "POST":
        article.title = request.form['title']
        article.intro = request.form['intro']
        article.text = request.form['text']
        
        try:
            db.session.commit()
            return redirect('/posts')
        except:
            return "Error"

    else:
        return render_template("post-update.html", article=article)



# это условие нужно для того чтобы запустить программу
# если этот файил евляется  основным то тогда запускается программа 
if __name__ == '__main__':
    app.run(debug=True)





