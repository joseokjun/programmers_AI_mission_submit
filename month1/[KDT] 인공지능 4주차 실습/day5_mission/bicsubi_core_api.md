Flask API
=========

Introduction
------------

This is a Flask API for managing weapons.

Usage
-----

### `/whoami`

Returns the name of the author of this API.

#### GET

##### Response

*   `200 OK` on success

json

```json
{
    "name": "joseokjun"
}
```

### `/echo`

Returns the string value passed as a query parameter.

#### GET

##### Query Parameters

*   `string`: The string value to echo.

##### Response

*   `200 OK` on success

json

```json
{
    "value": "string"
}
```

### `/weapon`

Retrieves the list of weapons.

#### GET

##### Response

*   `200 OK` on success

json

```json
[
    {
        "id": 0,
        "name": "missile",
        "stock": 1000
    }
]
```

#### POST

Adds a new weapon to the list of weapons.

##### Request

json

```json
{
    "id": 1,
    "name": "laser",
    "stock": 500
}
```

##### Response

*   `201 Created` on success

json

```json
{
    "id": 1,
    "name": "laser",
    "stock": 500
}
```

### `/weapon/<int:id>`

Updates, or deletes the specified weapon.

#### PUT

Updates the specified weapon with the provided details.

##### Request

json

```json
{
    "name": "new_weapon_name",
    "stock": 100
}
```

##### Response

*   `200 OK` on success

json

```json
{
    "id": 0,
    "name": "new_weapon_name",
    "stock": 100
}
```

#### DELETE

Deletes the specified weapon.

##### Response

*   `200 OK` on success

json

```json
[
    {
        "id": 1,
        "name": "laser",
        "stock": 500
    }
]
```

Conclusion
----------

This Flask API provides basic CRUD operations for managing weapons.