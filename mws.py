import microwebsrv

def http_handler(request, response):
    # Handle HTTP requests here
    response.WriteResponseHTML("Hello from your ESP32!")

# Create a micro web server on port 80
srv = microwebsrv.WebServer(port=80, webPath="/www")

# Set the request handler function
srv.SetHttpHandler(http_handler)

# Start the server
srv.Start(threaded=False)