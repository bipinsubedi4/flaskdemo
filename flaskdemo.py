from flask import Flask, render_template, request, redirect, url_for, session
import wikipedia

app = Flask(__name__)
# Set the secret key. Keep this really secret:
app.secret_key = 'IT@JCUA0Zr98j/3yXa R~XHH!jmN]LWX/,?RT'


@app.route('/')
def home():
    """Render the home page."""
    return render_template("home.html")


@app.route('/about')
def about():
    """Render the about page."""
    return render_template("about.html")


@app.route('/search', methods=['POST', 'GET'])
def search():
    """Handle the search form and redirect to results."""
    if request.method == 'POST':
        session['search_term'] = request.form['search']
        return redirect(url_for('results'))
    return render_template("search.html")


@app.route('/results')
def results():
    """Render the search results."""
    search_term = session.get('search_term', '')
    if not search_term:
        return redirect(url_for('home'))
    page = get_page(search_term)
    return render_template("results.html", page=page)


def get_page(search_term):
    """Fetch a Wikipedia page."""
    try:
        page = wikipedia.page(search_term)
    except wikipedia.exceptions.PageError:
        # No such page, return a random one
        page = wikipedia.page(wikipedia.random())
    except wikipedia.exceptions.DisambiguationError:
        # Handle disambiguation by getting the first related page
        page_titles = wikipedia.search(search_term)
        if len(page_titles) > 1 and page_titles[1].lower() != page_titles[0].lower():
            page = wikipedia.page(page_titles[1])
        else:
            page = wikipedia.page(wikipedia.random())
    return page


if __name__ == '__main__':
    app.run(debug=True)
