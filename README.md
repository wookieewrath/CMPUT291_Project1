CMPTU291_Project1

Note 1 (case-insensitive foreign key (and other) violations):
A possible suggestion. We need to take into account the case-insensitive inputs from the user. SELECT statements can use COLLATE NOCASE to retreive data case-insensitively.
When using INSERT (or maybe even UPDATE?), do not use the inputs from the user in the query. If you do, you might get a foreign key violation. Instead, use SELECT to retrieve whatever info is required, and use the fetch'd tuple's values in your INSERT/UPDATE statements. The fetch'd tuple will contain the proper capitalization. I think this is one approach around this problem? I have yet to try it out though.
