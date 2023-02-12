select bar, count(beer) as Total
from Sells
where price >= 2
group by bar;

/*

+------------+-------+
| bar        | Total |
+------------+-------+
| Bob's bar  |     2 |
| Joe's bar  |     4 |
| Mary's bar |     2 |
+------------+-------+
3 rows in set (0.00 sec)

*/