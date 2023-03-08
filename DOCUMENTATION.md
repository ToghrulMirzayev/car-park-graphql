# Documentation

## Base URL
`localhost/graphql`


## Overall description
GraphQL API included both `QUERIES` and `MUTATION` those described below in details

## QUERIES
There are 2 options implemented:

1. If you want to get all cars that in your park, then you can use below query. 
You can fetch the data what you want by including to the request the specific field listed below. 
* `getCars`
  * `carId`
  * `name`
  * `color`
  * `price`

Request sample:
```
query getAllCars {
  getCars {
    name,
    color
  }
}
```

Response sample:
```
{
  "data": {
    "getCars": [
      {
        "color": "Red",
        "name": "Audi A4"
      },
      {
        "color": "Black",
        "name": "Porsche Cayenne"
      },
      {
        "color": "White",
        "name": "Rolls-Royce Cullinan"
      }
    ]
  }
}
```
  
2. If you want to fetch the car by name, then you can use below query by including to the request the specific field listed below. 
Note: This query expects mandatory argument `name` with `string` data type that should be indicated in request
* `getCarByName`
  * `carId`
  * `name`
  * `color`
  * `price`

Request sample:
```
query getSingleCarByName {
  getCarByName(name: "Rolls-Royce Cullinan") {
    carId,
    name,
    color,
    price
  }
}
```

Response sample:
```
{
  "data": {
    "getCarByName": [
      {
        "carId": "3",
        "color": "White",
        "name": "Rolls-Royce Cullinan",
        "price": 340000
      }
    ]
  }
}
```

## MUTATIONS
There are 2 options implemented:

1. If you want to add new car to your park, then you can use below request
* `buyNewCar`
  * Mandatory arguments listed below, ID of new car will be created automatically by incrementing order
    * `name` - data type is `string`
    * `color` - data type is `string`
    * `price` - data type is `float`

Request sample
```
mutation buyFordMustang {
  buyNewCar(name: "Ford Mustang", color: "Grey", price: 35000) {
    carId
  }
}
```

Response sample
```
{
  "data": {
    "buyNewCar": {
      "carId": "4"
    }
  }
}
```

2. If you want to cell old car, then you can use below mutation.
* `cellOldCar`
  * Below argument is mandatory to specify
    * `id` - data type is `scalar`

Request sample
```
mutation cellAudiA4 {
  sellOldCar(carId: 1)
}
```

Response sample
```
{
  "data": {
    "sellOldCar": true
  }
}
```