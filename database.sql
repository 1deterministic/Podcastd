begin;

create table if not exists "feed" (
  "title" varchar (255) not null,
  "link" varchar (255) not null,
  "number" integer not null,
  "folder" varchar (255) not null,

  primary key ("title")
);

create table if not exists "entry" (
  "title" varchar (255) not null,
  "feed" varchar (255) not null,
  "date" integer not null,
  "link" varchar (255) not null,
  "file" varchar (255) not null,
  "downloaded" varchar (255) not null check ("downloaded" in ("True", "False")),

  primary key ("title", "feed"),
  constraint "feed_of_entry" foreign key ("feed") references "feed" ("title")
);

commit;