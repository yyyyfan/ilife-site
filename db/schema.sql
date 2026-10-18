-- iLiFE! 粉丝站数据库（SQLite）。data/*.json 由 export.py 从本库生成。
-- 约定：*_order 列保存原 JSON 对象的键顺序（逗号分隔），用于逐字节还原；
--       键在 key_order 中而列为 NULL 表示 JSON 中显式为 null，不在则表示该键不存在。
PRAGMA foreign_keys = ON;

CREATE TABLE meta (            -- 杂项（timeline.json 的 source/note 等）
  key   TEXT PRIMARY KEY,
  value TEXT NOT NULL
);

CREATE TABLE sources (         -- 所有出处 URL
  id  INTEGER PRIMARY KEY,
  url TEXT NOT NULL UNIQUE
);

CREATE TABLE members (
  id           INTEGER PRIMARY KEY,
  sort         INTEGER NOT NULL UNIQUE,     -- members.json 中的顺序
  tl_sort      INTEGER UNIQUE,              -- timeline.json 中的顺序
  name         TEXT NOT NULL UNIQUE,
  kana TEXT, birthday TEXT, color TEXT, hex TEXT, joined TEXT, note TEXT,
  status TEXT, romaji TEXT, role TEXT, x TEXT, x_status TEXT, catch TEXT,
  hex_note TEXT, support TEXT, left_ TEXT, color_source TEXT,
  source_id    INTEGER REFERENCES sources(id),
  key_order    TEXT NOT NULL
);

CREATE TABLE member_fields_sources (  -- members.json 的 sources{字段: URL}
  member_id INTEGER NOT NULL REFERENCES members(id),
  field     TEXT NOT NULL,
  source_id INTEGER NOT NULL REFERENCES sources(id),
  ord       INTEGER NOT NULL,
  PRIMARY KEY (member_id, field)
);

CREATE TABLE member_periods (  -- 在籍区间（timeline.json segments）
  id        INTEGER PRIMARY KEY,
  member_id INTEGER NOT NULL REFERENCES members(id),
  ord       INTEGER NOT NULL,
  type      TEXT NOT NULL CHECK (type IN ('r','s','n')), -- r=正式 regular, s=支援 support, n=非正式/候补生 trainee
  label     TEXT NOT NULL,
  color     TEXT,
  date_from TEXT NOT NULL,
  date_to   TEXT,                -- NULL = 至今
  key_order TEXT NOT NULL,
  UNIQUE (member_id, ord)
);

CREATE TABLE timeline_marks (
  id INTEGER PRIMARY KEY, date TEXT NOT NULL, label TEXT NOT NULL
);

CREATE TABLE eras (
  id         TEXT PRIMARY KEY,   -- e1..eN
  sort       INTEGER NOT NULL UNIQUE,
  name       TEXT NOT NULL,
  start      TEXT NOT NULL,
  change     TEXT,
  source_id  INTEGER REFERENCES sources(id)
);

CREATE TABLE era_members (
  era_id    TEXT NOT NULL REFERENCES eras(id),
  member_id INTEGER NOT NULL REFERENCES members(id),
  ord       INTEGER NOT NULL,
  role      TEXT,                -- 例：支援 / 副支援 / 休止（NULL=正式）
  PRIMARY KEY (era_id, member_id)
);

CREATE TABLE venues (
  id   INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  pref TEXT NOT NULL,
  UNIQUE (name, pref)
);

CREATE TABLE lives (
  id        INTEGER PRIMARY KEY,
  date      TEXT NOT NULL,
  title     TEXT NOT NULL,
  venue_id  INTEGER NOT NULL REFERENCES venues(id),
  source_id INTEGER REFERENCES sources(id)
);

CREATE TABLE songs (
  id             INTEGER PRIMARY KEY,
  title          TEXT NOT NULL UNIQUE,
  kana           TEXT,
  mv_date        TEXT,
  release_date   TEXT,
  release        TEXT,
  note           TEXT,
  source_id      INTEGER REFERENCES sources(id),
  cover_image_id INTEGER REFERENCES images(id)
);


CREATE TABLE costumes (
  id         INTEGER PRIMARY KEY,
  name       TEXT NOT NULL,
  song_id    INTEGER NOT NULL REFERENCES songs(id),
  era_id     TEXT NOT NULL REFERENCES eras(id),
  debut_date TEXT,
  image_id   INTEGER REFERENCES images(id),
  note       TEXT,
  source_id  INTEGER REFERENCES sources(id)
);

CREATE TABLE costume_images (
  costume_id INTEGER NOT NULL REFERENCES costumes(id),
  image_id   INTEGER NOT NULL REFERENCES images(id),
  ord        INTEGER NOT NULL,
  PRIMARY KEY (costume_id, image_id)
);

CREATE TABLE images (
  id          INTEGER PRIMARY KEY,  -- = images.json 中的顺序（从 1 开始）
  url         TEXT NOT NULL,
  orig        TEXT,
  date        TEXT NOT NULL,
  post_id     INTEGER REFERENCES sources(id),  -- 来源推文/存档页
  text        TEXT,
  category    TEXT,
  local       TEXT,                 -- 站内相对路径 img/...
  source      TEXT,                 -- 来源说明（X @账号 / Wayback）
  kind        TEXT,                 -- individual / group / NULL
  era         TEXT REFERENCES eras(id),  -- 人工指定的时期（站点按此分组显示；为空则不在时期分组中出现）
  w INTEGER, h INTEGER,
  match       TEXT,
  crop_of     TEXT,
  review      TEXT CHECK (review IN ('confirmed','uncertain','retagged')),
  review_note TEXT,
  related     INTEGER,
  pending     TEXT,                 -- '待确认'
  key_order   TEXT NOT NULL
);

CREATE TABLE image_members (
  image_id  INTEGER NOT NULL REFERENCES images(id),
  member_id INTEGER NOT NULL REFERENCES members(id),
  PRIMARY KEY (image_id, member_id)
);

CREATE TABLE image_eras (      -- 按图片日期推导（export 时重算校验）
  image_id INTEGER NOT NULL REFERENCES images(id),
  era_id   TEXT NOT NULL REFERENCES eras(id),
  PRIMARY KEY (image_id, era_id)
);

CREATE INDEX idx_images_date ON images(date);
CREATE INDEX idx_image_members_m ON image_members(member_id);
