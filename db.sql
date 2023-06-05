CREATE TABLE users(
	id serial primary key,
	user_name text,
	email text,
	pass text,
	reg_date timestamp default now(),
	status_id int default 0
);
ALTER TABLE users ADD COLUMN confirm_email_hash TEXT;
ALTER TABLE users ADD COLUMN change_pass_hash TEXT;
create unique index users_email_uniqix on users(email);
create unique index users_user_name_uniqix on users(user_name);
insert into users
(user_name, email, pass, status_id)
values
--('lena', 'lena@gmail.com', 'pass1', 2)
('oto', 'oshavadze@gmail.com', 'pass2', 1);
select * from users order by id;
DELETE FROM USERS where id > 1

CREATE TABLE reg_code(
	code TEXT
);
INSERT INTO reg_code(code) VALUES ('asda.asda');
SELECT * FROM reg_code


 

CREATE TABLE re_objects (
	id serial primary key,
	region text,
	municipality text,
	settlement text,
	addres text,
	rooms_cnt numeric,
	_floor  int,
	
	added_by int,
	added_date timestamp default now(),
	modified_by int,
	modified_date timestamp  default now()
);


insert into re_objects
(region, municipality,   rooms_cnt, _floor, added_by , addres )
values
('ქვემო ქართლი', 'რუსთავი',  2, 1, 1,  'ბლაბლა ბლაბლა ბლაბლა ბლაბლა ბლაბლა ბლაბლა ბლაბლა2 ბლაბლა ბლაბლა ბლაბლა ბლაბლა4 ')
;
select * from re_objects



 