# Changelog

## [Unreleased](https://github.com/paul-florentin-charles/bcn-rainfall-models/tree/HEAD)

[Full Changelog](https://github.com/paul-florentin-charles/bcn-rainfall-models/compare/v.0.4.0-webapp...HEAD)

**Closed issues:**

- Simplify code architecture by merging some files [\#93](https://github.com/paul-florentin-charles/bcn-rainfall-models/issues/93)
- Think about setting up a project management tool [\#88](https://github.com/paul-florentin-charles/bcn-rainfall-models/issues/88)
- Migrate Pandas to FireDucks [\#84](https://github.com/paul-florentin-charles/bcn-rainfall-models/issues/84)
- Build a basic front communicating with FastAPI [\#79](https://github.com/paul-florentin-charles/bcn-rainfall-models/issues/79)

**Merged pull requests:**

- A lot of changes, too lazy to sum it up [\#96](https://github.com/paul-florentin-charles/bcn-rainfall-models/pull/96) ([paul-florentin-charles](https://github.com/paul-florentin-charles))
- Solving squash commit diff issue between main/dev branches [\#95](https://github.com/paul-florentin-charles/bcn-rainfall-models/pull/95) ([paul-florentin-charles](https://github.com/paul-florentin-charles))
- Use uv to manage dependencies [\#94](https://github.com/paul-florentin-charles/bcn-rainfall-models/pull/94) ([paul-florentin-charles](https://github.com/paul-florentin-charles))
- Added generated CHANGELOG.md [\#92](https://github.com/paul-florentin-charles/bcn-rainfall-models/pull/92) ([paul-florentin-charles](https://github.com/paul-florentin-charles))
- Commit and push CHANGELOG.md generated file within workflow [\#91](https://github.com/paul-florentin-charles/bcn-rainfall-models/pull/91) ([paul-florentin-charles](https://github.com/paul-florentin-charles))
- Push GitHub Action "Generate changelog" on releases \(version v2.4\) [\#89](https://github.com/paul-florentin-charles/bcn-rainfall-models/pull/89) ([paul-florentin-charles](https://github.com/paul-florentin-charles))

## [v.0.4.0-webapp](https://github.com/paul-florentin-charles/bcn-rainfall-models/tree/v.0.4.0-webapp) (2024-12-09)

[Full Changelog](https://github.com/paul-florentin-charles/bcn-rainfall-models/compare/v.0.3.0-fastapi...v.0.4.0-webapp)

**Closed issues:**

- Build an HTTP client to expose FastAPI methods for use in front [\#80](https://github.com/paul-florentin-charles/bcn-rainfall-models/issues/80)
- Compute linear regression between given year interval [\#76](https://github.com/paul-florentin-charles/bcn-rainfall-models/issues/76)
- Add from\_config class method to instantiate AllRainfall class from configuration [\#70](https://github.com/paul-florentin-charles/bcn-rainfall-models/issues/70)
- Compute standard deviation weighted by average [\#69](https://github.com/paul-florentin-charles/bcn-rainfall-models/issues/69)
- Change behaviour of get\_relative\_distance\_from\_normal class function [\#68](https://github.com/paul-florentin-charles/bcn-rainfall-models/issues/68)
- Upgrade to Python 3.12 [\#46](https://github.com/paul-florentin-charles/bcn-rainfall-models/issues/46)
- Some UTs for api module would be most appreciated [\#43](https://github.com/paul-florentin-charles/bcn-rainfall-models/issues/43)
- Experiment and integrate Plotly for rainfall data visualisation [\#40](https://github.com/paul-florentin-charles/bcn-rainfall-models/issues/40)
- Allow CSV export between specific dates [\#36](https://github.com/paul-florentin-charles/bcn-rainfall-models/issues/36)

**Merged pull requests:**

- Code removal | Matplotlib -\> Plotly migration | Improve Webapp [\#87](https://github.com/paul-florentin-charles/bcn-rainfall-models/pull/87) ([paul-florentin-charles](https://github.com/paul-florentin-charles))
- Much stuff going on [\#86](https://github.com/paul-florentin-charles/bcn-rainfall-models/pull/86) ([paul-florentin-charles](https://github.com/paul-florentin-charles))
- More routes in client, more fun in webapp [\#85](https://github.com/paul-florentin-charles/bcn-rainfall-models/pull/85) ([paul-florentin-charles](https://github.com/paul-florentin-charles))
- New route exposed by API client & having fun with the front prototype [\#83](https://github.com/paul-florentin-charles/bcn-rainfall-models/pull/83) ([paul-florentin-charles](https://github.com/paul-florentin-charles))
- Dev [\#82](https://github.com/paul-florentin-charles/bcn-rainfall-models/pull/82) ([paul-florentin-charles](https://github.com/paul-florentin-charles))
- Very experimental webapp to start interacting with API [\#81](https://github.com/paul-florentin-charles/bcn-rainfall-models/pull/81) ([paul-florentin-charles](https://github.com/paul-florentin-charles))
- New API route | Rainfall precision from 2 to 1 decimal [\#78](https://github.com/paul-florentin-charles/bcn-rainfall-models/pull/78) ([paul-florentin-charles](https://github.com/paul-florentin-charles))
- Some improvements... [\#77](https://github.com/paul-florentin-charles/bcn-rainfall-models/pull/77) ([paul-florentin-charles](https://github.com/paul-florentin-charles))
- Some more API routes [\#75](https://github.com/paul-florentin-charles/bcn-rainfall-models/pull/75) ([paul-florentin-charles](https://github.com/paul-florentin-charles))
- Use pandas mean\(\) | Fix mypy pipeline | Add 2 new API routes [\#74](https://github.com/paul-florentin-charles/bcn-rainfall-models/pull/74) ([paul-florentin-charles](https://github.com/paul-florentin-charles))
- Update README.md [\#73](https://github.com/paul-florentin-charles/bcn-rainfall-models/pull/73) ([paul-florentin-charles](https://github.com/paul-florentin-charles))
- Python 3.12 [\#72](https://github.com/paul-florentin-charles/bcn-rainfall-models/pull/72) ([paul-florentin-charles](https://github.com/paul-florentin-charles))

## [v.0.3.0-fastapi](https://github.com/paul-florentin-charles/bcn-rainfall-models/tree/v.0.3.0-fastapi) (2024-08-15)

[Full Changelog](https://github.com/paul-florentin-charles/bcn-rainfall-models/compare/v0.2.0-alpha...v.0.3.0-fastapi)

**Closed issues:**

- Modify Month/Season enums to take string values instead of integers [\#67](https://github.com/paul-florentin-charles/bcn-rainfall-models/issues/67)
- Flasgger -\> FastAPI [\#57](https://github.com/paul-florentin-charles/bcn-rainfall-models/issues/57)

**Merged pull requests:**

- FastAPI migration DONE [\#71](https://github.com/paul-florentin-charles/bcn-rainfall-models/pull/71) ([paul-florentin-charles](https://github.com/paul-florentin-charles))
- Dev [\#66](https://github.com/paul-florentin-charles/bcn-rainfall-models/pull/66) ([paul-florentin-charles](https://github.com/paul-florentin-charles))
- Use python built-ins type hints instead of typing lib [\#65](https://github.com/paul-florentin-charles/bcn-rainfall-models/pull/65) ([paul-florentin-charles](https://github.com/paul-florentin-charles))
- Dev [\#63](https://github.com/paul-florentin-charles/bcn-rainfall-models/pull/63) ([paul-florentin-charles](https://github.com/paul-florentin-charles))
- Fix missing parameters for seasonal averages plot API route [\#62](https://github.com/paul-florentin-charles/bcn-rainfall-models/pull/62) ([paul-florentin-charles](https://github.com/paul-florentin-charles))
- Add begin/end year to average plots [\#61](https://github.com/paul-florentin-charles/bcn-rainfall-models/pull/61) ([paul-florentin-charles](https://github.com/paul-florentin-charles))
- Fix MyPy issues [\#60](https://github.com/paul-florentin-charles/bcn-rainfall-models/pull/60) ([paul-florentin-charles](https://github.com/paul-florentin-charles))

## [v0.2.0-alpha](https://github.com/paul-florentin-charles/bcn-rainfall-models/tree/v0.2.0-alpha) (2024-02-04)

[Full Changelog](https://github.com/paul-florentin-charles/bcn-rainfall-models/compare/v0.1.0-alpha...v0.2.0-alpha)

**Implemented enhancements:**

- Build a small API prototype [\#5](https://github.com/paul-florentin-charles/bcn-rainfall-models/issues/5)

**Closed issues:**

- Better path management using Pathlib or/and os [\#58](https://github.com/paul-florentin-charles/bcn-rainfall-models/issues/58)

**Merged pull requests:**

- Dev [\#59](https://github.com/paul-florentin-charles/bcn-rainfall-models/pull/59) ([paul-florentin-charles](https://github.com/paul-florentin-charles))
- Dev [\#56](https://github.com/paul-florentin-charles/bcn-rainfall-models/pull/56) ([paul-florentin-charles](https://github.com/paul-florentin-charles))
- Dev [\#54](https://github.com/paul-florentin-charles/bcn-rainfall-models/pull/54) ([paul-florentin-charles](https://github.com/paul-florentin-charles))
- Dev [\#52](https://github.com/paul-florentin-charles/bcn-rainfall-models/pull/52) ([paul-florentin-charles](https://github.com/paul-florentin-charles))
- Dev [\#51](https://github.com/paul-florentin-charles/bcn-rainfall-models/pull/51) ([paul-florentin-charles](https://github.com/paul-florentin-charles))
- Dev [\#50](https://github.com/paul-florentin-charles/bcn-rainfall-models/pull/50) ([paul-florentin-charles](https://github.com/paul-florentin-charles))

## [v0.1.0-alpha](https://github.com/paul-florentin-charles/bcn-rainfall-models/tree/v0.1.0-alpha) (2023-11-29)

[Full Changelog](https://github.com/paul-florentin-charles/bcn-rainfall-models/compare/3b8de199a7a0021a97b612e88ac4a870b69a6018...v0.1.0-alpha)

**Implemented enhancements:**

- Generic function for computing number of years above or under a specific rainfall value [\#12](https://github.com/paul-florentin-charles/bcn-rainfall-models/issues/12)
- Compute dispersion of data [\#6](https://github.com/paul-florentin-charles/bcn-rainfall-models/issues/6)

**Closed issues:**

- Manage API errors [\#44](https://github.com/paul-florentin-charles/bcn-rainfall-models/issues/44)
- Switch linter from Pylint to Ruff [\#41](https://github.com/paul-florentin-charles/bcn-rainfall-models/issues/41)
- Convert Yaml Swagger Spec files to Python dicts [\#31](https://github.com/paul-florentin-charles/bcn-rainfall-models/issues/31)
- Try to reduce the amount of optional parameters in functions/routes [\#29](https://github.com/paul-florentin-charles/bcn-rainfall-models/issues/29)
- Use marshmallow for API models and/or query parameters [\#25](https://github.com/paul-florentin-charles/bcn-rainfall-models/issues/25)
- Find another way to load all rainfall data to increase perf [\#23](https://github.com/paul-florentin-charles/bcn-rainfall-models/issues/23)
- Use swagger basePath config key for Flask API routes [\#22](https://github.com/paul-florentin-charles/bcn-rainfall-models/issues/22)
- Implement export to csv procedure for AllRainfall class [\#20](https://github.com/paul-florentin-charles/bcn-rainfall-models/issues/20)
- Reshape project file tree [\#19](https://github.com/paul-florentin-charles/bcn-rainfall-models/issues/19)
- Make a generic plot function [\#11](https://github.com/paul-florentin-charles/bcn-rainfall-models/issues/11)
- Review the way configuration works so that it is more flexible and easier to deploy [\#9](https://github.com/paul-florentin-charles/bcn-rainfall-models/issues/9)
- Unit Tests needed for classes \(YearlyRainfall & Co\) [\#7](https://github.com/paul-florentin-charles/bcn-rainfall-models/issues/7)
- Change label of y-axis when plotting rainfall normals [\#2](https://github.com/paul-florentin-charles/bcn-rainfall-models/issues/2)
- Precise Optional\[bool\] type to "show" argument in plot functions [\#1](https://github.com/paul-florentin-charles/bcn-rainfall-models/issues/1)

**Merged pull requests:**

- Dev [\#49](https://github.com/paul-florentin-charles/bcn-rainfall-models/pull/49) ([paul-florentin-charles](https://github.com/paul-florentin-charles))
- Dev [\#48](https://github.com/paul-florentin-charles/bcn-rainfall-models/pull/48) ([paul-florentin-charles](https://github.com/paul-florentin-charles))
- Renamed tags & removed array for "produces" key in swagger route specs [\#45](https://github.com/paul-florentin-charles/bcn-rainfall-models/pull/45) ([paul-florentin-charles](https://github.com/paul-florentin-charles))
- New linter! Ruff baby [\#42](https://github.com/paul-florentin-charles/bcn-rainfall-models/pull/42) ([paul-florentin-charles](https://github.com/paul-florentin-charles))
- Dev [\#37](https://github.com/paul-florentin-charles/bcn-rainfall-models/pull/37) ([paul-florentin-charles](https://github.com/paul-florentin-charles))
- Dev [\#35](https://github.com/paul-florentin-charles/bcn-rainfall-models/pull/35) ([paul-florentin-charles](https://github.com/paul-florentin-charles))
- Big fat MR [\#34](https://github.com/paul-florentin-charles/bcn-rainfall-models/pull/34) ([paul-florentin-charles](https://github.com/paul-florentin-charles))
- Implemented Marshmallow Schemas amidst other things [\#33](https://github.com/paul-florentin-charles/bcn-rainfall-models/pull/33) ([paul-florentin-charles](https://github.com/paul-florentin-charles))
- Swagger specs converted from YAML to Python dicts [\#32](https://github.com/paul-florentin-charles/bcn-rainfall-models/pull/32) ([paul-florentin-charles](https://github.com/paul-florentin-charles))
- Dev [\#30](https://github.com/paul-florentin-charles/bcn-rainfall-models/pull/30) ([paul-florentin-charles](https://github.com/paul-florentin-charles))
- Dev [\#28](https://github.com/paul-florentin-charles/bcn-rainfall-models/pull/28) ([paul-florentin-charles](https://github.com/paul-florentin-charles))
- Dev [\#27](https://github.com/paul-florentin-charles/bcn-rainfall-models/pull/27) ([paul-florentin-charles](https://github.com/paul-florentin-charles))
- Dev [\#26](https://github.com/paul-florentin-charles/bcn-rainfall-models/pull/26) ([paul-florentin-charles](https://github.com/paul-florentin-charles))
- Dev [\#24](https://github.com/paul-florentin-charles/bcn-rainfall-models/pull/24) ([paul-florentin-charles](https://github.com/paul-florentin-charles))
- Dev [\#21](https://github.com/paul-florentin-charles/bcn-rainfall-models/pull/21) ([paul-florentin-charles](https://github.com/paul-florentin-charles))
- Dev [\#18](https://github.com/paul-florentin-charles/bcn-rainfall-models/pull/18) ([paul-florentin-charles](https://github.com/paul-florentin-charles))
- Dev [\#17](https://github.com/paul-florentin-charles/bcn-rainfall-models/pull/17) ([paul-florentin-charles](https://github.com/paul-florentin-charles))
- Dev [\#16](https://github.com/paul-florentin-charles/bcn-rainfall-models/pull/16) ([paul-florentin-charles](https://github.com/paul-florentin-charles))
- First shot at setting up Flask API [\#15](https://github.com/paul-florentin-charles/bcn-rainfall-models/pull/15) ([paul-florentin-charles](https://github.com/paul-florentin-charles))
- Refactoring, docstrings & plotting [\#14](https://github.com/paul-florentin-charles/bcn-rainfall-models/pull/14) ([paul-florentin-charles](https://github.com/paul-florentin-charles))
- First intents to lighten up YearlyRainfall class by outsourcing functionalities [\#13](https://github.com/paul-florentin-charles/bcn-rainfall-models/pull/13) ([paul-florentin-charles](https://github.com/paul-florentin-charles))
- Added Unit Tests for YearlyRainfall & some modifications of config.py… [\#10](https://github.com/paul-florentin-charles/bcn-rainfall-models/pull/10) ([paul-florentin-charles](https://github.com/paul-florentin-charles))
- New functionalities for YearlyRainfall & misc. [\#8](https://github.com/paul-florentin-charles/bcn-rainfall-models/pull/8) ([paul-florentin-charles](https://github.com/paul-florentin-charles))
- New PyTest Workflow & Unit Tests improvements  [\#4](https://github.com/paul-florentin-charles/bcn-rainfall-models/pull/4) ([paul-florentin-charles](https://github.com/paul-florentin-charles))
- First batch of Unit Tests [\#3](https://github.com/paul-florentin-charles/bcn-rainfall-models/pull/3) ([paul-florentin-charles](https://github.com/paul-florentin-charles))



\* *This Changelog was automatically generated by [github_changelog_generator](https://github.com/github-changelog-generator/github-changelog-generator)*
