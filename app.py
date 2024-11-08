from flask import Flask, jsonify
from flask_cors import CORS  # Import CORS
import speedtest
import concurrent.futures

app = Flask(__name__)
# Apply CORS to allow requests from any origin
CORS(app)

@app.route('/api/speedtest', methods=['GET'])
def speed_test():
    st = speedtest.Speedtest()
    # st.get_best_server()
    st.get_servers([])
 # Function to run the download and upload tests concurrently
    def run_speed_tests():
        download_speed = round(st.download() / 1_000_000, 1)
        upload_speed = round(st.upload() / 1_000_000, 1)
        ping = round(st.results.ping, 1)
        return download_speed, upload_speed, ping

    with concurrent.futures.ThreadPoolExecutor() as executor:
        result = executor.submit(run_speed_tests)
        download_speed, upload_speed, ping = result.result()
    # download_speed = round(st.download() / 1_000_000, 1)  # Round to 1 decimal place
    # upload_speed = round(st.upload() / 1_000_000, 1)  # Round to 1 decimal place
    # ping = round(st.results.ping, 1)  # Round ping to 1 decimal place
    return jsonify({
        'download': download_speed,
        'upload': upload_speed,
        'ping': ping
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
