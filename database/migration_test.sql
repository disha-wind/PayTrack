insert into "user" (id, email, password_hash, full_name)
values (1,'admin@gmail.com','$2b$12$MjRsxhcKKmGXiTBsITez8uExAHT.Ooeaeo2m0HbuAEFQC/Mt1HaP2','Admin Test'),
       (2,'user@gmail.com','$2b$12$sl8ACbQQ/ZGLHip3F9LMMeNhAT8ehbiqeZ5mUl0QJUQtioleawQEC','User Test');

insert into admin (user_id)
values (1);

insert into account (id, user_id)
values (1, 2);
