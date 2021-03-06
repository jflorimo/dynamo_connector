# django_dynamo_connector
Explore posibilities to use dynamodb with django

## SETUP PROJECT
just run : 
```./manage.sh run```

## How to

## 1. models

To use a django model with Dynamodb your model must inherit from ```DynamoCompatibleModel``` 
and you must set ```table_name```, ```partition_key```, ```sort_key``` and ```dynamo = Connector()``` attributes to your model.

To facilitate the use of django viewset we needed to add two method to the model_class

```__from_dynamo__(self, data_dict)```
Used to transform result from dynamodb to django model instances.
Some datatypes like DateTimeField are not available in dynamodb (see /src/dynamodb/constants.py for conversion)

```__convert_id_to_dynamo_key_list__(self, django_id)```
Used to get partion/sort keys/values from a django model instance

example:
```python
class Booking(DynamoCompatibleModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_at = models.DateTimeField(default=datetime.now)
    
    # dynamo db
    partition_key = "user"
    sort_key = "date_at"
    table_name = "BookingUserByDateAt"
    dynamo = Connector()
    
    def __from_dynamo__(self, data_dict):
      ...
      
    def __convert_id_to_dynamo_key_list__(self, django_id):
      ...
    
```

## 2. queries
To query dynamodb database you must use the *Connector* object qttribute of your Django model class

example:
```python
Booking.dynamo.create_table()
Booking.dynamo.select(key_tuple_list) # with key_tuple_list = [(key, value), ]
Booking.dynamo.get(key_tuple_list) # with key_tuple_list = [(parition_key, value), (sort_key, value)]
Booking.dynamo.all()
Booking.dynamo.insert(instance) # with instance = Django model instance
Booking.dynamo.update(instance) # with instance = Django model instance
Booking.dynamo.delete(key_tuple_list) # with key_tuple_list = [(parition_key, value), (sort_key, value)]
```

## 3. viewsets.ModelViewSet

if you want to use ModelViewset with the *Connector* you just need to inherit ```DynamoViewset``` and add the attribute ```model_class```

example:
```python
class DynamoBooking(DynamoViewset):
    queryset = None
    model_class = Booking  # needed to use DynamoViewset
    serializer_class = BookingSerializer
    permission_classes = []
```

## 4. urls to test dynamo Connector
```python
"api/dynamo/booking/" # RETRIEVE_LIST, UPDATE
"api/dynamo/booking/<int:pk>/" # RETRIEVE_GET, PUT, PATCH, DELETE
```

## tips
run django cmd: ```./manage.sh run makemigrations```

display django logs: ```./manage.sh logs --tail=100 django```

run black: ```./manage.sh fmt```


