# Query your weather data using SQL
query = """
    SELECT *
    FROM weather
    WHERE time >= now() - INTERVAL '1 hour'
"""
result = collector.client.query(query=query, database=collector.database)
print(result.to_pandas())