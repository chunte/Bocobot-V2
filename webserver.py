import os
import time
import microcontroller
import wifi
import socketpool
from adafruit_httpserver.server import HTTPServer
from adafruit_httpserver.request import HTTPRequest
from adafruit_httpserver.response import HTTPResponse
from adafruit_httpserver.methods import HTTPMethod
from adafruit_httpserver.mime_type import MIMEType

# Variables
selected_mode = None  # Keeps track of the selected mode
server = None  # HTTP server instance

# Initialize WiFi and server
def init():
    global server, selected_mode
    print("Connecting to WiFi...")
    wifi.radio.connect(os.getenv('CIRCUITPY_WIFI_SSID'), os.getenv('CIRCUITPY_WIFI_PASSWORD'))
    print("Connected to WiFi")

    pool = socketpool.SocketPool(wifi.radio)
    server = HTTPServer(pool, "/static")  # Initialize the server

    # Define routes inside init after server initialization
    @server.route("/")
    def mode_selector(request: HTTPRequest):
        global selected_mode
        selected_mode = None  # Reset mode when returning to the selector
        with HTTPResponse(request, content_type=MIMEType.TYPE_HTML) as response:
            response.send(mode_selector_page())

    @server.route("/basic_movement")
    def basic_movement_mode(request: HTTPRequest):
        global selected_mode
        selected_mode = "basic_movement"
        with HTTPResponse(request, content_type=MIMEType.TYPE_HTML) as response:
            response.send(mode_operation_page("Basic Movement"))

    @server.route("/obstacle_avoidance")
    def obstacle_avoidance_mode(request: HTTPRequest):
        global selected_mode
        selected_mode = "obstacle_avoidance"
        with HTTPResponse(request, content_type=MIMEType.TYPE_HTML) as response:
            response.send(mode_operation_page("Obstacle Avoidance"))

    @server.route("/line_following")
    def line_following_mode(request: HTTPRequest):
        global selected_mode
        selected_mode = "line_following"
        with HTTPResponse(request, content_type=MIMEType.TYPE_HTML) as response:
            response.send(mode_operation_page("Line Following"))

    @server.route("/light_searching")
    def light_searching_mode(request: HTTPRequest):
        global selected_mode
        selected_mode = "light_searching"
        with HTTPResponse(request, content_type=MIMEType.TYPE_HTML) as response:
            response.send(mode_operation_page("Light Searching"))

    @server.route("/remote_control")
    def remote_control_mode(request: HTTPRequest):
        global selected_mode        
        selected_mode = "remote_control"
        with HTTPResponse(request, content_type=MIMEType.TYPE_HTML) as response:
            response.send(remote_control_page())
        
#  if a button is pressed on the site
    @server.route("/remote_control", method=HTTPMethod.POST)
    def remote_control_buttonpress(request: HTTPRequest):
        if selected_mode == "remote_control":
            #  get the raw text
            raw_text = request.raw_request.decode("utf8")
            #print(f"Rawtext: {raw_text}")
            
            try:
                # Extract the body of the POST request
                body = raw_text.split("\r\n\r\n", 1)[-1]  # Separate headers and body
                # Look for the pattern "remotebutton="
                if "remotebutton=" in body:
                    command = body.split("remotebutton=")[-1].split('&')[0]  # Extract value
                    #print(f"Extracted Command: {command}")

                    # Handle the command
                    from remote_control import handle_command
                    handle_command(command)
                else:
                    print("No valid remotebutton command found.")
            except Exception as e:
                print(f"Error processing command: {e}")
    
            from remote_control import handle_command
            handle_command(command)
            #  reload site
            with HTTPResponse(request, content_type=MIMEType.TYPE_HTML) as response:
                response.send(remote_control_page())
            

    # Start the server
    print("Starting server...")
    
    try:
        server.start(str(wifi.radio.ipv4_address))
        print(f"Server running at: http://{wifi.radio.ipv4_address}")
        
    #  if the server fails to begin, restart the pico w
    except OSError as e:
        if e.errno == 112:  # Address in use
            print("Server address in use. Restarting...")
            microcontroller.reset()

def get_selected_mode():
    """Returns the currently selected mode."""
    return selected_mode

def poll():
    """Poll the HTTP server to handle requests."""
    if server:
        server.poll()

# HTML Templates (Unchanged)
def mode_selector_page():
    #print("mode_selector_page")
    """HTML for the mode selection screen."""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Mode Selector</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                margin: 0;
                height: 100vh;
                font-family: Arial, sans-serif;
                background-color: #f0f0f0;
            }
            h1 {
                text-align: center;
                font-size: 2em;
                margin-bottom: 20px;
            }
            .menu {
                display: block;
                width: 80%;
                max-width: 300px;
                font-size: 1.5em;
                padding: 15px;
                margin: 10px auto;
                text-align: center;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 10px;
                cursor: pointer;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                transition: transform 0.2s ease;
            }
            .menu:hover {
                transform: scale(1.05);
            }
            .menu:active {
                transform: scale(0.95);
            }
        </style>
    </head>
    <body>
        <h1>Select a Mode</h1>
        <center>
        <button class="menu" onclick="navigate('basic_movement')">Basic Movement</button>
        <div></div>
        <button class="menu" onclick="navigate('obstacle_avoidance')">Obstacle Avoidance</button>
        <div></div>
        <button class="menu" onclick="navigate('line_following')">Line Following</button>
        <div></div>
        <button class="menu" onclick="navigate('light_searching')">Light Searching</button>
        <div></div>
        <button class="menu" onclick="navigate('remote_control')">Remote Control</button>
        <div></div>
        <script>
            function navigate(mode) {
                window.location.href = "/" + mode;
            }
        </script>
    </body>
    </html>
    """

def mode_operation_page(mode):
    #print("mode_operation_page")
    print(mode)
    """HTML for the mode operation screen."""
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{mode} Mode</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {{
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                margin: 0;
                height: 100vh;
                font-family: Arial, sans-serif;
                background-color: #f0f0f0;
            }}
            h1 {{
                text-align: center;
                font-size: 2em;
                margin-bottom: 20px;
            }}
            .button {{
                display: block;
                width: 80%;
                max-width: 300px;
                font-size: 1.5em;
                padding: 15px;
                margin: 10px auto;
                text-align: center;
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 10px;
                cursor: pointer;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                transition: transform 0.2s ease;
            }}
            .button:hover {{
                transform: scale(1.05);
            }}
            .button:active {{
                transform: scale(0.95);
            }}
        </style>
    </head>
    <body>
        <h1>{mode} Mode</h1>
        <button class="button" onclick="navigateBack()">Back</button>
        <script>
            function navigateBack() {{
                window.location.href = "/";
            }}
        </script> 
    </body>
    </html>
    """

def remote_control_page():
    """HTML for the Remote Control Mode page."""
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta http-equiv="Content-type" content="text/html;charset=utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <script>
    function buttonDown(button) {{
        // Send a POST request to tell the Pico that the button was pressed
        var xhttp = new XMLHttpRequest();
        xhttp.open("POST", "/remote_control", true);
        xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        xhttp.send("remotebutton=" + button);
    }}
    function buttonUp() {{
        // Send a POST request to tell the Pico that the button was released (stop)
        var xhttp = new XMLHttpRequest();
        xhttp.open("POST", "/remote_control", true);
        xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        xhttp.send("remotebutton=stop");
    }}
    </script>
    <style>
      h1 {{
        text-align: center;
         }}
      body {{
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
          height: 80vh;
          margin: 0;
        }}
        .controls {{
          display: grid;
          grid-template-columns: repeat(3, 1fr);
          gap: 10px;
        }}
        .button {{
          font-size: 90px;
          display: flex;
          align-items: center;
          justify-content: center;
          //border: 2px solid black;
          //border-radius: 10px;
          background: white;
          padding: 10px;
          user-select: none;
          width: 80px;
          height: 80px;
        }}
        .button:hover {{
            transform: scale(1.05);
        }}
        .button:active {{
            transform: scale(0.95);
        }}
        .backbutton {{
            display: block;
            width: 80%;
            max-width: 300px;
            font-size: 1.5em;
            padding: 15px;
            margin: 10px auto;
            text-align: center;
            background-color: #2196F3;
            color: white;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            transition: transform 0.2s ease;
        }}
        .backbutton:hover {{
            transform: scale(1.05);
        }}
        .backbutton:active {{
            transform: scale(0.95);
        }}
        
    </style>

    </head>
    <body>
    <h1>Wifi Remote Control Car</h1>
    <center><b>
    <div class="controls">
        <div></div>
        <div class="button" id="forward" ontouchstart="buttonDown(this.id)" ontouchend="buttonUp()" 
        onmousedown="buttonDown(this.id)" onmouseup="buttonUp()">⬆️</div>
        <div></div>
        
        <div class="button" id="left" ontouchstart="buttonDown(this.id)" ontouchend="buttonUp()" 
        onmousedown="buttonDown(this.id)" onmouseup="buttonUp()">⬅️</div>
        <div></div>
        <div class="button" id="right" ontouchstart="buttonDown(this.id)" ontouchend="buttonUp()" 
        onmousedown="buttonDown(this.id)" onmouseup="buttonUp()">➡️</div>
        
        <div></div>
        <div class="button" id="backward" ontouchstart="buttonDown(this.id)" ontouchend="buttonUp()" 
        onmousedown="buttonDown(this.id)" onmouseup="buttonUp()">⬇️</div>
        <div></div>
    </div>
    <div><br/></div>
    <button class="backbutton" onclick="window.location.href='/'">Back</button>
    </body></html>
    """
    
    return html
