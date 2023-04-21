from flask.views import MethodView
from flask import Flask, render_template, request, jsonify
import psycopg2
from query.query import generate_query, filter_results

app = Flask(__name__)

# Define your database connection parameters
db_params = {
    'database': "5400_h1b",
    'user': "postgres",
    'password': "123",
    'host': "localhost",
    'port': '5432'
}

conn = psycopg2.connect(**db_params)
cur = conn.cursor()

class Homepage(MethodView):
    results = None
    def get(self):
        return render_template('index.html', results = self.results)

    def post(self):
        search_term = request.form.get('search_term')
        case_status = request.form.get('case_status')
        decision_date = request.form.get('decision_date')
        wage_rate_of_pay_from = request.form.get('wage_rate_of_pay_from')
        h_1b_dependent = request.form.get('h_1b_dependent')
        full_time_position = request.form.get('full_time_position')
        query = generate_query(search_term, case_status, decision_date, wage_rate_of_pay_from, h_1b_dependent, full_time_position)
        
        # Execute the query and fetch the results
        cur.execute(query)
        results = cur.fetchall()
        if case_status or decision_date or wage_rate_of_pay_from or h_1b_dependent or full_time_position:
            results = filter_results(results, case_status, decision_date, wage_rate_of_pay_from, h_1b_dependent, full_time_position)
        return render_template('index.html', results=results)


app.add_url_rule('/', view_func=Homepage.as_view('home_page'), methods=['GET', 'POST'])

if __name__ == '__main__':
    app.run(debug=True)

cur.close()
conn.close()