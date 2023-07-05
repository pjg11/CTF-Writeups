# SQL challenges

## Introduction
This writeup is for all the challenges under the category of `sql`. All challenges use one database dump, here is how to load it:

1. Download the SQL dump
2. Make sure MySQL or MariaDB is installed on your system
3. Log in to mysql and create a database
    ```
    $ mysql -u root -p
    mysql> CREATE DATABASE [new_database];
    ```
4. Import the database using the following command
    ```bash
    $ mysql -u root -p [new_database] < [sql_dump_name]
    ```
5. Use the database using the following command:
    ```
    mysql> USE [new_database];
    ```

These are the tables within the database:

```
mysql> SHOW TABLES;
+---------------------+
| Tables_in_bodycount |
+---------------------+
| credit_cards        |
| cust_passwd         |
| customers           |
| employee_passwd     |
| employees           |
| loan_types          |
| loans               |
| test                |
+---------------------+
8 rows in set (0.000 sec)
```

Now, on to the challenges! 

## Body Count | 10pts
>One of our employees, Jimmie Castora, kept database backups on his computer. DEADFACE compromised his computer and leaked a portion of the database. Can you figure out how many customers are in the database? We want to get ahead of this and inform our customers of the breach. Submit the flag as `flag{#}`. For example, `flag{12345}`.

```
mysql> SELECT COUNT(cust_id) FROM customers;
+----------------+
| COUNT(cust_id) |
+----------------+
|          10000 |
+----------------+
1 row in set (0.003 sec)
```

Flag: `flag{10000}`

## Keys | 20pts
>One of De Monne’s database engineers is having issues rebuilding the production database. He wants to know the name of one of the foreign keys on the loans database table. Submit one foreign key name as the flag: `flag{foreign-key-name}` (can be ANY foreign key).

This one took a while to get right (as you can see I almost ran out of attempts too).

### Initial Attempt

```
mysql> DESC loans;
+--------------+---------------+------+-----+---------+----------------+
| Field        | Type          | Null | Key | Default | Extra          |
+--------------+---------------+------+-----+---------+----------------+
| loan_id      | smallint(6)   | NO   | PRI | NULL    | auto_increment |
| cust_id      | smallint(6)   | NO   | MUL | NULL    |                |
| employee_id  | smallint(6)   | NO   | MUL | NULL    |                |
| amt          | decimal(10,2) | NO   |     | NULL    |                |
| balance      | decimal(10,2) | NO   |     | NULL    |                |
| interest     | decimal(10,2) | YES  |     | NULL    |                |
| loan_type_id | smallint(6)   | NO   | MUL | NULL    |                |
+--------------+---------------+------+-----+---------+----------------+
7 rows in set (0.001 sec)
```

The initial flags I tried were `flag{cust_id}`, `flag{employee_id}` and `flag{loan_type_id}`. None of them seemed to work. Considering I had only two attempts left, I searched this up on google to see if I was doing something wrong.

### Solution

I found [an article](https://tableplus.com/blog/2018/08/mysql-how-to-see-foreign-key-relationship-of-a-table.html), which led to the correct solution. Modified the query a bit, which returned the following result:

```
mysql> SELECT COLUMN_NAME, CONSTRAINT_NAME, REFERENCED_TABLE_NAME FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE WHERE TABLE_NAME = 'loans';
+--------------+-----------------------+-----------------------+
| COLUMN_NAME  | CONSTRAINT_NAME       | REFERENCED_TABLE_NAME |
+--------------+-----------------------+-----------------------+
| loan_id      | PRIMARY               | NULL                  |
| cust_id      | fk_loans_cust_id      | customers             |
| employee_id  | fk_loans_employee_id  | employees             |
| loan_type_id | fk_loans_loan_type_id | loan_types            |
+--------------+-----------------------+-----------------------+
4 rows in set (0.001 sec)
```

I tried a flag with one of the records from the `CONSTRAINT_NAME` column, and it worked!

Flag: `flag{fk_loans_cust_id}` | `flag{fk_loans_employee_id}` | `flag{fk_loans_loan_type_id}`

## Address Book | 30pts
>It looks like DEADFACE is targeting one of De Monne’s customers. Check out this thread in Ghost Town and submit the customer’s name as the flag: `flag{Jane Doe}`

Here's what the Ghost Town thread mentions:

![](images/sql-article3.png)

So the query should include the following constraints:
- The gender is female
- The city is Vienna

Enter these constraints in the query and you have your answer, as there is only one female from Vienna in the database.

```
mysql> SELECT CONCAT(first_name, " ", last_name) FROM customers WHERE city="Vienna" AND gender="F";
+------------------------------------+
| CONCAT(first_name, " ", last_name) |
+------------------------------------+
| Collen Allsopp                     |
+------------------------------------+
1 row in set (0.008 sec)
```

Flag: `flag{Collen Allsopp}`

## City Lights | 40pts
>De Monne wants to know how many branch offices were included in the database leak. This can be found by figuring out how many unique cities the employees live in. Submit the flag as `flag{#}`.

```
SELECT COUNT(DISTINCT city) FROM employees;
+----------------------+
| COUNT(DISTINCT city) |
+----------------------+
|                  444 |
+----------------------+
1 row in set (0.036 sec)
```

Flag: `flag{444}`

## Boom | 100pts
>DEADFACE actors will be targeting customers they consider low-hanging fruit. Check out Ghost Town and see who they are targeting. Submit the number of target candidates as the flag: `flag{#}`.

Here is what the Ghost Town thread mentions:

![](images/sql-article6-1.png)

The thread leads to [this article](https://www.investopedia.com/terms/b/baby_boomer.asp):

>"Baby boomer" is a term used to describe a person who was born between 1946 and 1964.

This clears the conditions to be added in the WHERE clause. Before typing the query, I checked the data type of the `dob` field:

```
mysql> DESC customers;
+------------+-------------+------+-----+---------+----------------+
| Field      | Type        | Null | Key | Default | Extra          |
+------------+-------------+------+-----+---------+----------------+
| cust_id    | smallint(6) | NO   | PRI | NULL    | auto_increment |
| last_name  | tinytext    | NO   |     | NULL    |                |
| first_name | tinytext    | NO   |     | NULL    |                |
| email      | tinytext    | NO   |     | NULL    |                |
| street     | tinytext    | NO   |     | NULL    |                |
| city       | tinytext    | NO   |     | NULL    |                |
| state      | tinytext    | NO   |     | NULL    |                |
| country    | tinytext    | NO   |     | NULL    |                |
| postal     | tinytext    | NO   |     | NULL    |                |
| gender     | tinytext    | NO   |     | NULL    |                |
| dob        | tinytext    | NO   |     | NULL    |                |
+------------+-------------+------+-----+---------+----------------+
11 rows in set (0.001 sec)
```

As it is a string, I used the SUBSTRING function to extract the year, and converted it to an INT type so that the years can be compared.

```
mysql> SELECT COUNT(dob) FROM customers WHERE CONVERT (SUBSTRING(dob, 7, 4), INT) >= 1946 AND CONVERT(SUBSTRING(dob, 7, 4), INT) <=1964;
+------------+
| COUNT(dob) |
+------------+
|       2809 |
+------------+
1 row in set (0.009 sec)
```

Flag: `flag{2809}`

## El Paso | 250pts
>The regional manager for the El Paso branch of De Monne Financial is afraid his customers might be targeted for further attacks. He would like you to find out the dollar value of all outstanding loan balances issued by employees who live in El Paso. Submit the flag as `flag{$#,###.##}`.

```
mysql> SELECT SUM(balance) FROM loans JOIN employees ON loans.employee_id = employees.employee_id WHERE employees.city = 'El Paso';
+--------------+
| SUM(balance) |
+--------------+
|    877401.00 |
+--------------+
```

Flag: `flag{$877,401.00}`

## All A-Loan | 375pts
>De Monne has reason to believe that DEADFACE will target loans issued by employees in California. It only makes sense that they’ll then target the city with the highest dollar value of loans issued. Which city in California has the most money in outstanding Small Business loans? Submit the city and dollar value as the flag in this format: `flag{City_$#,###.##}`.

```
mysql> SELECT employees.city, SUM(loans.balance) AS outstanding FROM employees JOIN loans ON employees.employee_id = loans.employee_id WHERE loans.loan_type_id = 3 AND employees.state = "CA" GROUP BY employees.city ORDER BY outstanding DESC LIMIT 1;
+---------+-------------+
| city    | outstanding |
+---------+-------------+
| Oakland |    90600.00 |
+---------+-------------+
1 row in set (0.008 sec)
```

- `SUM(loans.balance)` has an alias of "outstanding" to make it easier to reference later in the query.
- The two tables, `employees` and `loans` are joined using the primary and foreign key.
- `loan_type_id` is set to 3 (Small Business loans) and the state is set to California.
- The output is grouped by the cities so the balance is calculated for each city.
- The database is ordered in descending order of balance and limited to 1 entry, showing us the highest amount, and the answer to this challenge!

**Fun fact:** I wasted 4/5 attempts on this challenge as I kept referencing the customers table instead of employees 😬.

Flag: `flag{Oakland_$90,600.00}`
