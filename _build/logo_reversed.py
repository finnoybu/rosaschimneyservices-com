"""Writes the horizontal logos (standard and cream-lettered) and the site copies."""
import os, shutil
import logo
HERE = os.path.dirname(os.path.abspath(__file__))
B = os.path.join(HERE, "..", "brand")
std = logo.horizontal()
rev = logo.horizontal(name_fill="#F6EBDD", sub_fill="#E3A85C", rule_fill="#E07A2E")
for d in ("2", "3"):
    open(os.path.join(B, d, "rosas-logo-horizontal.svg"), "w").write(std)
open(os.path.join(B, "3", "rosas-logo-horizontal-reversed.svg"), "w").write(rev)
shutil.copy(os.path.join(B, "3", "rosas-logo-horizontal-reversed.svg"), os.path.join(HERE, "..", "assets", "img", "logo-horizontal-light.svg"))
print("done")
