select bar as Bar
from Sells
Where price >= ALL(select price from Sells where price is not NULL);

/*

+-----------+
| Bar       |
+-----------+
| Joe's bar |
+-----------+
1 row in set (0.00 sec)

*/
