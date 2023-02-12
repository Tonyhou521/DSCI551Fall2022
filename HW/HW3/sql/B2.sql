select name
from Drinkers
where name not in (select drinker from Frequents where drinker is Not NULL);

/*

Empty set (0.00 sec)

*/
