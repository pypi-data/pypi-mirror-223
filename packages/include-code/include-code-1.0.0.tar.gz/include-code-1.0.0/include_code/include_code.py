#!/usr/bin/env python3
import panflute as pf
import sys
from .common import Valid, Error

from .validate import is_url_valid
from .fetch import fetch

__version__ = "1.0.0"

def include_code(cb: pf.CodeBlock):
    # replace the content of the code with the fetched
    # raw file
    url = cb.text
    validators = [
        is_url_valid
    ]
    for n, validator in enumerate(validators):
        validation_result = validator(url)
        if(type(validation_result) is not Valid):
            validation_errors = validation_result
            sys.stderr.write(str(validation_errors))
            sys.stderr.write(f"[ERROR][URL VALIDATION]: in validating {url} with {n} validator \n")
            for i, validation_error in enumerate(validation_errors):
                error_text = validation_error.text
                sys.stderr.write(f"[ERROR][VALIDATION ERROR {i}]: {error_text} \n")
            sys.exit(1)
    
    fetch_result = fetch(url)
    if(type(fetch_result) is Error):
        error_text = fetch_result.text
        sys.stderr.write(f"[ERROR][URL FETCHING]: in fetching {url} \n")
        sys.stderr.write(f"[ERROR][URL FETCHING]: {error_text} \n")
        sys.exit(2)
    
    file_contents = fetch_result
    cb.text = file_contents

def action(elem, doc):
    # The name of the class that has to be specified
    # in the code block in order for the content of the block
    # to be interpreted as url and fetched
    class_name = "code-include"

    if (type(elem) == pf.CodeBlock):
        if(class_name in elem.classes):
            include_code(elem)            
            # remove the classes from the code options
            # for the next filters
            elem.classes.remove(class_name)

def main():
    pf.run_filter(action, doc=None)

if __name__ == "__main__":
    main()