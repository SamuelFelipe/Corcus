# Corvus

Corvus is a payroll software automation, to improve SMEs efficiency,
for accountants looking to automate and control their services and
companies that need to automate their payroll processes.
Start keeping your company's accounting in a centralized (on your phone)
and simplified way (move and see the data you need in one click).

## Your business data in one place

While in the technology epicenter regions in the globe, new services
have reached the point of competing in producing higher and higher
percentages of efficiency over maximum percentages. In Latin America,
although it is not the goal to even make agriculture an automated and
robotized affair. It is obvious that even basic computational issues
such as data control, payroll or cash flow have not yet been implemented,
although they are necessary to improve the production of both companies
and society in general.

## Usage

If (<CORVUS_ENV> == test) the database will be erased at the end of the session
to avoid it remove the variable

console:

```
$ CORVUS_ENV=test CORVUS_MYSQL_USER=corvus_test CORVUS_MYSQL_PWD=c0rvus CORVUS_MYSQL_HOST=localhost CORVUS_MYSQL_DB=corvus_test_db ./console.py
```

Flask api server:

```
$ CORVUS_ENV=test CORVUS_MYSQL_USER=corvus_test CORVUS_MYSQL_PWD=c0rvus CORVUS_MYSQL_HOST=localhost CORVUS_MYSQL_DB=corvus_test_db python3 -m api.app
```

Flask web server:

```
$ CORVUS_ENV=test CORVUS_MYSQL_USER=corvus_test CORVUS_MYSQL_PWD=c0rvus CORVUS_MYSQL_HOST=localhost CORVUS_MYSQL_DB=corvus_test_db python3 -m web.app
```
