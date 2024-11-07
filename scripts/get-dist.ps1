function Get-Token {
    param (
        [string]$ApiKey,
        [string]$Url
    )

    $body = @{
        API_KEY_NETANGELS = $ApiKey
    }
    
    try {
        $response = Invoke-RestMethod -Uri $Url -Method Post -Body $body -ContentType "application/x-www-form-urlencoded"
        return $response.token
    }
    catch {
        throw "Failed to get the token: $($_.Exception.Response.StatusCode) $($_.Exception.Response.StatusDescription)"
    }
}

function Get-ApiResponse {
    param (
        [string]$Uri,
        [string]$Token
    )

    $headers = @{
        Authorization = "Bearer $Token"
    }

    try {
        $response = Invoke-RestMethod -Uri $Uri -Method Get -Headers $headers
        return $response
    }
    catch {
        throw "Failed to get API response: $($_.Exception.Response.StatusCode) $($_.Exception.Response.StatusDescription)"
    }
}

function Save-ResponseAsJson {
    param (
        [Object]$Response,
        [string]$FilePath
    )

    $Response | ConvertTo-Json | Set-Content -Path $FilePath
}

# main
$ApiKey = ""
$TokenUrl = "https://panel.netangels.ru/api/gateway/token/"
$ApiUrl = "https://api-ms.netangels.ru/api/v1/images/distributions/"
$JsonFilePath = "./json/distributions.json"

$API_TOKEN = Get-Token -ApiKey $ApiKey -Url $TokenUrl
$ApiResponse = Get-ApiResponse -ApiUrl $ApiUrl -Token $API_TOKEN
Save-ResponseAsJson -Response $ApiResponse -FilePath $JsonFilePath
