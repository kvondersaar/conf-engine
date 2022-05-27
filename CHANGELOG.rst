Changelog
---------

**[0.4]**
   - Fixed bug in evaluation of precedence when an option is defined in
     more than one source.
   - Fixed bug in defaults where a default of `False` would not be returned.

**[0.3]**
   - Added `default` argument to Option.  Now Options can be declared with
     a default value to be returned if the option value is not found in
     any configuration source.

**[0.2]**
   - Duplicate option exceptions are only thrown when the second
     declaration is not different from the first.

**[0.1]**
   - Initial release