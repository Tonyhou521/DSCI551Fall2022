create view Beers2Bars 
as 
select manf,beer,bar,price 
from Sells inner join Beers 
Where Sells.beer = Beers.name;

/*

create view Beers2Bars
    -> as
    -> select manf,beer,bar,price
    -> from Sells inner join Beers
    -> Where Sells.beer = Beers.name;
Query OK, 0 rows affected (0.01 sec)

+----------------+------------+------------+-------+
| manf           | beer       | bar        | price |
+----------------+------------+------------+-------+
| Anheuser-Busch | Bud        | Bob's bar  |     3 |
| Anheuser-Busch | Bud        | Joe's bar  |     3 |
| Anheuser-Busch | Bud        | Mary's bar |  NULL |
| Anheuser-Busch | Bud Lite   | Joe's bar  |     3 |
| Anheuser-Busch | Bud Lite   | Mary's bar |     3 |
| Heineken       | Budweiser  | Mary's bar |     2 |
| Anheuser-Busch | Michelob   | Joe's bar  |     3 |
| Pete's         | Summerbrew | Bob's bar  |     3 |
| Pete's         | Summerbrew | Joe's bar  |     4 |
+----------------+------------+------------+-------+
9 rows in set (0.00 sec)

*/
