#  ISS Real-Time Tracking Dashboard

A real-time International Space Station (ISS) tracking system built using:

* Python
* Apache Kafka
* Docker
* WebSockets
* Leaflet Maps
* Plotly 3D Visualization
* Chart.js

The system continuously fetches live ISS telemetry data from a public API, streams it through Kafka, forwards it via WebSockets, and visualizes it in a browser dashboard. The dashboard code is provided in the uploaded HTML file.

---

#  Architecture

```text
ISS API
   │
   ▼
producer.py
   │
   ▼
Kafka Topic (iss_location)
   │
   ▼
bridge.py
(WebSocket Server)
   │
   ▼
index.html
(Browser Dashboard)
```

---

#  Project Structure

```text
project/
│
├── producer.py
├── bridge.py
├── docker-compose.yml
├── index.html
└── README.md
```

---

#  Components

## 1. Producer

**File:** `producer.py`

Responsibilities:

* Fetch live ISS data every 3 seconds
* Extract:

  * Latitude
  * Longitude
  * Altitude
  * Velocity
  * Timestamp
* Publish data to Kafka topic

Data Source:

```text
https://api.wheretheiss.at/v1/satellites/25544
```

Kafka Topic:

```text
iss_location
```

---

## 2. Kafka Broker

**Dockerized Apache Kafka**

Responsibilities:

* Receive ISS telemetry
* Store messages
* Stream messages to consumers

Configured using:

```yaml
docker-compose.yml
```

Services:

* Zookeeper
* Kafka

Port:

```text
9092
```

---

## 3. WebSocket Bridge

**File:** `bridge.py`

Responsibilities:

* Consume messages from Kafka
* Forward messages to connected browsers
* Provide real-time communication

WebSocket Endpoint:

```text
ws://127.0.0.1:8765
```

---

## 4. Frontend Dashboard

**File:** `index.html`

Features:

###  Live World Map

Displays:

* Current ISS position
* User location

Using:

```text
Leaflet.js
```

---

###  Statistics Cards

Displays:

* Distance from user to ISS
* ISS velocity
* ISS altitude
* ISS coordinates
* User coordinates

---

###  XY Projection

Longitude vs Latitude Cartesian trajectory.

---

###  YZ Projection

Latitude vs Altitude trajectory.

---

###  XZ Projection

Longitude vs Altitude trajectory.

---

###  3D ISS Trajectory

Interactive 3D path visualization using:

```text
Plotly.js
```

Supports:

* Rotation
* Zooming
* Panning

---

#  Running Kafka

Start Kafka and Zookeeper:

```bash
docker-compose up -d
```

Verify containers:

```bash
docker ps
```

Expected containers:

```text
zookeeper
kafka
```

---

#  Running the Project

### Step 1

Start Kafka:

```bash
docker-compose up -d
```

---

### Step 2

Run Producer:

```bash
python producer.py
```

Expected output:

```text
 Producer running...
 Sent: {...}
```

---

### Step 3

Run WebSocket Bridge:

```bash
python bridge.py
```

Expected output:

```text
 Bridge running on ws://127.0.0.1:8765
```

---

### Step 4

Open Dashboard

Open:

```text
index.html
```

in a browser.

---

#  Sample Kafka Message

```json
{
  "latitude": 12.34,
  "longitude": 56.78,
  "altitude": 420.5,
  "velocity": 27600.2,
  "timestamp": 1710000000
}
```

---

#  Technologies Used

| Technology | Purpose           |
| ---------- | ----------------- |
| Python     | Backend           |
| Kafka      | Streaming         |
| Docker     | Containerization  |
| WebSockets | Real-time updates |
| Requests   | ISS API access    |
| Leaflet    | Maps              |
| Plotly     | 3D Visualization  |
| Chart.js   | Graphs            |

---

#  Learning Outcomes

This project demonstrates:

* Real-time data pipelines
* Event-driven architecture
* Apache Kafka fundamentals
* Producer–Consumer model
* WebSocket communication
* Live data visualization
* Dockerized deployment
* Geospatial visualization

---

#  Future Enhancements

* Historical data storage
* PostgreSQL integration
* Kafka Streams analytics
* Multiple satellite tracking
* Orbit prediction
* Alert system for ISS overhead passes
* Cloud deployment (AWS/Azure/GCP)
* Mobile-friendly dashboard

---

#  Author

Real-Time ISS Tracking and Visualization System using Kafka, Docker, Python, WebSockets, Leaflet, Plotly, and Chart.js.
