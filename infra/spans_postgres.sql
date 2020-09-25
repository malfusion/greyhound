-- -------------------------------------------------------------
-- TablePlus 3.9.1(342)
--
-- https://tableplus.com/
--
-- Database: postgres
-- Generation Time: 2020-09-19 18:24:01.2990
-- -------------------------------------------------------------


-- This script only contains the table creation statements and does not fully represent the table in the database. It's still missing: indices, triggers. Do not use it as a backup.

-- Sequence and defined type
CREATE SEQUENCE IF NOT EXISTS spans_span_id_seq;

-- Table Definition
CREATE TABLE "public"."spans" (
    "span_id" int8 NOT NULL DEFAULT nextval('spans_span_id_seq'::regclass),
    "parent_span_id" int8,
    "process_id" int8,
    "cont_id" int8,
    "start_time" timestamp,
    "end_time" timestamp,
    "tags" json,
    PRIMARY KEY ("span_id")
);

