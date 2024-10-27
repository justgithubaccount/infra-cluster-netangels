API_KEY=

curl -XPOST https://panel.netangels.ru/api/gateway/token/ \
    -d 'api_key='$API_KEY'' > ./token-na.txt