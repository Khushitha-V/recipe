
from flask import Flask, redirect, render_template, request, url_for
import mysql.connector

# Connect to the MySQL database
mydb = mysql.connector.connect(
    host="khushitha29112004.mysql.pythonanywhere-services.com",
    user="khushitha2911200",
    password="12345678@k",
    database="khushitha2911200$users"
)
mycursor = mydb.cursor()

# Initialize Flask app
app = Flask(__name__)

@app.route('/')
def index():
    # Retrieve all recipes from the database
    mycursor.execute("SELECT * FROM recipes")
    recipes = mycursor.fetchall()
    return render_template('index.html', recipes=recipes)

@app.route('/add', methods=['GET', 'POST'])
def add_recipe():
    if request.method == "POST":
        recipe_name = request.form['name']
        ingredients = request.form['ingredients']
        instructions = request.form['instructions']
        # Insert the new recipe into the database
        sql = "INSERT INTO recipes (name, ingredients, instructions) VALUES (%s, %s, %s)"
        val = (recipe_name, ingredients, instructions)
        mycursor.execute(sql, val)
        mydb.commit()
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/delete/<int:id>')
def delete_recipe(id):
    # Delete the recipe from the database
    sql = "DELETE FROM recipes WHERE id = %s"
    val = (id,)
    mycursor.execute(sql, val)
    mydb.commit()
    return redirect(url_for('index'))

@app.route('/search', methods=['GET', 'POST'])
def search_recipe():
    if request.method == 'POST':
        query = request.form['query']
        # Search for recipes in the database
        sql = "SELECT * FROM recipes WHERE name LIKE %s"
        val = ('%' + query + '%',)
        mycursor.execute(sql, val)
        results = mycursor.fetchall()
        return render_template('search.html', recipes=results, query=query)
    return render_template('search.html')

if __name__ == '__main__':
    app.run(debug=True)

