import boto3


def lambda_handler(event, context):
    cloudwatch = boto3.client("cloudwatch")

    farm_id = event["farm_id"]
    crop_id = event["crop_id"]
    humidity = event["humidity"]
    temperature = event["temperature"]

    cloudwatch.put_metric_data(
        Namespace="SmartFarm",
        MetricData=[
            {
                "MetricName": "Humidity",
                "Dimensions": [
                    {"Name": "Farm ID", "Value": farm_id},
                    {"Name": "Crop ID", "Value": crop_id},
                ],
                "Unit": "Percent",
                "Value": float(humidity),
            },
            {
                "MetricName": "Temperature",
                "Dimensions": [
                    {"Name": "Farm ID", "Value": farm_id},
                    {"Name": "Crop ID", "Value": crop_id},
                ],
                "Unit": "None",
                "Value": float(temperature),
            },
        ],
    )

    return {"statusCode": 200, "body": f"{farm_id}/{crop_id}: Metric published."}
