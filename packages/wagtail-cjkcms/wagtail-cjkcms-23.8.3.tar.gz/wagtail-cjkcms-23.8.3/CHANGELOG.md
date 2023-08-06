# 0.1.1 (2022-08-14)

- Updated the README.md

# 0.1.2 (2022-08-14)

- Updated the README.md

# 0.1.3 (2022-08-15)

- added config for mkdocs
- moved docs folder one level up
- started basic documentation and updated readme
- updated pyproject.toml and added requirements to setup.cfg

# 0.1.4 (2022-08-15)

- fixed broken docs links in readme

# 0.1.5 (2022-08-15)

- fixed missing folders in the install package (modified manifest file)

# 0.1.6 (2022-08-25)

- Added import of `BaseBlock` to cjkcms.blocks for compatibility with other apps using the block
- Fixed missing InlinePanel allowing choosing default site navbar in Settings -> Layout
- Removed models/cms_models_legacy.py as it was crashing doctests due to duplicate model names
- extracted get_panels() method from Cjkcmspage get_edit_handler() to simplify overriding admin panels in subclasses. (as per suggestion of @FilipWozniak)

# 0.1.7 (2022-08-27)

- Added missing InlinePanel allowing choosing footers for the website in Settings -> Layout

# 0.1.8 (2022-08-27)

- Fixed missing search template in CjkcmsMeta (for backward compatibility)
- Fixed broken Advanced Settings in admin panel (hooks adding js/css were missing)

# 0.1.9.x (2022-09-01)

- Fixed broken get_panels() call preventing display of body panels in backend editor
- Removed useless debug/print entries in page_models

# 0.2.0 (2022-09-03)

- NON-COMPATIBLE with Wagtail<4.0!
- Added missing attribute `use_json_field=True` in StreamField in several models - new migration.
- Removed unused block ada_skip in base page template.

# 0.2.1 (2022-09-03)

- Changed dependencies wagtail-seo i wagtail-cache to forked versions, which allow Wagtail 4.0.

# 0.2.2 (2022-09-03)

- Added cms_models to models/\_init\_\_.py, as they are already part of migration 0001, so they are not optional. Updated docs to reflect this.

# 0.2.3 (2022-09-06)

- Added label_format attribute for all content and layout blocks, to ensure correct display in collapsed admin view
- Added new test for article index / article page

# 0.2.4 (2022-09-07)

- Added new test to verify fixing a bug with ArticleIndexPage (details below)
- Fixed bug in ArticleIndexPage which prevented creation of an ArticleIndexPage under WebPage
- Fixed a broken test in test_articlepages introduced in 0.2.3.

# 0.2.5 (2022-09-07)

- Added a management command: init-website (replaces default HP with a custom, cms based one)
- Added a management command: init-navbar (adds a new Navbar and sets it as default for the website)

# 0.2.6 (2022-09-14)

- Added flags show_covers, show_dates and show_authors to the LatestPages block and its' templates

# 0.2.7 (2022-10-09)

- Fixed image formatting options in the RichtextBlock, to work with Bootstrap5.
- Registered new image formats: left-thumb and right-thumb
- Introduced CI with CircleCI: flake8, codespell and unit tests

# 0.2.8 (2022-11-05)

- Added default_card_template to CardGrid to allow overriding default card template in a whole CardGrid
- Restored pypi requirements for wagtail-seo and wagtail-cache

# 0.2.8.1 (2022-11-06)

- Restored an aliast to SearchableHTMLBlock in cjkcms.blocks.searchable_html_blocks for backward compatibility

# 0.2.8.2 (2022-11-10)

- Fixed broken card template file name in settings.py

# 22.11.1 (2022-11-12)

- Renamed package to wagtail-cjkcms
- Changed versioning to calendar versioning (YY.MM.X)

# 22.11.2 (2022-11-27)

- Added two new quote styles and fixed formatting for the default quote template
- Added LayoutSettings to control default visibility of article author and publication date
- Removed unneeded stuff from testproject
- Updated setup configuration and gitignore. Added tox.ini config.
- Fixed broken reference to default image in card_landing\* templates. Fixed accordion to work with B5 and MDB5.

# 22.11.3 (2022-11-30)

- Added new templatetag library (auth_extras) with a filter has_group to check if a user is in a group

# 22.11.4 (2022-11-30)

- Added custom handler for external links in RichText - any external link ending with ?\_blank will open in a new tab
- Added missing static file (quote.svg)

# 22.11.5 (2022-11-30)

- Added responsive embeds CSS to work with WAGTAILEMBEDS_RESPONSIVE_HTML = True setting.
- Fixed quote_block_leftbar malformed tag.
- Fixed broken .gitignore which was blockig any images subfolder, while it should only ignore /images/ folder in the root of the repository.

# 23.1.1 (2023-01-28)

- Updated MDB and Bootstrap (CDN) libs to most recent.
- Updated FontAwesome (CDN) to v6.
- Added custom font in layout settings with default Roboto.
- Updated card_landing2.html style to something usable. It requires two images, and uses page cover_image as one of backgrounds

# 23.1.2 (2023-01-28)

- Added filtering image gallery by tag, previously was only by collection

# 23.2.1 (2023-02-04)

- Added title and show_navigation to PageListBlock. It is currently used only in TOC template
- Removed required parent page in PageListBlock - now defaults to self.parent 
- Changed default num_posts in PageListBlock to 10
- Added new template (TOC) to PageListBlock, with tracking of current/prev/next

# 23.2.2 (2023-02-11)
- Updated imports to get rid of deprecation warnings
- Fixed exception in search results containing page with PageListBlock with implicit parent page
- Changed PriceListItem description to RichTextBlock and adjusted template accordingly

# 23.2.3 (2023-02-20)
- Added simple implementation of cookie consent using https://github.com/orestbida/cookieconsent
- Added simple templatetag to display current year: {{ current_year }}

# 23.2.4 (2023-02-22)
- Added .modal max-width: none to avoid problems with centering images in modals, both in Bootstrap and MDBootstrap
- Fixed carousel prev/next not working with MDB & Plain Bootstrap 5.

# 23.2.5 (2023-02-23)
- Google analytics script fix to respect cookie consent.
- Fixed broken link tracking script.
- Removed unnecessary requirement re: wagtail 4.2 from migration 0006

# 23.2.6 (2023-02-23)
- Fixed problem with migration broken by 23.2.5

# 23.3.1 (2023-03-12)
- Added "cjkcms start [projectname]" command to create a new project with wagtail-cjkcms installed

# 23.4.1 (2023-04-16)
- Added new layout setting (bootstrap_icon) + static files to load Bootstrap icons css+woff locally.
- Modified frontend_assets template to load bootstrap icons if set.

# 23.4.2 (2023-04-20)
- Fixed problem of request context missing in can_show_item templatetag by adding try/except block.

# 23.4.3 (2023-04-25)
- Add possibility to choose between menu dropdown and bottom corner language selectors.

# 23.5.1 (2023-05-21)
- Fixed regression from previous update, where change of langue chooser setting from Boolean to Char caused missing template crash if applied to existing project with Boolean value of True. Now all previous values will be changed to None upon migration.

# 23.6.1 (2023-05-31)
- Basic compatibility with Wagtail 5.0
- Due to wagtail-seo and wagtail-cache not being compatible with Wagtail 5.0, they were replaced with forked versions downloadable from github. This is a temporary solution until the original packages are updated.

# 23.6.2 (2023-06-05)
- Added new project template with webpack support (untested as of yet)
- Modified the navbar model to support multilingual websites: new column "language" allows setting navbar
visibility to all languages or just one selected.

# 23.7.1 (2023-07-02)
- Split requirements into prod and dev
- Classifier bug fixes copied from codered #51d8838
- Implemented filmstrip block as per codered #849f1f4
- Implemented related pages feature as per codered #a130c53;
- Added ButtonLink title in collapsed view

# 23.7.2 (2023-07-03)
- Fixed leftover {{ page }} in base.html

# 23.7.4 (2023-07-03)
- Removed Universal Google Analytics
- Added support for Matomo Analytics

# 23.8.1 (2023-08-02)
- Break down matomo tracking code snippet into two, moving the "noscript" section to the bottom of html file
- Add instructions for using pytest excluding the project_template folder

# 23.8.2 (2023-08-05)
 - Removed previously under construction Navbar Social Media link item. Replaced with a location field added to SocialMediaSettings, with four locations: none, inside menu bar, float left, and float right. Requires loading font awesome icons in settings -> layout.

# 23.8.3 (2023-08-06)
 - Fixed error in social media template twitter link. Added target _blank to all social media links.