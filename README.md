# Weather Data Streaming and Storage Pipeline

This project demonstrates a data pipeline that fetches weather information for multiple cities from the OpenWeather API, streams the data into Apache Spark via Apache Kafka, and stores the processed data into AWS S3.

### Project Structure
weather_data_pipeline/  
│  
├── src/  
│   ├── kafka_producer.py         # Script to fetch weather data and produce to Kafka  
│   ├── weather_streaming.py      # Spark streaming script to process and store data  
│  
├── requirements.txt              # Dependencies file  
├── README.md                     # Project documentation  


### Setup Instructions
1. Clone the repository:
   ```bash
   git clone https://github.com/fengdsti/Openweather_pipeline.git
   cd Openweather_pipeline

2. Install dependencies using pip:
   ```bash
   pip install -r requirements.txt

3. Set up your OpenWeather API key and AWS credentials:  

    Obtain an OpenWeather API key from https://openweathermap.org/api  
    Configure your AWS credentials or use an AWS IAM role with appropriate permissions for S3.  

4. Run the Kafka producer script to fetch weather data and produce to Kafka; And run the Spark streaming script to process and store data in S3:
   ```bash
   python src/weather_streaming.py
