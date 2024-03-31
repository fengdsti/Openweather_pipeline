from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, IntegerType
from confluent_kafka import Producer
import requests

# Define the list of cities and your OpenWeather API key
API_KEY = "6cc06e4a2fb6c377522e54bb7c4337cc"
cities = ["London", "Paris", "Berlin"]

def fetch_weather_data(api_key, cities):
    base_url = "http://api.openweathermap.org/data/2.5/group"
    city_ids = ",".join(str(city_id) for city_id in cities)
    params = {
        "id": city_ids,
        "appid": api_key,
        "units": "metric"
    }
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Check for any request errors
        weather_data = response.json()['list']
        return weather_data
    except requests.exceptions.RequestException as e:
        print("Error fetching weather data:", e)
        return None

# Initialize SparkSession
spark = SparkSession.builder \
    .appName("WeatherDataStreaming") \
    .getOrCreate()

# Define Kafka parameters
kafka_bootstrap_servers = "localhost:9092"
kafka_topic = "weather_data_topic"

# Define the schema for weather data
schema = StructType([
    StructField("City", StringType(), True),
    StructField("Temperature", DoubleType(), True),
    StructField("Description", StringType(), True),
    StructField("Humidity", IntegerType(), True),
    StructField("Wind Speed", DoubleType(), True)
])

def produce_to_kafka(topic, data):
    producer = Producer({'bootstrap.servers': kafka_bootstrap_servers})
    for city_data in data:
        message = f"{city_data['name']},{city_data['main']['temp']},{city_data['weather'][0]['description']},{city_data['main']['humidity']},{city_data['wind']['speed']}"
        producer.produce(topic, value=message.encode('utf-8'))
    producer.flush()
    print("Messages produced to Kafka topic:", topic)


# Fetch weather data for cities
weather_info = fetch_weather_data(API_KEY, cities)
if weather_info:
    # Produce weather data messages to Kafka
    produce_to_kafka(kafka_topic, weather_info)
else:
    print("Failed to fetch weather data.")

# Create a streaming DataFrame from Kafka
df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", kafka_bootstrap_servers) \
    .option("subscribe", kafka_topic) \
    .load()

# Convert the value column from Kafka into structured data using the defined schema
df = df.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("weather_data")) \
    .select("weather_data.*")

# Define the S3 output path where the data will be stored
s3_output_path = "s3://your-bucket-name/path/to/output/"

# Write the streaming data to S3 in Parquet format
query = df \
    .writeStream \
    .outputMode("append") \
    .format("parquet") \
    .option("path", s3_output_path) \
    .option("checkpointLocation", "checkpoint/location") \
    .start()

# Wait for the stream to terminate
query.awaitTermination()
