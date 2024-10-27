API_TOKEN=""

curl --request GET "https://api-ms.netangels.ru/api/v1/images/distributions/" \
    --header "Authorization: Bearer $API_TOKEN" > dist.json
