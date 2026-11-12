SITE DESIGNER ONLY
==================
Everything in this _build folder is the site designer's (Ken Tannenbaum's) toolkit.
None of it is needed to host or edit the live website, and none of it is included
in the files handed to Rosas Chimney Services.

  build.py, areas.py, extra_pages.py, icons.py   generate every page of the site
  es_i18n.py, es_strings_1.py, es_strings_2.py   build the Spanish (/es/) pages
  brand_set.py                                   builds the logo set from brand/rosas-logo-primary.svg
  logo.py, logo_reversed.py, trace_emblem.py     retired logo tools, kept for reference
  publish-to-github.bat                          DEMO SITE ONLY: publishes the github.io preview

IMPORTANT: once the owners start editing their own copy of the site, running
build.py here would produce pages WITHOUT their edits. Pull their current files
from their GitLab repository before making any further changes.
