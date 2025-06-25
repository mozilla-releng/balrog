def serialize_signoff_requirements(requirements):
    dct = {}
    for rs in requirements:
        signoff_verifier = "role" if "role" in rs else "permission"
        signoffs_required = max(dct.get(rs[signoff_verifier], 0), rs["signoffs_required"])
        dct[rs[signoff_verifier]] = signoffs_required

    return dct
