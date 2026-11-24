(() => {
    "use strict";
    const app = document.getElementById("app");
    const back = document.getElementById("back");
    const dialog = document.getElementById("dialog");
    const form = document.getElementById("dialog-form");
    const content = document.getElementById("dialog-content");
    const dialogError = document.getElementById("dialog-error");
    // Eel sends Python dictionaries as objects, with book IDs as string keys.
    let books = {};
    let stats = {};
    let topRatedBooks = [];
    let routeHistory = [];
    let previous = "";
    let generation = 0;

    // Helpers for building the interface.
    const createElement = (tag, text, cls) => {
        const el = document.createElement(tag);
        if (text != null) {
            el.textContent = text;
        }
        if (cls) {
            el.className = cls;
        }
        return el;
    };

    function appendChildren(parent, ...children) {
        parent.append(...children);
        return parent;
    }

    function makeButton(text, action, cls) {
        const b = createElement("button", text, cls);
        b.type = "button";
        b.addEventListener("click", action);
        return b;
    }

    function bookLink(text, id) {
        const a = createElement("a", text, "book-title");
        a.href = "#book/" + encodeURIComponent(id);
        return a;
    }

    function makePanel(title) {
        return appendChildren(createElement("section", null, "panel"), createElement("h2", title));
    }

    async function callPython(name, ...args) {
        if (!window.eel || typeof eel[name] !== "function") {
            throw new Error("Start Bookaholic through Python/Eel, not by opening index.html directly.");
        }
        return await eel[name](...args)();
    }

    function bookCover(book) {
        const fallback = createElement("div", "No cover available", "cover placeholder");
        const url = book.metadata.cover_url;
        if (!url || !/^https?:\/\//i.test(url)) {
            return fallback;
        }
        const img = createElement("img", null, "cover");
        img.alt = "Cover of " + book.metadata.title;
        img.src = url;
        img.addEventListener("error", () => img.replaceWith(fallback));
        return img;
    }

    function readingDays(book) {
        if (!book.rating) {
            return null;
        }
        return Math.max(1, Math.round((Date.parse(book.rating.finish_date) - Date.parse(book.metadata.start_date)) / 86400000) + 1);
    }

    function readingSpeed(book) {
        return Math.round(book.metadata.n_pages / readingDays(book) * 100) / 100;
    }

    function ratingStars(book) {
        return createElement("span", book.rating ? "★".repeat(book.rating.rating) + "☆".repeat(5 - book.rating.rating) : "Not rated", "stars");
    }

    function addStat(parent, label, value) {
        appendChildren(parent, appendChildren(createElement("div", null, "stat"), createElement("span", label, "muted"), createElement("strong", String(value))));
    }

    function showEmpty(parent, text) {
        parent.append(createElement("p", text, "empty"));
    }

    function bookCard(id, b) {
        return appendChildren(createElement("article", null, "book-card"), bookCover(b), bookLink(b.metadata.title, id), createElement("span", b.metadata.author, "muted"));
    }

    function makeTable(headers, rows) {
        let tableElement = createElement("table"), headerRow = createElement("tr");
        headers.forEach(heading => headerRow.append(createElement("th", heading)));
        tableElement.append(appendChildren(createElement("thead"), headerRow));
        let body = createElement("tbody");
        for (const row of rows) {
            let rowElement = createElement("tr");
            for (const value of row) {
                let cell = createElement("td");
                cell.append(value instanceof Node ? value : document.createTextNode(String(value)));
                rowElement.append(cell);
            }
            body.append(rowElement);
        }
        tableElement.append(body);
        return appendChildren(createElement("div", null, "table-wrap"), tableElement);
    }

    // Get the latest library data before drawing a page.
    async function refreshData() {
        const [library, summary, rated] = await Promise.all([
            callPython("get_library"),
            callPython("get_statistics_summary"),
            callPython("get_top_rated")
        ]);
        books = library;
        stats = summary;
        topRatedBooks = rated;
    }

    // Dashboard
    function showHome() {
        const actions = createElement("div", null, "actions");
        actions.append(
            makeButton("View Library", () => location.hash = "library"),
            makeButton("Add Book", openAdd, "secondary")
        );
        const head = appendChildren(
            createElement("div"),
            createElement("h1", "Your reading journey"),
            createElement("p", "Track your books and celebrate your progress.", "muted"),
            actions
        );
        app.append(head);
        const side = makePanel("Statistics");
        addStat(side, "Total books read", stats.total_books);
        addStat(side, "Total pages read", stats.total_pages);
        addStat(side, "Average pages per day", stats.overall_daily_avg_pages);
        for (const [label, key] of [["Yearly", "by_year"], ["Monthly", "by_month"], ["Weekly", "by_week"]]) {
            const d = appendChildren(createElement("details"), createElement("summary", label + " reading statistics"));
            const rows = Object.entries(stats[key] || {}).sort((a, b) => b[0].localeCompare(a[0])).map(([period, v]) => [period, v.books, v.pages]);
            if (rows.length) {
                d.append(makeTable(["Period", "Books", "Pages"], rows));
            } else {
                showEmpty(d, "No completed books yet.");
            }
            side.append(d);
        }
        const ranking = (stats.speed_ranking || []).map(id => [id, books[id]]).filter(([, b]) => b && b.rating);
        for (const [label, rows] of [["Fastest books", ranking], ["Slowest books", [...ranking].reverse()]]) {
            const d = appendChildren(createElement("details"), createElement("summary", label));
            if (rows.length) {
                d.append(makeTable(["Book", "Pages/day"], rows.map(([id, b]) => [bookLink(b.metadata.title, id), readingSpeed(b)])));
            } else {
                showEmpty(d, "No completed books yet.");
            }
            side.append(d);
        }
        const current = makePanel("Current books"), grid = createElement("div", null, "books");
        const reading = Object.entries(books).filter(([, b]) => !b.rating);
        reading.forEach(([id, b]) => grid.append(bookCard(id, b)));
        current.append(grid);
        if (!reading.length) {
            showEmpty(current, "No current books. Add a book to get started.");
        }
        const fav = makePanel("Favourite books");
        const rated = topRatedBooks.map(id => [id, books[id]]).filter(([, b]) => b && b.rating).sort((a, b) => b[1].rating.rating - a[1].rating.rating);
        if (rated.length) {
            fav.append(makeTable(["Title", "Rating"], rated.map(([id, b]) => [bookLink(b.metadata.title, id), ratingStars(b)])));
        } else {
            showEmpty(fav, "Books rated 4 or 5 stars will appear here.");
        }
        app.append(appendChildren(createElement("div", null, "dashboard"), side, appendChildren(createElement("div"), current, fav)));
    }

    // Library search and filters
    function showLibrary() {
        app.append(createElement("h1", "Library"), createElement("p", "Browse or search your collection.", "muted"));
        const search = createElement("input");
        search.type = "search";
        search.placeholder = "Search by title or author";
        search.setAttribute("aria-label", "Search books");
        const filter = createElement("select");
        filter.setAttribute("aria-label", "Reading status");
        for (const [v, t] of [["all", "All books"], ["reading", "Currently reading"], ["finished", "Completed"]]) {
            const o = createElement("option", t);
            o.value = v;
            filter.append(o);
        }
        const ratingFilter = createElement("select");
        ratingFilter.setAttribute("aria-label", "Star rating");
        for (const [v, t] of [["all", "All ratings"], ["5", "★★★★★ (5 stars)"], ["4", "★★★★☆ (4 stars)"], ["3", "★★★☆☆ (3 stars)"], ["2", "★★☆☆☆ (2 stars)"], ["1", "★☆☆☆☆ (1 star)"], ["none", "Not rated"]]) {
            const o = createElement("option", t);
            o.value = v;
            ratingFilter.append(o);
        }
        const results = createElement("div", null, "panel");
        app.append(appendChildren(createElement("div", null, "filters"), search, filter, ratingFilter), results);
        function update() {
            const q = search.value.trim().toLowerCase();
            const rows = Object.entries(books)
                .filter(([, book]) => {
                    const text = `${book.metadata.title} ${book.metadata.author}`.toLowerCase();
                    const matchesSearch = text.includes(q);
                    const matchesStatus = filter.value === "all" ||
                        (filter.value === "finished" ? !!book.rating : !book.rating);
                    const matchesRating = ratingFilter.value === "all" ||
                        (ratingFilter.value === "none"
                            ? !book.rating
                            : book.rating?.rating === Number(ratingFilter.value));

                    return matchesSearch && matchesStatus && matchesRating;
                })
                .sort((a, b) => a[1].metadata.title.localeCompare(b[1].metadata.title));
            results.replaceChildren(createElement("p", `${rows.length} book${rows.length === 1 ? "" : "s"}`, "muted"));
            if (rows.length) {
                results.append(makeTable(["Title", "Author", "Status", "Rating"], rows.map(([id, b]) => [bookLink(b.metadata.title, id), b.metadata.author, b.rating ? "Completed" : "Reading", ratingStars(b)])));
            } else {
                showEmpty(results, "No matching books.");
            }
        }
        search.addEventListener("input", update);
        filter.addEventListener("change", update);
        ratingFilter.addEventListener("change", update);
        update();
    }

    // Individual book page
    function showBook(id) {
        const book = books[id];
        if (!book) {
            app.append(createElement("h1", "Book not found"), makeButton("View Library", () => location.hash = "library"));
            return;
        }
        const metadata = book.metadata, subject = book.subject, rating = book.rating;
        app.append(createElement("h1", metadata.title), createElement("p", metadata.author, "muted"));
        const infoPanel = makePanel("Book information");
        const fields = createElement("dl", null, "fields");
        const values = [["Author", metadata.author], ["Pages", metadata.n_pages], ["Type", subject.fiction ? "Fiction" : "Non-fiction"], ["Genres", subject.genres.join(", ") || "Unclassified"], ["Start date", metadata.start_date], ["Status", rating ? "Completed" : "Currently reading"]];
        if (rating) {
            values.push(["Finish date", rating.finish_date], ["Days taken", readingDays(book)], ["Pages per day", readingSpeed(book)]);
        }
        for (const [label, value] of values) {
            fields.append(appendChildren(createElement("div"), createElement("dt", label), createElement("dd", String(value))));
        }
        infoPanel.append(appendChildren(createElement("div", null, "detail"), bookCover(book), fields));
        app.append(infoPanel);
        if (rating) {
            const review = makePanel("Your review");
            review.append(ratingStars(book), createElement("p", rating.review || "No written review.", "review"));
            app.append(review);
        }
        app.append(appendChildren(createElement("div", null, "actions"), makeButton(rating ? "Edit Review" : "Mark as Finished", () => openReview(id, book)), makeButton("Delete Book", () => openDelete(id, book), "secondary danger")));
    }

    // Dialogs and form fields
    function today() {
        const d = new Date();
        return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
    }

    function addField(label, type, value = "", required = true) {
        const input = createElement(type === "textarea" ? "textarea" : "input");
        if (type !== "textarea") {
            input.type = type;
        }
        input.value = value;
        input.required = required;
        content.append(appendChildren(createElement("label", label), input));
        return input;
    }

    function openModal(title, submit, handler) {
        content.replaceChildren(createElement("h2", title));
        dialogError.textContent = "";
        const save = document.getElementById("submit-dialog");
        save.textContent = submit;
        save.disabled = false;
        form.onsubmit = async (e) => {
            e.preventDefault();
            save.disabled = true;
            dialogError.textContent = "";
            try {
                await handler();
                dialog.close();
                await render();
            } catch (err) {
                dialogError.textContent = String(err.message || err);
            } finally {
                save.disabled = false;
            }
        };
        dialog.showModal();
    }

    function openReview(id, b) {
        let rating, date, review;
        openModal("Review " + b.metadata.title, "Save review", async () => {
            if (date.value < b.metadata.start_date) {
                throw new Error("Finish date must be on or after the start date.");
            }
            await callPython("finish_book", Number(id), Number(rating.value), date.value, review.value);
        });
        rating = addField("Rating (1–5 stars)", "number", b.rating?.rating || 5);
        rating.min = 1;
        rating.max = 5;
        rating.step = 1;
        date = addField("Book end date", "date", b.rating?.finish_date || today());
        date.min = b.metadata.start_date;
        review = addField("Written review", "textarea", b.rating?.review || "", false);
    }

    function openDelete(id, b) {
        openModal("Delete book?", "Delete", async () => {
            await callPython("remove_book", Number(id));
            location.hash = "library";
        });
        content.append(createElement("p", "Remove " + b.metadata.title + " and its review from your library?"));
    }

    async function openAdd() {
        let title, author, pages, start, url, type, genres;
        openModal("Add a book", "Add to Library", async () => {
            if (!title.value.trim() || !author.value.trim()) {
                throw new Error("Enter a title and author.");
            }
            const book = {
                metadata: {
                    title: title.value.trim(),
                    author: author.value.trim(),
                    n_pages: Number(pages.value),
                    cover_url: url.value.trim() || null,
                    start_date: start.value
                },
                subject: {
                    fiction: type.value === "fiction",
                    genres: [...genres.selectedOptions].map(option => option.value)
                },
                rating: null
            };

            await callPython("add_book", book);
        });
        const isbn = addField("ISBN (10 or 13 digits)", "text", "", false);
        isbn.placeholder = "9780261102217";
        const isbnLookup = makeButton("Search by ISBN", () => lookupBook(true), "secondary");
        content.append(isbnLookup);
        title = addField("Title", "text");
        author = addField("Author", "text");
        const lookup = makeButton("Search by Title and Author", () => lookupBook(false), "secondary");
        content.append(lookup);
        async function lookupBook(byISBN) {
            const code = isbn.value.replace(/[\s-]/g, "").toUpperCase();
            if (byISBN && !/^(?:[0-9]{9}[0-9X]|[0-9]{13})$/.test(code)) {
                dialogError.textContent = "Enter a valid 10- or 13-character ISBN.";
                return;
            }
            if (!byISBN && (!title.value.trim() || !author.value.trim())) {
                dialogError.textContent = "Enter both title and author first.";
                return;
            }
            lookup.disabled = isbnLookup.disabled = true;
            const save = document.getElementById("submit-dialog");
            save.disabled = true;
            dialogError.textContent = "Searching…";
            try {
                const b = byISBN ? await callPython("create_book_by_isbn_search", code) : await callPython("create_book_by_title_and_author_search", title.value.trim(), author.value.trim());
                if (!b) {
                    throw new Error("Book not found");
                }
                title.value = b.metadata.title;
                author.value = b.metadata.author;
                pages.value = b.metadata.n_pages;
                url.value = b.metadata.cover_url || "";
                type.value = b.subject.fiction ? "fiction" : "nonfiction";
                await updateGenres(b.subject.genres);
                dialogError.textContent = "";
            } catch (e) {
                dialogError.textContent = "Lookup failed. Check your search or enter the book manually.";
            } finally {
                lookup.disabled = isbnLookup.disabled = save.disabled = false;
            }
        }
        pages = addField("Pages", "number");
        pages.min = 1;
        pages.step = 1;
        url = addField("Cover image URL", "url", "", false);
        start = addField("Start date", "date", today());
        type = createElement("select");
        for (const [v, t] of [["fiction", "Fiction"], ["nonfiction", "Non-fiction"]]) {
            const o = createElement("option", t);
            o.value = v;
            type.append(o);
        }
        content.append(appendChildren(createElement("label", "Type"), type));
        genres = createElement("select");
        genres.multiple = true;
        genres.size = 5;
        content.append(appendChildren(createElement("label", "Genres (Ctrl/Cmd to select multiple)"), genres));
        async function updateGenres(selected = []) {
            const values = await callPython(type.value === "fiction" ? "get_fiction_genres" : "get_non_fiction_genres");
            genres.replaceChildren(...values.map(v => {
                const o = createElement("option", v);
                o.value = v;
                o.selected = selected.includes(v);
                return o;
            }));
        }
        type.addEventListener("change", () => updateGenres().catch(e => dialogError.textContent = String(e)));
        try {
            await updateGenres();
        } catch (e) {
            dialogError.textContent = "Could not load genres.";
        }
    }

    // Navigation and page updates
    async function render() {
        const token = ++generation;
        app.replaceChildren(createElement("p", "Loading your library…", "muted"));
        try {
            await refreshData();
            if (token !== generation) {
                return;
            }
            app.replaceChildren();
            const route = location.hash.slice(1) || "home";
            if (route === "library") {
                showLibrary();
            } else if (route.startsWith("book/")) {
                showBook(decodeURIComponent(route.slice(5)));
            } else {
                showHome();
            }
        } catch (e) {
            if (token !== generation) {
                return;
            }
            app.replaceChildren(createElement("h1", "Unable to load Bookaholic"), createElement("p", String(e.message || e), "error"), makeButton("Try again", render));
        }
    }

    function onRoute() {
        const current = location.hash || "#home";
        if (previous && previous !== current) {
            routeHistory.push(previous);
        }
        previous = current;
        back.disabled = current === "#home" && !routeHistory.length;
        render();
    }
    back.addEventListener("click", () => {
        if (routeHistory.length) {
            const target = routeHistory.pop();
            previous = target;
            location.hash = target;
        } else if (location.hash !== "#home") {
            previous = "#home";
            location.hash = "home";
        }
    });
    document.getElementById("cancel-dialog").addEventListener("click", () => dialog.close());
    window.addEventListener("hashchange", onRoute);
    if (!location.hash) {
        history.replaceState(null, "", "#home");
    }
    onRoute();
})();
