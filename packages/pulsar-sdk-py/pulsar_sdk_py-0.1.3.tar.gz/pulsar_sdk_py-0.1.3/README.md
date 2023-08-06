![alt text](https://i.imgur.com/jVdp3yy.png)

<div id="top"></div>

This library serves as a way to interact with Pulsar's Third Party APIs.
Provided you have an API Key, getting started is very easy.

```python
from pulsar_sdk_py import PulsarSDK
API_KEY = "YOUR API KEY HERE"
sdk = PulsarSDK(API_KEY)
```

And then you're set, and you can start doing some things like this:

````python
from pulsar_sdk_py import PulsarSDK
from pulsar_sdk_py.enums import ChainKeys
API_KEY = "YOUR API KEY HERE"
sdk = PulsarSDK(API_KEY)

responses_list = []
async for wallet_balance in sdk.balances.get_wallet_balances(wallet_addr="YOUR WALLET ADDRESS", chain=ChainKeys.YOUR_WALLET_CHAIN):
    responses_list.append(wallet_balance)
````

Which will fetch you all the wallet balances for your wallet, provided the Chain is active in our environment.

For more information, check out our [documentation](http://pulsar.readme.io/).

## Changelog
### v0.1.2/3:
- Changing names of dataclasses to match return from API.
### v0.1.1: 
- Fixed issue where balances and timeseries would come duplicated. 
- Fixed wallet timeseries schema.
### v0.1.0:
- Beta launch.