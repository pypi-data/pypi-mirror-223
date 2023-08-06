# Ferhassio Saver

*Arango wrapper for 
https://github.com/ArangoDB-Community/python-arango*


### Install requirements

Run:
```
pip install python-arango
```
### Usage

**Create connection**<br>
arango = FerhassioSaver(hosts, user, password, dbname, collection)

**Create unique index**<br>
arango.create_unique_field(field='field')

**Fetch data**<br>
results = arango.fetch_data(cnt, field)<br>
 *cnt - data limit (optional), field - specify a field if you need to get only a specific value and not the entire document (optional).*

**Fetch by field**<br>
result = arango.fetch_by(by_field, value)<br>
*Fetch data using field and value like (_key, 123456).*

**Load data**<br>
arango.load_data(json_list, chunk_size, on_duplicate)<br>
*Load list of json documents in collection. chunk_size - chunk size for worker. On_duplicate: replace(default), update, ignore*

arango.load_once(doc, overwrite_mode)<br>
*Load one document. Overwrite_mode: update(default), replace*

**Validate**<br>
result = arango.is_valid(doc)<br>
*Return true if document in collection.*

**Delete**<br>
result = arango.delete(doc)<br>
*Delete selected document (in dev).*

**Counter**<br>
result = arango.collection_count()<br>
*Returns documents count in selected collection.*

**Execute**<br>
results = arango.execute(query)<br>
*Execute AQL query.*
