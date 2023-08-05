#[macro_use]
extern crate lazy_static;
use ammonia::Builder;
use pulldown_cmark as md;
use regex_lite::{Captures, Regex};
use std::collections::HashMap;

pub struct User {
    pub username: String,
    pub user_id: String,
    pub link: String,
    pub fullname: String,
}

trait MarkminiWhitelist {
    fn allow_code_classes(&mut self) -> &mut Self;
    fn allow_chosen_tailwind(&mut self) -> &mut Self;
}

impl<'a> MarkminiWhitelist for Builder<'a> {
    fn allow_code_classes(&mut self) -> &mut Self {
        // Separate function due to long list.
        // List is more extensive than it needs, but its not a security issue.
        // Languages are grouped together (js goes with javascript etc.) and sorted as well as I can.
        self.add_allowed_classes(
            "code",
            &[
                "language-sh",
                "language-bash",
                "language-c",
                "language-cs",
                "language-csharp",
                "language-cpp",
                "language-django",
                "language-docker",
                "language-dockerfile",
                "language-fortran",
                "language-go",
                "language-hs",
                "language-haskell",
                "language-java",
                "language-js",
                "language-javascript",
                "language-jsx",
                "language-jinja2",
                "language-julia",
                "language-json",
                "language-json5",
                "language-kt",
                "language-kotlin",
                "language-latex",
                "language-lua",
                "language-lolcode",
                "language-md",
                "language-markdown",
                "language-matlab",
                "language-mongodb",
                "language-nginx",
                "language-nim",
                "language-objc",
                "language-ocaml",
                "language-perl",
                "language-php",
                "language-py",
                "language-python",
                "language-regex",
                "language-rs",
                "language-rust",
                "language-sass",
                "language-scss",
                "language-smarty",
                "language-sql",
                "language-swift",
                "language-tex",
                "language-toml",
                "language-ts",
                "language-typescript",
                "language-tsx",
                "language-yml",
                "language-yaml",
                "language-zig",
            ],
        );
        return self;
    }

    fn allow_chosen_tailwind(&mut self) -> &mut Self {
        // Usually people don't style anything, but if they want to they can.
        // These tags also need to be safelisted in tailwind config or else they might get treeshaken away

        let inline_tags = ["a", "span", "h1", "h2", "h3", "h4", "h5"];
        let block_tags = ["p", "div", "t-spoiler", "t-quote"];
        // Allowed on both
        for &tag in inline_tags.iter().chain(block_tags.iter()) {
            self.add_allowed_classes(
                tag,
                &[
                    "primary",
                    "secondary",
                    "accent-1",
                    "accent-2",
                    "accent-3",
                    "accent-4",
                    "font-header",
                    "font-body",
                ],
            );
        }

        // Inline tags
        for tag in inline_tags {
            self.add_allowed_classes(tag, &["idk"]);
        }

        // Block tags
        for tag in block_tags {
            self.add_allowed_classes(tag, &["inverse-header"]);
        }

        return self;
    }
}

lazy_static! {
    // Feels a little hacky matching angle brackets, but it's
    // to allow the tag to be immediately after a html tag
    static ref USER_REGEX: Regex = Regex::new(r"(^|\s|<[^>]*>)@(\w+|\d+)").unwrap();
}

pub struct Markmini {
    tag_to_link: HashMap<String, String>,
}

impl Markmini {
    pub fn new() -> Self {
        return Self {
            tag_to_link: HashMap::new(),
        };
    }

    pub fn add_users(&mut self, users: Vec<User>) {
        for u in users {
            let link = String::from("<a href=\"") + &u.link + "\">" + &u.fullname + "</a>";
            self.tag_to_link.insert(u.user_id, link.clone());
            self.tag_to_link.insert(u.username, link);
        }
    }

    pub fn compile(&self, input: &str) -> String {
        let mut output = self.mardownify(input);
        output = self.replace_tags_with_links(&output);
        output = self.sanitize(&output);
        return output;
    }

    pub fn compile_comment(&self, input: &str) -> String {
        let mut output = self.replace_tags_with_links(input);
        output = self.sanitize_comment(&output);
        return output;
    }

    fn mardownify(&self, input: &str) -> String {
        let mut options = md::Options::empty();
        // Enable some Github flavored markdown features
        options.insert(md::Options::ENABLE_STRIKETHROUGH);
        options.insert(md::Options::ENABLE_TABLES);
        options.insert(md::Options::ENABLE_TASKLISTS);
        let parser = md::Parser::new_ext(input, options);
        let mut output = String::new();
        md::html::push_html(&mut output, parser);
        return output;
    }

    fn replace_tags_with_links(&self, input: &str) -> String {
        #[cfg(test)]
        dbg!(input);

        let replacer = |c: &Captures| match self.tag_to_link.get(&c[2]) {
            // Note: capture 0 is entire match, capture 1 is the optional leading whitespace, capture 2 is the uid or username
            Some(link) => String::new() + &c[1] + link,
            None => String::new() + &c[1] + "@" + &c[2],
        };

        let output = USER_REGEX.replace_all(input, replacer);

        return output.to_string();
    }

    /// Sanitize output html to avoid security issues
    fn sanitize(&self, input: &str) -> String {
        // Ammonia sanitizes our output html.
        // It's defaults are very strict so we whitelist som
        return Builder::default()
            // allow lit component html tags
            .add_tags(&["t-spoiler", "t-quote"])
            .add_tag_attributes("t-spoiler", &["open"])
            .add_tag_attributes("t-quote", &["name"])
            // Open question: only allow spans as slots?
            .add_tag_attributes("span", &["slot"])
            .allow_code_classes()
            .allow_chosen_tailwind()
            .clean(input)
            .to_string();
    }

    fn sanitize_comment(&self, input: &str) -> String {
        // Ammonia sanitizes our output html.
        // Very strict defaults are fine since comments are mostly pure text
        return Builder::default().clean(input).to_string();
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn regular_markdown() {
        let compiler = Markmini::new();
        let result = compiler.compile("# Hello world!");
        assert_eq!(result, "<h1>Hello world!</h1>\n");

        let result = compiler.compile("Midway in writing <");
        assert_ne!(result, "");
    }

    #[test]
    fn with_users() {
        let mut compiler = Markmini::new();
        compiler.add_users(vec![User {
            user_id: "1".to_string(),
            username: "testy".to_string(),
            link: "/users/1".to_string(),
            fullname: "Test McTestern".to_string(),
        }]);

        let result = compiler.compile("Yo @testy se her");
        assert_eq!(
            result,
            "<p>Yo <a href=\"/users/1\" rel=\"noopener noreferrer\">Test McTestern</a> se her</p>\n"
        );

        let result = compiler.compile("@testy se her");
        assert_eq!(
            result,
            "<p><a href=\"/users/1\" rel=\"noopener noreferrer\">Test McTestern</a> se her</p>\n"
        );

        let result = compiler.compile("@finsikke finnes ikke");
        assert_eq!(result, "<p>@finsikke finnes ikke</p>\n");

        let result = compiler.compile("Hey, @finsikke finnes ikke");
        assert_eq!(result, "<p>Hey, @finsikke finnes ikke</p>\n");

        let result = compiler.compile("# @testy");
        assert_eq!(
            result,
            "<h1><a href=\"/users/1\" rel=\"noopener noreferrer\">Test McTestern</a></h1>\n"
        )
    }

    #[test]
    fn code_blocks() {
        let compiler = Markmini::new();
        let result = compiler.compile("```rs\nfn test() {}\n```");
        assert_eq!(
            result,
            "<pre><code class=\"language-rs\">fn test() {}\n</code></pre>\n"
        );
    }

    #[test]
    fn comments() {
        let mut compiler = Markmini::new();
        compiler.add_users(vec![User {
            user_id: "1".to_string(),
            username: "testy".to_string(),
            link: "/users/1".to_string(),
            fullname: "Test McTestern".to_string(),
        }]);
        let result = compiler.compile_comment("Yo @testy se her");
        assert_eq!(
            result,
            "<p>Yo <a href=\"/users/1\" rel=\"noopener noreferrer\">Test McTestern</a> se her</p>\n"
        );

        let result = compiler.compile_comment("# Markdown funker ikke");
        assert_eq!(result, "# Markdown funker ikke\n");
    }
}
