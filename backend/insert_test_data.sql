-- Inserts a bunch of test data

INSERT INTO comics VALUES ("Nedroid", "Anthony Clark", "http://nedroid.com/");
INSERT INTO comics VALUES ("webcomic name", "Alex Norris", "https://webcomicname.com/");

INSERT INTO strips (title, link, datePublished, description, comic)
    VALUES ("Hypocrisy", "https://webcomicname.com/post/186677278334", "20190731T072008-0700", "some description", "webcomic name");
INSERT INTO strips (title, link, datePublished, description, comic)
    VALUES ("Running Gag", "https://webcomicname.com/post/186631606894", "20190729T085610-0700", "some description", "webcomic name");
INSERT INTO strips (title, link, datePublished, comic)
    VALUES ("Tangent", "https://webcomicname.com/post/186495985534", "20190723T102619-0700", "webcomic name");
INSERT INTO strips (title, link, datePublished, comic)
    VALUES ("Brand New Day", "http://nedroid.com/2019/09/brand-new-day/", "20190906T103223-0700", "Nedroid");

INSERT INTO reads SELECT id FROM strips WHERE title="Tangent" LIMIT 1;
