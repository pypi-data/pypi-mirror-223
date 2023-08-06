# easycloudapi
The `easycloudapi` is a simple uitility to provide ease of developing experience for any Python Applications.


## Functionality Availaible:
1. Generate Date Dimension
2. Generate Bigquery Schema from Json

## Code Samples:

### Generate Bigquery Schema-
1. You can directly pass json/dict object to the `generate_bq_schema` method
    ```python
    from easycloudapi.gcp.bigquery.bigquery_schema import BigquerySchema

    sample_json = {
        "name": "Danilo",
        "age": 32,
        "date_joined": "2020-11-05",
        "location": {"country": "United Kingdom", "city": "London"},
        "years_active": [2020, 2021, 2022],
        "favourite_movies": [
            {"name": "Momento", "year": "2000"},
            {"name": "Se7en", "year": "1995"},
            {"name": "Momento", "year": "2000"}
        ]
    }

    bq_schema_obj = BigquerySchema()
    out_generate_bq_schema = bq_schema_obj.generate_bq_schema(data=sample_json)

    print(f"out_generate_bq_schema:\n{out_generate_bq_schema}")
    ```

2. You can also convert the json file into json/dict object and pass to the `generate_bq_schema` method
    ```python
    import json
    from easycloudapi.gcp.bigquery.bigquery_schema import BigquerySchema


    bq_schema_obj = BigquerySchema()
    with open("tests//test_data//sample_json_01.json") as json_file:
        sample_dict = json.load(json_file)

    out_generate_bq_schema = bq_schema_obj.generate_bq_schema(data=sample_dict)
    print(out_generate_bq_schema)
    ```

### Date Functionality-
1. Generate Date Dimension
    ```python
    from easycloudapi.generic.datetime.generate_date_dimention import generate_date_dimension

    out1 = generate_date_dimension(start_date="2023\\08\\01", end_date="2023\\08\\03")
    print(f"out1: {out1}")
    out2 = generate_date_dimension(start_date="2023/08/01", end_date="2023/08/03")
    print(f"out2: {out2}")
    out3 = generate_date_dimension(start_date="2023-08-01", end_date="2023-08-03")
    print(f"out3: {out3}")
    ```

## How to Contribute
1. Refer to [Developer Guide](developer.md)


