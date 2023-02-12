select drinker 
from Likes
where (beer ='Bud') AND drinker != all(select drinker from Likes where beer = 'Summerbrew');

/*

+----------+
| drinker  |
+----------+
| Bill     |
| Jennifer |
+----------+
2 rows in set (0.00 sec)

*/




