
## Logs Analysis Project

### About
An internal reporting tool that will use information from the database to discover what kind of articles the site's readers like.

The database contains newspaper articles, as well as the web server log for the site. The log has a database row for each time a reader loaded a web page. Using that information, the code will answer questions about the site's user activity.

The program you write in this project will run from the command line. It won't take any input from the user. Instead, it will connect to that database, use SQL queries to analyze the log data, and print out the answers to some questions.

### Setups
To use this project install VirtualBox, Vagrant, Python3, pep8
Following steps were followed during the initial setup:

1. Install VirtualBox
  - VirtualBox is the software that actually runs the virtual machine.You can download it from virtualbox.org, here.
2. Install Vagrant
  - Vagrant is the software that configures the VM and lets you share files between the host computer and the VM's filesystem. Download it from vagrantup.com.
3. Download the VM configuration
  - Download and unzip this file: [FSND-Virtual-Machine.zip](https://d17h27t6h515a5.cloudfront.net/topher/2017/June/5948287e_fsnd-virtual-machine/fsnd-virtual-machine.zip) This will give you a directory called FSND-Virtual-Machine.
4. Change to this directory in the terminal with cd. Inside, you will find another directory called vagrant. Change directory to the vagrant directory:
  ```
  $ cd vagrant/
  ```
- Start the Virtual Machine

  ```
  $ vagrant up
  ```
  This will cause Vagrant to download the Linux operating system and install it.
  ```
  $ vagrant ssh
  ```
  run vagrant ssh to log in to the newly installed Linux VM.

5. Download the data [here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip). The file inside the zip is called newsdata.sql. Put this file into the vagrant directory, which is shared with the virtual machine.

To load the data, use the command
```
psql -d news -f newsdata.sql.
```

6. Connect to the database using the following command
```
psql -d news
```

Execute the Views listed in next Section.

7. Execute the following command to run the log Analysis queries.

```
python3 newsdb.py
```

 Log analysis example of program's output can be seen in the plain text file at [query_result.txt](vagrant/query_result.txt).

### View Definitions

create view popular_articles as
  select title, count(*) as popularity
  from articles join log
  on log.path LIKE '%' || articles.slug
  group by title
  order by popularity desc;

create view popular_article_authors as
  select author, count(*) as popularity
  from articles join log
  on log.path LIKE '%' || articles.slug
  group by author
  order by popularity desc;

select name, popularity
from authors join popular_article_authors
on popular_article_authors.author = authors.id;

create view request_errors as
  select time::timestamp::date as date,
  COUNT(CASE WHEN status LIKE '%200 OK%' THEN 1 END) AS success,
  COUNT(CASE WHEN status LIKE '%404 NOT FOUND%' THEN 1 END) AS errors
  from log
  group by date;


### Table Schema

articles Table

 Column |           Type           |                       Modifiers
--------+--------------------------+-------------------------------------------------------
 author | integer                  | not null
 title  | text                     | not null
 slug   | text                     | not null
 lead   | text                     |
 body   | text                     |
 time   | timestamp with time zone | default now()
 id     | integer                  | not null default nextval('articles_id_seq'::regclass)
Indexes:
    "articles_pkey" PRIMARY KEY, btree (id)
    "articles_slug_key" UNIQUE CONSTRAINT, btree (slug)
Foreign-key constraints:
    "articles_author_fkey" FOREIGN KEY (author) REFERENCES authors(id)


Table "public.authors"
 Column |  Type   |                      Modifiers
--------+---------+------------------------------------------------------
 name   | text    | not null
 bio    | text    |
 id     | integer | not null default nextval('authors_id_seq'::regclass)
Indexes:
    "authors_pkey" PRIMARY KEY, btree (id)
Referenced by:
    TABLE "articles" CONSTRAINT "articles_author_fkey" FOREIGN KEY (author) REFERENCES authors(id)

Table "public.log"
 Column |           Type           |                    Modifiers
--------+--------------------------+--------------------------------------------------
 path   | text                     |
 ip     | inet                     |
 method | text                     |
 status | text                     |
 time   | timestamp with time zone | default now()
 id     | integer                  | not null default nextval('log_id_seq'::regclass)
Indexes:
    "log_pkey" PRIMARY KEY, btree (id)


