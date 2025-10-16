create table if not exists users (
  id bigserial primary key,
  name text not null,
  email text unique not null,
  phone text,
  company text,
  password_hash text not null,
  avatar_url text,
  created_at timestamptz default now()
);
