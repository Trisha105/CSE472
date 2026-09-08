# Actual browser and source test results

Browser: Chromium 143.0.7499.4. Delivery: real local HTTP server.

Summary: {'PASS': 33}

| ID | Check | Expected | Actual | Status |
|---|---|---|---|---|
| T01 | HTML5 structure and nesting | HTML5, metadata and balanced tags | Unclosed tags: 0; nesting errors: 0 | PASS |
| T02 | Semantic structure | One h1; at least three sections; all landmarks | 1 main heading; 5 sections | PASS |
| T03 | IDs and labels | Unique IDs and connected labels for every input | 21 IDs; 9 explicitly labelled inputs | PASS |
| T04 | Lists | Ordered, unordered and correctly nested lists | 3 nested lists inside parent list items | PASS |
| T05 | Schedule table | Caption, five headings and four consistent data rows | 5 headings; 4 data rows | PASS |
| T06 | Local file references | All linked local resources exist | 4 references; missing: [] | PASS |
| T07 | CSS syntax | No CSS parser errors | 241 declarations; 0 errors | PASS |
| T08 | Helper syntax | Node syntax check succeeds | Exit code 0 | PASS |
| T09 | Rendered image and styling | Image loaded and CSS declarations supported | Image loaded: True; unsupported declarations: 0 | PASS |
| T10 | Internal navigation | Every link reaches its target | 8 links checked; 0 failures | PASS |
| T11 | External link attributes | HTTPS, new tab and safe relationship attributes | 2 external links checked | PASS |
| T12 | Live external destination | HTML standard loads successfully | HTTP 200 | PASS |
| T13 | Required fields | Empty form rejected and first required field focused | Valid: False; focus: fullname | PASS |
| T14 | Name minimum length | Two-character name rejected | tooShort: True | PASS |
| T15 | Student ID limits | Letters rejected; maximum fifteen digits | Letter mismatch: True; capped length: 15 | PASS |
| T16 | Email validation | Malformed email rejected | typeMismatch: True | PASS |
| T17 | Date boundaries | Only 15 and 16 October accepted | 14, 15, 16, 17 October valid: [False, True, True, False] | PASS |
| T18 | Radio group | Exactly one participation type selected | Exclusive: True | PASS |
| T19 | Checkbox choices | Two topics can be selected independently | Selected topics: 2 | PASS |
| T20 | Valid demo submission | Local confirmation; no request or navigation | Confirmation: True; new requests: 0 | PASS |
| T21 | Enter-key submission | Enter uses the same safe handler | Unchanged URL: True; new requests: 0 | PASS |
| T22 | Reset button | All fields and selections return to defaults | All controls reset: True | PASS |
| T23 | Label interaction | Labels focus or toggle the corresponding input | Text focus: True; checkbox selected: True | PASS |
| T24 | Keyboard focus | Tab gives a visible three-pixel focus outline | 3px solid | PASS |
| T25 | Responsive layout at 1200px | No horizontal document overflow | Document width: 1200px; viewport: 1200px | PASS |
| T26 | Responsive layout at 820px | No horizontal document overflow | Document width: 820px; viewport: 820px | PASS |
| T27 | Responsive layout at 390px | No horizontal document overflow | Document width: 390px; viewport: 390px | PASS |
| T28 | Responsive layout at 320px | No horizontal document overflow | Document width: 320px; viewport: 320px | PASS |
| T29 | Mobile table scrolling | Wide table scrolls inside its own region | Horizontal offset: 100px | PASS |
| T30 | Reduced motion | Reduced-motion preference disables smooth scrolling | scroll-behavior: auto | PASS |
| T31 | No-JavaScript safety | Submit disabled; Enter sends no information | Disabled: True; new requests: 0; unchanged URL: True | PASS |
| T32 | Console and page errors | No avoidable errors on the implemented page | Errors recorded: 0 | PASS |
| T33 | Real resource loading | HTML, CSS, helper and SVG load through HTTP | All four resources returned HTTP 200: True | PASS |
