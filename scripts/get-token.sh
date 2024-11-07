API_KEY_NETANGELS=

curl -XPOST https://panel.netangels.ru/api/gateway/token/ \
    -d 'API_KEY_NETANGELS='$API_KEY_NETANGELS'' > ./token-na.txt