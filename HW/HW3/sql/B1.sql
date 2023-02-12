select manf as Manufacturer
from Beers
group by manf
having count(name) >= 3;

/*

+----------------+
| Manufacturer   |
+----------------+
| Anheuser-Busch |
+----------------+
1 row in set (0.00 sec)

*/
