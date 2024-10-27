API_TOKEN=""

curl --request POST 'https://api-ms.netangels.ru/api/v1/cloud/vms/' \
    --header "Authorization: Bearer $API_TOKEN" \
    --header "Content-Type: application/json" \
    --data '{
        "tariff": "start_1",
        "disk_size": 10,
        "image": "img_debian-bookworm",
        "is_backup_enabled": false
    }'
