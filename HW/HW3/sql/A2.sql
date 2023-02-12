select distinct first_name, last_name
from employees as E inner join salaries as S
where E.emp_no = S.emp_no and S.salary >= 150000;

/*
+------------+-----------+
| first_name | last_name |
+------------+-----------+
| Tokuyasu   | Pesch     |
| Tokuyasu   | Pesch     |
| Tokuyasu   | Pesch     |
| Tokuyasu   | Pesch     |
| Tokuyasu   | Pesch     |
| Ibibia     | Junet     |
| Xiahua     | Whitcomb  |
| Xiahua     | Whitcomb  |
| Lansing    | Kambil    |
| Willard    | Baca      |
| Willard    | Baca      |
| Tsutomu    | Alameldin |
| Tsutomu    | Alameldin |
| Tsutomu    | Alameldin |
| Tsutomu    | Alameldin |
| Tsutomu    | Alameldin |
| Charmane   | Griswold  |
| Charmane   | Griswold  |
| Weicheng   | Hatcliff  |
| Weicheng   | Hatcliff  |
| Mitsuyuki  | Stanfel   |
| Sanjai     | Luders    |
| Sanjai     | Luders    |
| Sanjai     | Luders    |
| Honesty    | Mukaidono |
| Honesty    | Mukaidono |
| Honesty    | Mukaidono |
| Weijing    | Chenoweth |
| Weijing    | Chenoweth |
| Shin       | Birdsall  |
| Shin       | Birdsall  |
| Mohammed   | Moehrke   |
| Lidong     | Meriste   |
| Lidong     | Meriste   |
| Lidong     | Meriste   |
| Lidong     | Meriste   |
+------------+-----------+
36 rows in set (1.51 sec)

*/

