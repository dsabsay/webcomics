# webcomics

## Development Plan
* Implement `reads/` feature to mark strips as read when clicked.
* Bookmarks for narrative-style comics. Can be implemented as a bookmarklet. Will want to smartly handle when the user is not logged in by saving URL temporarily, requesting login, and then saving the bookmark when the user logs in.
* Viewer (for webcomic name)
* RSS feed updater
* DB backup job
* Add new comics. Will require mappings from feed fields -> DB columns.
