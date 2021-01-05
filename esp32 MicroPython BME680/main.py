# Complete project details at https://RandomNerdTutorials.com/micropython-bme680-esp32-esp8266/

def web_page():
  bme = BME680_I2C(i2c=i2c)
  
  html = """<html><head><title>ESP with BME680</title>
  <meta http-equiv="refresh" content="10">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="icon" href="data:,"><style>body { text-align: center; font-family: "Trebuchet MS", Arial;}
  table { border-collapse: collapse; margin-left:auto; margin-right:auto; }
  th { padding: 12px; background-color: #0043af; color: white; }
  tr { border: 1px solid #ddd; padding: 12px; }
  tr:hover { background-color: #bcbcbc; }
  td { border: none; padding: 12px; }
  .sensor { color:white; font-weight: bold; background-color: #bcbcbc; padding: 1px;
  </style></head><body><h1>KI6EPW/AB6OR Environment Sensor</h1>
  </style></head><body><h1>ESP with BME680</h1>
  <table><tr><th>MEASUREMENT</th><th>VALUE</th></tr>  
  <tr><td>Temp. Fahrenheit</td><td><span class="sensor">""" + str(round(((bme.temperature) * (9/5) + 32), 1))  + """ &degF</span></td></tr>
  <tr><td>Pressure</td><td><span class="sensor">""" + str(round(bme.pressure, 1)) + """ hPa</span></td></tr>
  <tr><td>Humidity</td><td><span class="sensor">""" + str(int((round(bme.humidity, 0)))) + """ %</span></td></tr>
  <tr><td>Gas</td><td><span class="sensor">""" + str(round(bme.gas/1000, 1)) + """ kOhms</span></td></tr>
  <tr><td>Air Quality</td><td><span class="sensor">""" + str(bme.iqa()) + """</span></td></tr></body></html>"""
  
  return html

  #<tr><td>Temp. Celsius</td><td><span class="sensor">""" + str(round(bme.temperature, 1)) + """ &degC</span></td></tr>
  #<tr><td>Humidity Score</td><td><span class="sensor">""" + str(round(bme.humidity_score(bme.humidity), 1)) + """</span></td></tr>
  #<tr><td>Gas Score</td><td><span class="sensor">""" + str(round(bme.gas_score(bme.gas), 1)) + """</span></td></tr>

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 8002))
s.listen(5)

while True:
  try:
    if gc.mem_free() < 102000:
      gc.collect()
    conn, addr = s.accept()
    conn.settimeout(3.0)
    print('Got a connection from %s' % str(addr))
    request = conn.recv(1024)
    conn.settimeout(None)
    request = str(request)
    print('Content = %s' % request)
    response = web_page()
    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: text/html\n')
    conn.send('Connection: close\n\n')
    conn.sendall(response)
    conn.close()
  except OSError as e:
    conn.close()
    print('Connection closed')