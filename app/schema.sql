create table if not exists messages (
    id integer primary key,
    name text default Anonymous,
    message text not null,
    created timestamp not null
);