BEGIN;
--
-- Add field rating to comment
--
CREATE TABLE "new__news_comment" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "rating" smallint unsigned NOT NULL CHECK ("rating" >= 0), "user_name" varchar(100) NOT NULL, "email" varchar(254) NOT NULL, "text" text NOT NULL, "created_at" datetime NOT NULL, "is_moderated" bool NOT NULL);
INSERT INTO "new__news_comment" ("id", "user_name", "email", "text", "created_at", "is_moderated", "rating") SELECT "id", "user_name", "email", "text", "created_at", "is_moderated", 3 FROM "news_comment";
DROP TABLE "news_comment";
ALTER TABLE "new__news_comment" RENAME TO "news_comment";
--
-- Create constraint comment_rating_1_to_5 on model comment
--
CREATE TABLE "new__news_comment" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "user_name" varchar(100) NOT NULL, "email" varchar(254) NOT NULL, "text" text NOT NULL, "created_at" datetime NOT NULL, "is_moderated" bool NOT NULL, "rating" smallint unsigned NOT NULL CHECK ("rating" >= 0), CONSTRAINT "comment_rating_1_to_5" CHECK (("rating" >= 1 AND "rating" <= 5)));
INSERT INTO "new__news_comment" ("id", "user_name", "email", "text", "created_at", "is_moderated", "rating") SELECT "id", "user_name", "email", "text", "created_at", "is_moderated", "rating" FROM "news_comment";
DROP TABLE "news_comment";
ALTER TABLE "new__news_comment" RENAME TO "news_comment";
COMMIT;
