BEGIN;
--
-- Create model Comment
--
CREATE TABLE "news_comment" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "user_name" varchar(100) NOT NULL, "email" varchar(254) NOT NULL, "text" text NOT NULL, "created_at" datetime NOT NULL, "is_moderated" bool NOT NULL);
--
-- Create model News
--
CREATE TABLE "news_news" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "title" varchar(150) NOT NULL, "content" text NOT NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "photo" varchar(100) NOT NULL, "is_published" bool NOT NULL);
COMMIT;
