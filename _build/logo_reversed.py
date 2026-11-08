"""Retired. The horizontal logos (and every other logo) now come from brand_set.py,
which builds the whole set from brand/rosas-logo-primary.svg."""
import runpy, os
runpy.run_path(os.path.join(os.path.dirname(os.path.abspath(__file__)), "brand_set.py"), run_name="__main__")
