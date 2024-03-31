# Weather Data Streaming and Storage Pipeline

This project demonstrates a data pipeline that fetches weather information for multiple cities from the OpenWeather API, streams the data into Apache Spark via Apache Kafka, and stores the processed data into AWS S3.

### Project Structure
- `src/`: Contains the source code files
  - `weather_streaming.py`: Script to fetch weather data and produce to Kafka; Spark streaming script to process and store data
- `requirements.txt`: File listing the project dependencies
- `README.md`: Documentation file (you are currently reading this)

### Setup Instructions
1. Clone the repository:
   ```bash
   git clone https://github.com/fengdsti/Openweather_pipeline.git
   cd Openweather_pipeline
