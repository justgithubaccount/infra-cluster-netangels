API_TOKEN=

curl -XPOST GET 'https://api-ms.netangels.ru/api/v1/sshkeys/' \
    --header "Authorization: Bearer $API_TOKEN"
