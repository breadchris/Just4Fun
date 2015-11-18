from vuln import create_app
app = create_app()
app.run(debug=False, host="0.0.0.0", port=80, threaded=True)

