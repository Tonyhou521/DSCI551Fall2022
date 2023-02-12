select dept_no
from dept_manager
group by dept_no
having count(emp_no) >= 3;

/*

+---------+
| dept_no |
+---------+
| d004    |
| d006    |
| d009    |
+---------+
3 rows in set (0.00 sec)

*/
