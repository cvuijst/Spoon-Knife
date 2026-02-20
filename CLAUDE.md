# CLAUDE.md

This file provides guidance for AI assistants working with the Spoon-Knife repository.

## Repository Overview

Spoon-Knife is GitHub's canonical demo repository, created to teach the GitHub forking workflow. It is intentionally minimal — there is no build system, no test suite, and no package manager. Its purpose is as a sandbox for practicing git operations (fork, clone, commit, pull request).

## Repository Structure

```
Spoon-Knife/
├── index.html      # Single-page HTML app with inline CSS and JavaScript
├── forkit.gif      # Animated GIF displayed by index.html (octocat image)
├── README          # One-line description of the repository
├── README2         # Secondary test file added to demonstrate additional commits
├── Test.xml        # draw.io diagram file (base64-encoded XML)
└── .project        # Eclipse IDE project descriptor (no build configuration)
```

## Key Files

### `index.html`
The only functional file in the project. It is a static HTML page that:
- Displays `forkit.gif` centered on the page
- Shows the text "Fork me? No, fork you!"
- Contains a hidden Easter egg: entering the [Konami code](https://en.wikipedia.org/wiki/Konami_Code) (`↑ ↑ ↓ ↓ ← → ← → B A`) via keyboard reveals a "Double repositories all the way across the sky!" message
- Uses inline `<style>` for layout (no external CSS framework)
- Uses inline `<script>` for the keydown event handler (no external JS library)

### `Test.xml`
A [draw.io](https://app.diagrams.net/) diagram stored in compressed XML format. It can be opened and edited at draw.io or with compatible desktop tools. It is not connected to any build pipeline.

### `.project`
An Eclipse IDE project descriptor. It declares the project name as `Spoon-Knife` and contains no build specs or natures, meaning Eclipse treats it as a generic project with no language tooling.

## Development Conventions

- **No build step**: there is nothing to compile or bundle. Edit `index.html` and open it directly in a browser.
- **No dependency manager**: there is no `package.json`, `Gemfile`, `requirements.txt`, or equivalent. Do not introduce one unless explicitly requested.
- **No test suite**: there are no automated tests. Manual browser verification is the only testing method.
- **Static files only**: all assets are served directly. Do not add server-side code unless explicitly requested.
- **Formatting**: the HTML file uses 2-space indentation with mixed tabs in the `<script>` block (matching the existing style). Preserve the existing formatting when making edits.

## Git Workflow

This repository exists specifically to demonstrate the GitHub fork-and-pull-request workflow:

1. Fork the repository on GitHub
2. Clone your fork locally
3. Create a feature branch
4. Make changes and commit
5. Push to your fork
6. Open a pull request against the upstream repository

Branch naming used by automated tooling follows the pattern `claude/<description>-<session-id>`.

## Common Tasks

### View the page locally
Open `index.html` directly in a browser — no web server required.

### Edit the page content
All HTML, CSS, and JavaScript are in `index.html`. There are no separate asset pipeline steps.

### Edit the draw.io diagram
Open `Test.xml` at [draw.io](https://app.diagrams.net/) using File > Open from > This device, or commit the file to a GitHub repository and open it with the draw.io GitHub integration.

## What Not to Do

- Do not add a build system, bundler, or task runner unless explicitly asked.
- Do not add dependencies or a package manager.
- Do not restructure the repository layout — its simplicity is intentional.
- Do not delete `forkit.gif`; it is referenced directly in `index.html`.
