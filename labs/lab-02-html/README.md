# CSE 472 Lab Report 02 - HTML Fundamentals and Structured Webpage Development

## Assignment
**SEU Tech Event Information and Registration Page**

This folder contains the complete CSE 472 Lab 02 submission. The project is a responsive single-page HTML website that demonstrates HTML5 document structure, semantic elements, links, images, lists, a table, and a registration form with browser-side validation.

## Student Information
- **Name:** Jannatul Tuna Trisha
- **Student ID:** 2023200000664
- **Section:** 01
- **Semester:** 9th
- **Department:** Computer Science and Engineering
- **University:** Southeast University
- **Course:** CSE 472 - Web and Internet Programming Lab
- **Instructor:** Abid Ahmad
- **Submission Date:** 8 September 2026

## Features Implemented
- Proper HTML5 skeleton with UTF-8 and responsive viewport metadata
- Semantic `header`, `nav`, `main`, `section`, and `footer` layout
- Exactly one main `h1` with a clear heading hierarchy
- Internal navigation links and a safe external university link
- Responsive local event banner with meaningful alternative text
- Meaningful `div` and `span` usage
- Unordered, ordered, and correctly nested lists
- Event schedule table with caption, header row, and four data rows
- Registration form containing full name, student ID, email, preferred date, radio buttons, checkboxes, submit, and reset controls
- Matching form labels and input IDs
- `required`, `minlength`, `maxlength`, `value`, `placeholder`, `name`, and related form attributes where appropriate
- Static-form notice and prevented submission because no backend is part of this HTML lab
- External CSS with responsive layout, focus states, table styling, form styling, and mobile breakpoints

## Project Structure
```text
lab-02-html/
|-- index.html
|-- style.css
|-- images/
|   `-- event-banner.jpg
|-- screenshots/
|   |-- homepage-top.png
|   |-- event-details.png
|   `-- registration-form.png
|-- report/
|   |-- lab_report_02.tex
|   `-- lab_report_02.pdf
|-- README.md
`-- CSE472_Lab_02_Complete.zip
```

## How to Run the Website
1. Download or clone the repository.
2. Open `labs/lab-02-html/`.
3. Open `index.html` in a modern browser such as Chrome, Edge, or Firefox.
4. No web server, package installation, or build step is required.

## Testing Summary
The final source was checked for HTML structure, duplicate IDs, label/input connections, CSS parsing, local file references, and required assignment elements. Chromium browser-preview testing verified CSS rendering, image rendering, internal links, external-link safety attributes, required-field validation, email validation, radio buttons, checkboxes, submit prevention, reset behavior, desktop layout, mobile layout, and console errors.

**Environment note:** Direct navigation to `localhost` and `file://` was blocked by the execution environment's browser policy. Therefore, Chromium rendered the exact final HTML and CSS through its browser-preview API with the local image embedded only for the test session. The actual source still uses the required relative paths (`style.css` and `images/event-banner.jpg`), and those paths were verified separately to exist. No browser console or page errors were observed in the browser preview.

## LaTeX Report Compilation
From the `report/` directory:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error lab_report_02.tex
```

The source uses the `listings` package, so shell escape is not required.

## Screenshot Preview
- `screenshots/homepage-top.png` - header, navigation, event introduction, and banner
- `screenshots/event-details.png` - ordered/nested lists and the complete event schedule table
- `screenshots/registration-form.png` - complete registration form and footer

## Image Source / Attribution
`images/event-banner.jpg` is an original graphic created specifically for this Lab 02 submission. It does not use an externally downloaded photograph or third-party logo, so no external image attribution is required.

## Submission Contents
The submission contains the final HTML, external CSS, local image asset, three genuine browser-rendered screenshots, LaTeX report source, compiled PDF report, this README, and the tested ZIP archive.
