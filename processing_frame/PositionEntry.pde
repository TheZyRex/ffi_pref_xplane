class Position {
  float lat, lon;
  
  Position(float lat, float lon) {
    this.lat = lat; // Breite
    this.lon = lon; // Länge
  }
  
  Position copy() {
    return new Position(this.lat, this.lon);
  }
}

class Ringbuffer {
  private Position[] buffer;
  private int head = 0;
  private int tail = 0;
  private int count = 0;
  private final int maxSize;

  Ringbuffer(int size) {
    this.maxSize = size;
    this.buffer = new Position[maxSize];
  }

  void push(Position entry) {
    buffer[head] = entry;
    head = (head + 1) % maxSize;
    if(count < maxSize) count++;
    else tail = (tail + 1) % maxSize;
  }

  ArrayList<Position> values() {
    ArrayList<Position> list = new ArrayList<Position>();

    for(int i = 0; i < count; i++) {
      int idx = (tail + i) % maxSize;
      list.add(buffer[idx]);
    }
    return list;
  }
}
