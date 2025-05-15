import hypermedia.net.*;

PImage img;

int PORT_RX=45682;
int PORT_TX= 45683;
String HOST_IP = "127.0.0.1";     // IP Address of the PC in which this App is running
UDP udp;  // Create UDP object for recieving


final int HISTORY_SECONDS = 30;
final int EXPECTED_UPDATES_PER_SECOND = 10;
Ringbuffer positionHistory = new Ringbuffer(HISTORY_SECONDS * EXPECTED_UPDATES_PER_SECOND);

// magnetic heading
float mag_hdg = 0.0;
float alt = 0.0;

// plane position from xplane
Position plane_pos = new Position(11.46167, 48.76333);

// Coords of map
Position top_left = new Position(48.86667, 11.33333);
Position bottom_right = new Position(48.6, 11.73333);

// X and Y pixels of map
float top_left_x = 25.0;
float top_left_y = 25.0;
float bottom_right_x = 670.0;
float bottom_right_y = 670.0;

//
int msg_counter = 0;


// Translation Helpers
float mapLatToY(float lat) {
  return map(lat, top_left.lat, bottom_right.lat, top_left_y, bottom_right_y); 
}

float mapLonToX(float lon) {
  return map(lon, top_left.lon, bottom_right.lon, top_left_x, bottom_right_x);
}


void setup() { 
  size(695,695);
  stroke(255);
  background(255);
  stroke(128);
  
  img = loadImage("ETSI_ING_MANCHING_MAP.png");

  udp = new UDP(this, PORT_RX, HOST_IP);
  udp.log(false);
  udp.listen(true);

  udp.send("MAP, Startup", HOST_IP, PORT_TX);
  
}


//
void drawHistoryPoint(Position entry) {
  float x = mapLonToX(entry.lon);
  float y = mapLatToY(entry.lat);
  fill(255, 0, 0);
  ellipse(x, y, 5, 5);
}


//
void drawAircraft(float x, float y, float heading) {
  pushMatrix();                      // Transformationen isolieren
  translate(x, y);                   // Ursprung auf Flugzeugposition setzen
  rotate(radians(heading));          // In Flugrichtung drehen (Grad zu Radiant)
  fill(0, 0, 255);                   // Flugzeugsymbol blau ausfüllen
  stroke(0);                         // Schwarzer Rand
  // Einfaches Dreieck als Flugzeug
  beginShape();
  vertex(0, -15);    // Spitze (zeigt nach oben, Flugrichtung)
  vertex(-10, 10);   // linke Ecke
  vertex(10, 10);    // rechte Ecke
  endShape(CLOSE);
  popMatrix();                      // Transformationen zurücksetzen
}


//
void draw()
{
  image(img, 0,0);
  
  
  // Historie zeichnen
  for (Position pos : positionHistory.values()) {
    drawHistoryPoint(pos);
  }

  // Aktuelle Position zeichnen
  drawAircraft(
    mapLonToX(plane_pos.lon),
    mapLatToY(plane_pos.lat),
    mag_hdg
  );

}


// Receive Aircraft Data. Wird automatisch vom UDP Callback aufgerufen
void receive(byte[] data, String HOST_IP, int PORT_RX)
{
 
  String message = new String( data );
  
  println("message: ", message);
 
  String[] message_part = split(message, ",");
  if(message_part.length == 5)
  {
    msg_counter = int(message_part[0]);
    plane_pos.lat = float(message_part[1]);
    plane_pos.lon = float(message_part[2]);
    alt = float(message_part[3]);
    mag_hdg = float(message_part[4]);
  
    println( "MSG#: ", msg_counter, "  lat: ", plane_pos.lat, "  lon: ", plane_pos.lon, "  alt: ", alt, "  mag_hdg: ", mag_hdg);
    
    // Add to History
    positionHistory.push(plane_pos.copy());
  }
  else 
  {
    println("ERROR: message_lenght");
  }
}
