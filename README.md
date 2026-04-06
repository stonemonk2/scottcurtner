# scottcurtner.com

Personal professional website for Scott Curtner, CIA, CISA — Technology Audit Manager and GRC leader based in the San Francisco Bay Area.

## About this site

Built as a static HTML/CSS site using Claude (claude.ai) as a development partner — no frameworks, no build tools, no monthly hosting fees. Hosted free on GitHub Pages.

## How it was built

This site was "vibe coded" — a conversational build process where professional content, design preferences, and copy were developed through dialogue with Claude, which generated the finished HTML and CSS files. The result is a fully custom site without templates or drag-and-drop builders.

Full write-up: [How I Built a Professional Website for Free](https://www.scottcurtner.com/article-1.html)

## Structure

```
scottcurtner-website/
├── index.html        # Main site (home, about, experience, credentials, writing, contact)
├── article-1.html    # Article: How I Built a Professional Website for Free
└── README.md         # This file
```

## Stack

- Pure HTML5 and CSS3 — no JavaScript frameworks
- [DM Serif Display + DM Sans](https://fonts.google.com/) via Google Fonts
- Hosted on [GitHub Pages](https://pages.github.com/) (free)
- Domain managed at [Network Solutions](https://www.networksolutions.com/)
- HTTPS enforced via GitHub's free SSL certificate

## DNS setup (for reference)

For anyone pointing a Network Solutions domain to GitHub Pages — you need:

| Type  | Name | Value                   |
|-------|------|-------------------------|
| A     | @    | 185.199.108.153         |
| A     | @    | 185.199.109.153         |
| A     | @    | 185.199.110.153         |
| A     | @    | 185.199.111.153         |
| CNAME | www  | stonemonk2.github.io    |

**Note:** Network Solutions blocks replacing the default WWW A record via self-service UI. You must contact their support chat to convert it to a CNAME. See article-1.html for the full story.

## Author

**Scott Curtner, CIA, CISA, MCSE, ITIL**
Technology Audit Manager · San Francisco Bay Area

- Website: [scottcurtner.com](https://www.scottcurtner.com)
- LinkedIn: [linkedin.com/in/scottcurtner](https://www.linkedin.com/in/scottcurtner/)

---

*Part of a content series: "What happens when a technology auditor goes deep on AI tools."*
