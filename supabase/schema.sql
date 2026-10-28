-- Run this ONCE in Supabase: SQL Editor > New query > paste > Run.
-- It makes one table called "readings". Each row is one reading of one pump.
create table readings (
  id bigint generated always as identity primary key,   -- unique number, made automatically
  pump text not null,                                    -- for example P-101
  time timestamptz not null default now(),               -- when the reading was taken
  vibration double precision not null,                   -- mm/s
  bearing_temp double precision not null,                -- degrees C
  discharge_pressure double precision not null,          -- bar
  flow double precision not null                         -- m3/h
);

-- History of changes made on the Manage page (add, edit, delete).
-- Already made the readings table? Run just this part.
create table activity_log (
  id bigint generated always as identity primary key,
  time timestamptz not null default now(),               -- when the change was made
  action text not null,                                  -- Added, Edited or Deleted
  pump text not null,                                    -- for example P-101
  reading_id bigint,                                     -- which reading was changed
  details text                                           -- what changed
);
