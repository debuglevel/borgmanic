import os
import time

# Define a dictionary to store the tags and fields for the InfluxDB line protocol
metrics_data = {
    "measurement": "create-backup.sh",
    "tags": {
        "host": os.environ.get("HOSTNAME", "unknown")
    },
    "fields": {
        "begin": time.strftime('%Y-%m-%dT%H:%M:%S'),
    }
}


def metrics_begin_fields():
    # Fields
    metrics_data["fields"]["end"] = time.strftime('%Y-%m-%dT%H:%M:%S')
    metrics_data["fields"]["durationSeconds"] = str(int(time.time()))
    metrics_data["fields"]["durationMinutes"] = str(int(time.time() // 60))


def metrics_write(output_file):
    # Unix timestamp in nanoseconds
    timestamp = str(int(time.time() * 1e9))
    metrics_data["timestamp"] = timestamp

    # Convert metrics_data to InfluxDB line protocol format
    influxdb_line = f"{metrics_data['measurement']}"

    # Add tags
    for tag_key, tag_value in metrics_data["tags"].items():
        influxdb_line += f",{tag_key}={tag_value}"

    influxdb_line += " "

    # Add fields
    for field_key, field_value in metrics_data["fields"].items():
        influxdb_line += f"{field_key}={field_value},"

    # Remove the trailing comma and add the timestamp
    influxdb_line = influxdb_line[:-1] + f" {timestamp}"

    # Write the line to the output file
    output_file.write(influxdb_line + "\n")
    output_file.flush()


def metrics_keyvalue(key, value):
    # Do not write null values, as InfluxDB cannot parse them.
    if value is not None and value != "null":
        metrics_data["fields"][key] = value


def metrics_keyvalue_integer(key, value):
    metrics_data["fields"][key] = f"{value}i"


def metrics_keyvalue_string(key, value):
    metrics_data["fields"][key] = f'"{value}"'


def metrics_seperator():
    pass  # No need for a separator in Python

# Usage example
# metrics_set_outputfile("output.txt")
# metrics_begin_fields()
# metrics_keyvalue("someKey", "someValue")
# metrics_write(output_file)
