import mysql.connector
import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, url_for
import html


app = Flask(__name__)


# Define the database configuration
# Load environment variables from .env file

load_dotenv()

# Get database configuration from environment variables
db_config = {
    "host": os.getenv("VIDEOS_DB_HOST"),
    "user": os.getenv("VIDEOS_DB_USER"),
    "password": os.getenv("VIDEOS_DB_PASSWORD"),
    "database": os.getenv("VIDEOS_DB_DATABASE"),
}

@app.route('/', methods=['GET', 'POST'])
def videos():
    search_term = request.form.get('search_term', '')

    try:
        # Connect to the database
        conn = mysql.connector.connect(**db_config)

        # Create a cursor object to interact with the database
        cursor = conn.cursor()

        if request.method == 'POST':
            # Execute a query to select specific columns and filter by the search term
            query = "SELECT name, url FROM videos WHERE name LIKE %s OR url LIKE %s"
            search_term = '%' + search_term + '%'
            cursor.execute(query, (search_term, search_term))
        else:
            # If no search term provided, fetch all data
            query = "SELECT name, url FROM videos"
            cursor.execute(query)


        # Fetch all the rows from the result set
        rows = cursor.fetchall()

        # Generate HTML table rows for the search results
        rows_html = []
        for row in rows:
            name = html.escape(row[0])
            url = html.escape(row[1])
            copy_text = f"{name} {url}"
            row_html = (
                f"<tr><td>{name}</td><td><a href='{url}'>{url}</a></td>"
                f"<td><button class='copy-button' data-copy-text='{copy_text}'>Copy</button></td></tr>"
            )
            rows_html.append(row_html)

        # Close the cursor and connection
        cursor.close()
        conn.close()

        # Return the HTML table rows as a string
        if request.method == 'POST':
            return ''.join(rows_html)
        else:
            # Render the full HTML template for initial page load
            return render_template('videos.html', search_term=search_term)

    except mysql.connector.Error as err:
        return f"Error: {err}"

if __name__ == '__main__':
    app.run()