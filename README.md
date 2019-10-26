CMPTU291_Project1


(some) Issues:
    
>>> The get_marriage and get_birth do not currently use the USERS's location as the birth and marriage location.
>>> Errors need to be caught and dealt with properly, specifically if the user enters something stupid. 
    Perhaps we can do this in the main method? Instead of catching errors in every function.
>>> Registry Agent function #6 needs to be completed
>>> Traffic Officer function #2 needs to be completed


NOTE 1 

(case-insensitive foreign key (and other) violations):
A possible suggestion. We need to take into account the case-insensitive inputs from the user. SELECT statements can use COLLATE NOCASE to retreive data case-insensitively.
When using INSERT (or maybe even UPDATE?), do not use the inputs from the user in the query. If you do, you might get a foreign key violation. Instead, use SELECT to retrieve whatever info is required, and use the fetch'd tuple's values in your INSERT/UPDATE statements. The fetch'd tuple will contain the proper capitalization. I think this is one approach around this problem? I have yet to try it out though.     UPDATE: I have tried this and it works. 


Pro-Tip#2:

Since we are often returning tuples with multiple values, when executing an SQL query, remember to include an additional comma at the end. I wasted so much time trying to figure out what was wrong. example (note the comma after regno):

cursor.execute("UPDATE registrations SET expiry=? WHERE regno=?", (next_year, regno,))
                       
                       
                      
