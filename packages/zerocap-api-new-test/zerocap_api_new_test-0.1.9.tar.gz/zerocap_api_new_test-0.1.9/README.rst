# zerocap-api-test 

# <a href="#testapi">Jump restapi</a>
# <a href="#test">Jump websocket</a>



```

描述介绍

sdk install
pip install zerocap-api-test
。
。
。

```



# <a id='testapi' href='https://dma-api.defi.wiki/redoc'>restapi </a>
get https://dma-api.defi.wiki/redoc



#### 1. Create an order
post https://dma-api.defi.wiki/orders/create_order



请求参数:

| Parameter       | required  | data type | describe        | Value range  |
|-----------------|-----------|-----------|-----------------|--------------|
| symbol          | true      | string    | Instrument      | USDT/AUD     |
| side            | true      | string    | Side            | buy sell     |
| type            | true      | string    | Type            | market limit |
| amount          | true      | string    | Quantity        |              |
| price           | true      | string    | Price           |              |
| client_order_id | true      | string    | Client order id |              |
| account_vault   | true      | json      | accountVault    |              |

请求参数：示例（不能直接使用,需要替换自己的参数）

```

{
    "symbol": "USDT/AUD",
    "side": "buy",
    "type": "market",
    "amount": "1000",
    "price": "1000",
    "client_order_id": "e7f80d34-0d80-4256-9de3-cd37310a55da",
    "account_vault": {
        "third_identity_id": "918d7125916c13191f3674e",
        "api_key": "***",
        "signature": "***",
        "note": ""
    }
}

```

响应数据:

| Parameter          | required | data type | describe        | Value range |
|--------------------|----------|-----------|-----------------|-------------|
| id                 | true     | long      | Transaction ID  |             |
| clientOrderId      | true     | string    | Client order id |             |
| datatime           | true     | string    | Time            |             |
| timestamp          | true     | string    | Time            |             |
| lastTradeTimestamp | true     | long      | Time            |             |
| status             | true     | string    | Status          |             |
| type               | true     | string    | Type            |             |
| timeInForce        | true     | string    | timeInForce     |             |
| side               | true     | string    | Side            |             |
| price              | true     | string    | Price           |             |
| average            | true     | string    | average         |             |
| amount             | true     | string    | Quantity        |             |
| filled             | true     | string    | filled          |             |
| remaining          | true     | string    | remaining       |             |
| cost               | true     | string    | cost            |             |
| transferId         | true     | string    | transferId      |             |
| trades             | true     | string    | trades          |             |


响应例子:

```

 {
    "id": "16ef58d1-677e-489c-8fe0-5acc4a680b6e",
    "clientOrderId": "e7f80d34-0d80-4256-9de3-cd37310a55dabe",
    "datatime": "2023-07-28 09:19:45",
    "timestamp": "1690535984000",
    "lastTradeTimestamp": "1690535984000",
    "status": "closed",
    "symbol": "USDT/AUD",
    "type": "Market",
    "timeInForce": "FOK",
    "side": "buy",
    "price": "21.1",
    "average": "1.685133171",
    "amount": "9",
    "filled": "9",
    "remaining": "0",
    "cost": "15.16619854",
    "transferId": "12424971-f51d-4144-a205-9e306eb6351c",
    "trades": [
        {
            "id": "12424971-f51d-4144-a205-9e306eb6351c",
            "timestamp": "1690535984000",
            "datetime": "2023-07-28 09:19:45",
            "symbol": "USDT/AUD",
            "order": "16ef58d1-677e-489c-8fe0-5acc4a680b6e",
            "type": "market",
            "side": "buy",
            "takerOrMaker": "taker",
            "price": "1.685133171",
            "amount": "9",
            "cost": "15.16619854",
            "orderFrom": "coinroutes"
        }
    ]
}

```




#### 2. Fetch specific orders
post https://dma-api.defi.wiki/orders/fetch_order


请求参数:


| Parameter       | required | data type | describe       | Value range  |
|-----------------|----------|-----------|----------------|--------------|
| id              | true     | string    | Transaction ID |              |
| account_vault   | true     | json      | accountVault   |              |

请求参数：示例（不能直接使用,需要替换自己的参数）

```

{
    "id": "16ef58d1-677e-489c-8fe0-5acc4a680b6e",
    "account_vault": {
        "third_identity_id": "918d7125916c13191f3674e",
        "api_key": "***",
        "signature": "***",
        "note": ""
    }
}

```

响应数据 接口报错 待定:


| Parameter     | required | data type | describe       | Value range |
|---------------|----------|-----------|----------------|-------------|
| id            | true     | string    | Transaction ID |             |
| account_vault | true     | json      | accountVault   |             |


响应例子:

```

{
	"id": "5e24b0e6-c5c9-42fa-b998-91eff88cb599",
	"client_order_id": "e7f80d34-0d80-4256-9de3-cd37310234",
	"datatime": "2023-07-31 02:10:45",
	"timestamp": "1690769444000",
	"last_trade_timestamp": "1690769444000",
	"status": "closed",
	"symbol": "USDT/AUD",
	"type": "Market",
	"time_in_force": "FOK",
	"side": "sell",
	"price": "1",
	"average": "1.319611568",
	"amount": "500",
	"filled": "500",
	"remaining": "0",
	"cost": "659.8057838",
	"transfer_id": "cd8f809d-19bb-4014-8814-ec59cdf54136",
	"fee": "",
	"trades": [
		{
			"id": "cd8f809d-19bb-4014-8814-ec59cdf54136",
			"timestamp": "1690769444000",
			"datetime": "2023-07-31 02:10:45",
			"symbol": "USDT/AUD",
			"order": "5e24b0e6-c5c9-42fa-b998-91eff88cb599",
			"type": "market",
			"side": "sell",
			"taker_or_maker": "taker",
			"price": "1.319611568",
			"amount": "500",
			"cost": "659.8057838",
			"order_from": "coinroutes",
			"fee": "",
			"fees": ""
		}
	]
}

```


#### 3. Batch fetch order
post https://dma-api.defi.wiki/orders/fetch_orders



请求参数:

| Parameter      | required | data type | describe        | Value range |
|----------------|----------|-----------|-----------------|-------------|
| symbol         | true     | string    | symbol          |             |
| start_datetime | true     | string    | start_datetime  |             |
| end_datetime   | true     | string    | end_datetime    |             |
| page           | true     | string    | page            |             |
| limit          | true     | string    | limit           |             |
| ids            | true     | string    | Transaction ids |             |
| status         | true     | string    | status          |             |
| sort_order     | true     | string    | sort_order      |             |
| order_type     | true     | string    | order_type      |             |
| side           | true     | string    | side            |             |
| account_vau lt | true     | j son     | accountVault    |             |

请求参数：示例（不能直接使用,需要替换自己的参数）

```

{
    "symbol": "",
    "start_datetime": 0,
    "end_datetime": 0,
    "page": 0,
    "limit": 0,
    "ids": "",
    "status": "",
    "sort_order": "",
    "order_type": "",
    "side": "",
    "account_vault": {
        "third_identity_id": "918d7125916c13191f3674e",
        "api_key": "***",
        "signature": "***",
        "note": ""
    }
}

```

响应数据 接口报错 待定:



| Parameter     | required | data type | describe       | Value range |
|---------------|----------|-----------|----------------|-------------|
| id            | true     | string    | Transaction ID |             |
| account_vault | true     | json      |  accountVault  |             |



响应例子:

```

{
	"order_list": [
		{
			"id": "476b0262-8689-4bc4-b5ff-380bb4ccc5e1",
			"client_order_id": "e7f80d34-0d80-4256-9de3-cd37310a55da",
			"datatime": "2023-07-31 02:12:23",
			"timestamp": "1690516007000",
			"last_trade_timestamp": "1690516007000",
			"status": "rejected",
			"symbol": "USDT/AUD",
			"type": "market",
			"time_in_force": "FOK",
			"side": "buy",
			"price": "1000",
			"average": "",
			"amount": "1000",
			"filled": "",
			"remaining": "",
			"cost": "",
			"transfer_id": "",
			"fee": "",
			"trades": []
		}
	],
	"status": "success",
	"total": 3864,
	"page": "1"
}

```



## <span id='test'>websocket</span>

#### 1. Subscribe to Market data


websocket wss://dma-api.defi.wiki/ws/GetMarket



请求参数:

| Parameter     | required | data type | describe                | Value range |
|---------------|----------|-----------|-------------------------|-------------|
| api_key       | true     | string    | key                     |             |
| signature     | true     | long      | Cryptographic signature |             |
| data_type     | true     | string    | Subscribed Channels     | price       |


请求参数：示例（不能直接使用,需要替换自己的参数）

```

wss://dma-api.defi.wiki/ws/GetMarket?api_key=coinroutes&signature=2585311b823982b325b266e132cd8cdf88d190ca61706dda5a67d421b23005df&data_type=price

```


响应数据:


| Parameter            | required | data type | describe | Value range        |
|----------------------|----------|-----------|----------|--------------------|
| type                 | true     | long      | type     |                    |
| channel              | true     | string    | channel  | dma_price_USDT/AUD |
| data                 | true     | jsonstr   | data     |                    |
| data['sell_price']   | true     | string    | data     | sell price         |
| data['buy_price']    | true     | string    | data     | buy price          |
| data['datetime']     | true     | string    | data     | time               |
| data['timestamp']    | true     | string    | data     | time               |


响应例子:

```

{
    "type": "message",
    "channel": "dma_price_USDT/AUD",
    "data": "{
        \"sell_price\": \"1.322544321902561296\",
        \"buy_price\": \"1.668209315127094362\",
        \"datetime\": \"2023-07-28 10:03:40\",
        \"timestamp\": \"1690538620.1056492\"
        }"
}

```

#### 2.  Subscribe Order updates or transaction records


websocket wss://dma-api.defi.wiki/ws/GetOrdersInfo



请求参数:


| Parameter     | required | data type | describe                | Value range |
|---------------|----------|-----------|-------------------------|-------------|
| api_key       | true     | string    | key                     |             |
| signature     | true     | long      | Cryptographic signature |             |
| data_type     | true     | string    | Subscribed Channels     | order,trade |


请求参数：示例（不能直接使用,需要替换自己的参数）

```

wss://dma-api.defi.wiki/ws/GetOrdersInfo?api_key=coinroutes&signature=2585311b823982b325b266e132cd8cdf88d190ca61706dda5a67d421b23005df&data_type=order,trade

```


dma_order_info 响应数据:


| Parameter             | required   | data type | describe      | Value range                    |
|-----------------------|------------|-----------|---------------|--------------------------------|
| type                  | true       | long      | type          |                                |
| channel               | true       | string    | channel       | dma_order_info dma_trader_info |
| data                  | true       | jsonstr   | data          |                                |
| data['OrderId']       | true       | str       | OrderId       |                                |
| data['ClientOrderId'] | true       | str       | ClientOrderId |                                |
| data['TxnAlias']      | true       | str       | TxnAlias      |                                |
| data['TransferId']    | true       | str       | TransferId    |                                |
| data['Symbol']        | true       | str       | Symbol        |                                |
| data['Type']          | true       | str       | Type          |                                |
| data['TimeInForce']   | true       | str       | TimeInForce   |                                |
| data['Side']          | true       | str       | Side          |                                |
| data['OrderId']       | true       | str       | OrderId       |                                |
| data['Price']         | true       | str       | Price         |                                |
| data['AveragePrice']  | true       | str       | AveragePrice  |                                |
| data['Amount']        | true       | str       | Amount        |                                |
| data['CreatedAt']     | true       | str       | CreatedAt     |                                |
| data['UpdatedAt']     | true       | str       | UpdatedAt     |                                |
| data['AccountId']     | true       | str       | AccountId     |                                |
| data['VaultId']       | true       | str       | VaultId       |                                |
| data['Note']          | true       | str       | Note          |                                |
| data['Status']        | true       | str       | Status        |                                |
| data['Average']       | true       | str       | Average       |                                |
| data['Filled']        | true       | str       | Filled        |                                |
| data['Remaining']     | true       | str       | Remaining     |                                |
| data['Cost']          | true       | str       | Cost          |                                |
| data['ExecPrice']     | true       | str       | ExecPrice     |                                |
| data['OrderFrom']     | true       | str       | OrderFrom     |                                |


响应例子:

```

{
    "type":"message",
    "channel":"dma_order_info",
    "data":"{
        \"OrderId\":\"d8be1f41-9e8e-4af0-899b-c1334916aa0e\",
        \"ClientOrderId\":\"e7f80d34-0d80-4256-9de3-cd37310a55da\",
        \"TxnAlias\":\"\",
        \"TransferId\":\"\",
        \"Symbol\":\"USDT/AUD\",
        \"Type\":\"market\",
        \"TimeInForce\":\"FOK\",
        \"Side\":\"sell\",
        \"Price\":\"1000\",
        \"AveragePrice\":\"\",
        \"Amount\":\"1000\",
        \"CreatedAt\":1690538950000,
        \"UpdatedAt\":1690538950000,
        \"AccountId\":\"1ca36d2b-2103-45c7-a2e3-3b90825ba1b2\",
        \"VaultId\":\"5175\",
        \"Note\":\"yyy_test_create_order\",
        \"Status\":\"open\",
        \"Average\":\"0\",
        \"Filled\":\"0\",
        \"Remaining\":\"1000\",
        \"Cost\":\"1000000\",
        \"ExecPrice\":\"\",
        \"OrderFrom\":\"coinroutes\
    "}"
}

```


