pragma foreign_keys = on;

begin;

create table if not exists 'feed' (
    'title' text not null,
    'link' text not null,
    'number' integer not null,
    'folder' text not null,
    
    primary key ('title')
);

create table if not exists 'episode' (
    'feed' text not null,
    'title' text not null,
    'date' text not null,
    'link' text not null,
    'file' text not null,
    
    constraint 'episode_has_feed' foreign key ('feed') references 'feed' ('title'),
    primary key ('feed', 'title')
);

commit;
