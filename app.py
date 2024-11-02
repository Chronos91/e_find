from flask import Flask, request, jsonify, render_template
import dns.resolver

app = Flask(__name__)

def get_mx_records(domain):
    try:
        mx_records = dns.resolver.resolve(domain, 'MX')
        if not mx_records:
            return f"No MX records found for {domain}."

        mx_list = [mx.exchange.to_text() for mx in mx_records]
        return mx_list
    except dns.resolver.NoAnswer:
        return f"No MX records found for {domain}."
    except dns.resolver.NXDOMAIN:
        return f"The domain {domain} does not exist."
    except Exception as e:
        return f"Error fetching MX records: {e}"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/lookup', methods=['POST'])
def lookup():
    domain = request.form['domain']
    mx_records = get_mx_records(domain)
    return jsonify(mx_records)

if __name__ == '__main__':
    app.run(debug=True)
