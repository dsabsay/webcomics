-- Inserts a bunch of test data

INSERT INTO comics VALUES ("Nedroid", "Anthony Clark", "http://nedroid.com/", "http://nedroid.com/favicon.ico", "episodic");
INSERT INTO comics VALUES ("webcomic name", "Alex Norris", "https://webcomicname.com/", "https://66.media.tumblr.com/avatar_44d7cb4c7049_128.pnj", "episodic");
INSERT INTO comics VALUES ("BACK", "Anthony Clark & KC Green", "http://backcomic.com/", "http://backcomic.com/monad.png", "serial");
INSERT INTO comics VALUES ("Elfquest", "Wendy and Richard Pini", "http://elfquest.com/read/digitalEQ.html", "http://elfquest.com/images/heads/0.jpg", "serial");

INSERT INTO strips (title, link, datePublished, description, comic)
    VALUES ("Hypocrisy", "https://webcomicname.com/post/186677278334", "20190731T072008-0700", "some description", "webcomic name");
INSERT INTO strips (title, link, datePublished, description, comic)
    VALUES ("Running Gag", "https://webcomicname.com/post/186631606894", "20190729T085610-0700", "some description", "webcomic name");
INSERT INTO strips (title, link, datePublished, comic)
    VALUES ("Tangent", "https://webcomicname.com/post/186495985534", "20190723T102619-0700", "webcomic name");
INSERT INTO strips (title, link, datePublished, comic)
    VALUES ("Brand New Day", "http://nedroid.com/2019/09/brand-new-day/", "20190906T103223-0700", "Nedroid");

-- This assumes that a user with ID of `1` exists.
INSERT INTO reads SELECT id, 1 FROM strips WHERE title="Tangent" LIMIT 1;
INSERT INTO bookmarks VALUES ("BACK", 1, "https://www.backcomic.com/3");
