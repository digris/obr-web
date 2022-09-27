# Account

## Authentication

 - [API Doc](https://next.openbroadcast.ch/api/v1/schema/redoc/#tag/authentication)

### Default Login / Session / JWT Token

```
/api/v1/account/login/
```

Response on success:

```json
{
    "ct": "account.user",
    "uid": "E85E25A3",
    ...
    "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

For requesting further resources via browser session subsequent authentication the `sid` cookie sent with the 
login request can/will be used.

For non-session requests use the provided `accessToken`.

#### JWT Token Authentication

Provide the `accessToken` from above in every request header:

```
# Headers
Authorization: Bearer <accessToken>
```


#### Refreshing JWT Token

The provided token has a limited lifetime ("a couple of hours") - see `core/settings/base.py` for configured token 
lifetimes.

To refresh the `accessToken` periodically call the user endpoint:

```
/api/v1/account/users/me/
```

which will (amongst others) include an updated token:

```json
{
    "ct": "account.user",
    "uid": "E85E25A3",
    ...
    "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCK0..."
}
```

### User Details

Expandable details: `settings`, `subscription`, `address`

```
/api/v1/account/users/me/?expand=settings,subscription,address
# or
/api/v1/account/users/me/?expand[]=settings&expand[]=subscription&expand[]=address
```

Full example:

```
# Response Header
Content-Type: application/json
Set-Cookie: Cloud-CDN-Cookie=URLPrefix=aH...; HttpOnly: SameSite=Lax
Vary: Accept
```
```json
{
    "ct": "account.user",
    "uid": "E85E25A3",
    "email": "none@none.no",
    "dateJoined": "2021-12-10T15:46:41.412704+01:00",
    "firstName": "Karl A.",
    "lastName": "Klammer",
    "isStaff": true,
    "isAdmin": true,
    "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "subscription": {
        "ct": "subscription.subscription",
        "uid": "61FAC457",
        "activeUntil": "2023-08-14T23:59:59+02:00",
        "isActive": true,
        "isTrial": false
    },
    "settings": {
        "ct": "account.settings",
        "uid": "44936BA2"
    },
    "address": {
        "ct": "account.address",
        "uid": "B5DED631",
        "line1": "Fooweeg 17",
        "line2": "",
        "postalCode": "45654",
        "city": "Zurich",
        "country": "DZ"
    }
}
```


### "Password-less" Login

See [API Doc](https://next.openbroadcast.ch/api/v1/schema/redoc/#tag/authentication)

#### Auth-code Login

T.B.D.

#### Signed Email Login

T.B.D.