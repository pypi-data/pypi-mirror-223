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
