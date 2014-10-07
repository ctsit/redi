Code Review Checklist
=====================

When reviewing a pull request there are many quality checks we could
perform. This document can serve as a guide for tests we can apply to
assess the quality of the work.

-  Is the pull request against the right branch? Changes without
   dependencies should be forked from the head of the ***master*** and
   merged back to ***develop***. Changes with dependencies should fork
   from and merge back to a non-production branch, generally
   ***develop***.
-  Does the pull request contain one and only one thing be it a new
   feature, bug fix, refactor, etc. ?
-  Do the commit(s) in the request describe the work?
-  Does the pull request comment describe the work?
-  Does the pull request pass the Travis tests?
-  Do new tests accompany any new code?
-  If this is a bug fix, is a test added to test for that bug?
-  If this is a new feature, is it documented?
-  Does the new code improve or maintain the lint score?
-  Does the new code improve or maintain the code coverage score?
-  If the new code contains changes that would break existing
   installations (e.g. database schema, configuration file changes),
   does it also contain relevant documentation of the change? Does it
   have a migration procedure? Does it have a migration tool?
-  Does the merged code pass an integration test?

