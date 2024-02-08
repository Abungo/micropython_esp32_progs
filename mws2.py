import microwebsrv
# Function to handle HTTP requests
def http_handler(request, response):
    # Specify the file path
    file_path = 'index.html'
    try:
        # Open the file and read its content
        with open(file_path, 'r') as file:
            file_content = file.read()
        # Set the response headers
        response.Headers['Content-Type'] = 'text/plain'
        response.WriteResponse(200, file_content)
    except OSError:
        # Handle file not found or other errors
        response.WriteResponse(404, "File not found")
# Create a micro web server on port 80
srv = microwebsrv.WebServer(port=80)
# Set the request handler function
srv.SetHttpHandler(http_handler)
# Start the server
srv.Start(threaded=False)