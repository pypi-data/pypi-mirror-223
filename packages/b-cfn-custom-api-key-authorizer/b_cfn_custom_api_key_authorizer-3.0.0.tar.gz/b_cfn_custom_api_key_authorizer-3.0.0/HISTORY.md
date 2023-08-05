# Release history

### 3.0.0

* Upgrade CDK support from v1 to v2.
* Upgrade GitHub pipelines checkout version from v2 to v3.
* Set GitHub pipelines node version 18.
* Set GitHub pipelines python version 3.10.

### 2.3.0

* Update of `authorizer` function. Removing of sensitive information form lambda event implemented. 

### 2.2.0

* Remove unnecessary dependencies.

### 2.1.1

* Add more integration tests.
* Update README documentation.

### 2.1.0

* Add ability to specify what type of authentication strategy to use.
  Support for both `ApiKey` / `ApiSecret` and `Authorization` headers.

### 2.0.1

* Dollar sign excluded from API secret.

### 2.0.0

* Restructured project.
* All lambda functions are under `functions` directory.
* Add `deleter` function to revoke api keys.
* Add `exists` function to check whether given api key exists.
* Add `validator` function to validate api key and api secret.
* Increase the length of api key (15) and api secret (30).
* Move authentication checking logic to a lambda layer.
* Add more lambda-level logging.
* Add more integrations tests (total 11 as of now).
* **Very important security improvement** - api secrets are now hashed, to avoid
  leaks if the database is pawned. This is a standard password-level storage security.
* Greatly improve documentation.

### 1.1.0

* Create a dedicated lambda function to generate
  api keys. You should not interact with the database directly.

### 1.0.0

* Prod-ready version.
* Added documentation.
* Added more tests.
* Some code improvements.

### 0.1.0

* Initial testing done. Authorizer works.
* Need more tests and edge case handling before promoting to 1.0.0.

### 0.0.1

* Initial build.
