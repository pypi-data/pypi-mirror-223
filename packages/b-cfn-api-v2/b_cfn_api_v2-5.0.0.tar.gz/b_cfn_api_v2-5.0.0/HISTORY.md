# Release history

### 5.0.0
* Upgrade CDK support from v1 to v2.
* Upgrade GitHub pipelines checkout version from v2 to v3.
* Set GitHub pipelines node version 18.
* Set GitHub pipelines python version 3.10.

### 4.0.0
* Fix origin paths between pure api or its cloudfront distribution.
  Both should require stage name to be entered as a part of a URL.
  This is a breaking change.

### 3.1.0
* Enable easy stage logging.

### 3.0.0
* Upgrade breaking dependencies.

### 2.0.1
* Make dependencies range more loose with maximum version not reaching `2.0.0`.

### 2.0.0
* Use the newest `2.0.0` custom api keys authorizer which now hashes 
api secrets and is no longer compatible with previous versions. 

### 1.1.1
* Update readme.

### 1.1.0
* Implement api keys custom authorizer (https://github.com/Biomapas/B.CfnCustomApiKeyAuthorizer).

### 1.0.0
* Fully documented, tested, and working version release.

### 0.0.1
* Initial build. 
