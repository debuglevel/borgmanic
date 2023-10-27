# File to write metrics for Telegraf consumption
TELEGRAF_METRICS_FILE = "telegraf_metrics.txt"


# Function to write metrics in InfluxDB line protocol format and to a file
def write_metrics(measurement, tags, fields, time=None):
    # Create data point in line protocol format
    data_point = {
        "measurement": measurement,
        "tags": tags,
        "fields": fields,
    }

    if time:
        data_point["time"] = time

    # Write data point to InfluxDB
    client.write_points([data_point])

    # Write data point to the Telegraf metrics file
    with open(TELEGRAF_METRICS_FILE, "a") as telegraf_file:
        telegraf_line = f"{measurement}"
        for key, value in tags.items():
            telegraf_line += f",{key}={value}"
        for key, value in fields.items():
            telegraf_line += f" {key}={value}"
        if time:
            telegraf_line += f" {time}"
        telegraf_line += "\n"
        telegraf_file.write(telegraf_line)


if __name__ == "__main__":
    # Example usage
    measurement = "myMeasurement"
    tags = {"tag1": "value1", "tag2": "value2"}
    fields = {"fieldKey": "fieldValue"}

    write_metrics(measurement, tags, fields)
