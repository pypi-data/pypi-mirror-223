from hypymedia.elements import (
    html_,
    head_,
    meta_,
    body_,
    title_,
    script_,
    header_,
    h1_,
    nav_,
    li_,
    ul_,
    main_,
    section_,
    div_,
    p_,
    aside_,
    footer_,
    a_,
    input_,
)


document = html_(
    {"lang": "en"},
    head_(
        meta_({"charset": "UTF-8"}),
        meta_({"http-equiv": "X-UA-Compatible", "content": "IE=edge"}),
        meta_({"name": "viewport", "content": "width=device-width, initial-scale=1.0"}),
        title_("Hypermediacy"),
        script_({"src": "https://unpkg.com/htmx.org@1.8.0"}),
    ),
    body_(
        {"id": "index", "class": "home", "hx-boost": "true"},
        header_(
            {"id": "banner", "class": "body"},
            h1_(
                a_(
                    {"href": "#"},
                    "Hypermediacy : Seeing the web as the web",
                ),
            ),
            nav_(
                ul_(
                    li_(
                        {"class": "active"},
                        a_({"href": "#"}, "home"),
                    ),
                ),
            ),
        ),
        main_(
            div_(),
            div_("THIS TEST"),
            section_(
                {"id": "content", "class": "body"},
                div_({"hx-get": "views/index/signin.html"}, "Sign In"),
            ),
            section_({"id": "notify"}, p_("User is not logged in")),
        ),
        aside_("Extra Content"),
        footer_("Footer"),
    ),
)

print(document)
