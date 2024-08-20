from flask import Flask, render_template, request, redirect, url_for
import sqlite3 

app = Flask(__name__, template_folder='templates')

recipes_set = set()
ingredients_set = set()

@app.route("/")
def render_index_page():
    global recipes_set, ingredients_set
    """Function to render the html file."""
    return render_template('index.html', ingredients=ingredients_set, results=recipes_set)

@app.route("/addIngredient", methods=["POST"])
def addIngredient():
    global recipes_set, ingredients_set
    conn = sqlite3.connect(r"C:\Users\CrCra\Documents\python\Proyectos\recipes\app_db\data_recipes.db")
    cursor = conn.cursor()
    if request.method =='POST':
        ingredient = request.form['ingredient']
        ingredients_set.add(ingredient)
        if len(ingredient.strip()) > 2:
            cursor.execute(f"select recipes from INGREDIENTS_TABLE where ingredient like '%{ingredient}%'")
            results = cursor.fetchall()
            tmp_set = set()
            for result in results:
                if result:
                    x = list(result[0][1:-1].strip().split(','))
                    if x:
                        query = x[0].replace("'", "''").replace('"','')
                        cursor.execute(f"select link from RECIPES_TABLE where title like '%{query}%'")
                        link = cursor.fetchall()
                        if link:
                            tmp_set.add((query,link[0]))
                        else:
                            tmp_set.add((query,"No link"))

            if recipes_set:
                recipes_set &= tmp_set  # Mantiene solo las recetas que coinciden con todos los ingredientes
            else:
                recipes_set = tmp_set  # Inicializa con las recetas encontradas
        conn.close()
        return redirect(url_for('render_index_page'))

@app.route("/clearAll", methods=["POST"])
def clear():
    global recipes_set, ingredients_set
    recipes_set.clear()
    ingredients_set.clear()
    return redirect(url_for('render_index_page'))


if __name__ == '__main__':
    app.run(debug=True)