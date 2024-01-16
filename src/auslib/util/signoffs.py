def serialize_signoff_requirements(requirements):
    dct = {}
    for rs in requirements:
        signoff_check = "role" if "role" in rs else "permission"
        signoffs_required = max(dct.get(rs[signoff_check], 0), rs["signoffs_required"])
        dct[rs[signoff_check]] = signoffs_required

    return dct
