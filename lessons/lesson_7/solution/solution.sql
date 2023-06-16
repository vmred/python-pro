drop table if exists products;
drop table if exists storages;

create table storages (
  id SERIAL primary key,
  name VARCHAR(50) not null,
  address VARCHAR(100) not null
);

CREATE TABLE products (
  id SERIAL PRIMARY KEY,
  name VARCHAR(50) NOT NULL,
  price NUMERIC(10, 2) NOT NULL,
  storage_id INTEGER REFERENCES storages(id)
);

insert into storages (name, address) values
('rozetka', '1001, 1 random street, random city, random country'),
('atb', '1002, 2 random street, random city, random country'),
('tavria_v', '1003, 3 random street, random city, random country');

insert into products (name, price, storage_id) values
('iphone 14', 1000, 1),
('iphone 13', 900, 1),
('iphone 12', 800, 1),
('iphone 11', 700, 1),
('milk', 2, 2),
('bread', 1, 2),
('tea', 2, 2),
('beer', 1, 3),
('apple juice', 2, 3),
('orange juice', 2, 3);

update products set price = 1.5 where name = 'apple juice';

delete from products where storage_id = 1;

create index idx_product_name on products (name);