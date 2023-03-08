from flask import Flask, request
import graphene

app = Flask(__name__)


class ID(graphene.Scalar):

    """
    Class representing a custom GraphQL scalar type for a unique identifier

    Methods:
    - serialize(value): Return the given value
    - parse_value(value): Return the given value
    - parse_literal(ast): Parse the given GraphQL AST value

    Attributes:
    - None
    """

    @staticmethod
    def serialize(value):
        return value

    @staticmethod
    def parse_value(value):
        return value

    @staticmethod
    def parse_literal(ast):
        return ast.value


class Car(graphene.ObjectType):
    """
    Class representing a car in a car park

    Attributes:
        car_id (ID): The unique identifier for the car
        name (str): The name of the car
        color (str): The color of the car
        price (float): The price of the car
    """
    car_id = graphene.Field(ID, required=True)
    name = graphene.String()
    color = graphene.String()
    price = graphene.Float()

    def __init__(self, car_id, name, color, price):
        self.car_id = car_id
        self.name = name
        self.color = color
        self.price = price


class CarPark(graphene.ObjectType):
    """
    Class representing a car park that contains a list of cars

    Attributes:
        cars (List[Car]): A list of cars in the car park
    """
    cars = graphene.List(Car)

    def __init__(self, cars):
        self.cars = cars

    def find_all_cars(self):
        return self.cars

    def find_car_by_name(self, name):
        matching_cars = []
        for car in self.cars:
            if car.name == name:
                matching_cars.append(car)
        return matching_cars

    def buy_new_car(self, name, color, price):
        car_id = str(len(self.cars) + 1)
        car = Car(car_id=car_id, name=name.lower(), color=color, price=price)
        self.cars.append(car)
        return car

    def sell_old_car(self, car_id):
        for index, car in enumerate(self.cars):
            if car.car_id == car_id:
                self.cars.pop(index)
                return True
        return False


car_park = CarPark(cars=[
    Car(car_id="1", name="Audi A4", color="Red", price=45000.00),
    Car(car_id="2", name="Porsche Cayenne", color="Black", price=75000.00),
    Car(car_id="3", name="Rolls-Royce Cullinan", color="White", price=340000.00),
])


class Query(graphene.ObjectType):
    """
    GraphQL query object representing the available queries for the car park application.

    Queries:
    - get_cars: Returns a list of all cars in the car park
    - get_car_by_name: Returns a list of cars that match the given name
    """
    get_cars = graphene.List(Car)
    get_car_by_name = graphene.List(Car, name=graphene.String(required=True))

    @staticmethod
    def resolve_get_cars(root, info):
        return car_park.find_all_cars()

    @staticmethod
    def resolve_get_car_by_name(root, info, name):
        return car_park.find_car_by_name(name)


class Mutation(graphene.ObjectType):
    """
    A GraphQL mutation object representing the available mutations for the car park application

    Mutations:
    - buy_new_car: Adds a new car to the car park
    - sell_old_car: Removes a car from the car park
    """
    buy_new_car = graphene.Field(Car, name=graphene.String(required=True), color=graphene.String(required=True),
                                 price=graphene.Float(required=True))
    sell_old_car = graphene.Field(graphene.Boolean, car_id=graphene.Argument(ID, required=True))

    @staticmethod
    def resolve_buy_new_car(root, info, name, color, price):
        return car_park.buy_new_car(name, color, price)

    @staticmethod
    def resolve_sell_old_car(root, info, car_id):
        return car_park.sell_old_car(car_id)


schema = graphene.Schema(query=Query, mutation=Mutation)


@app.route("/graphql", methods=["POST"])
def graphql():
    data = request.get_json()
    query = data.get("query")
    result = schema.execute(query)
    return {"data": result.data}


if __name__ == "__main__":
    app.run()
