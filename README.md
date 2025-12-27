# AWS - IoT Integration

## Run MQTT Publisher

```shell
python main.py \
    --endpoint <AWS_IOT_ENDPOINT> \
    --cert <PATH-TO-CERT> \
    --key <PATH-TO-PRIVATE-KEY> \
    --farm_id <FARM-ID> \
    --crop_name <CROP-ID> \
    --humid_low <MIN_HUMIDITY> \
    --humid_high <MAX_HUMIDITY> \
    --temp_low <MIN_TEMPERATURE> \
    --temp_high <MAX_TEMPERATURE>
```
