from auslib.util.rulematching import matchRegex


def serialize_signoff_requirements(requirements):
    dct = {}
    for rs in requirements:
        signoffs_required = max(dct.get(rs["role"], 0), rs["signoffs_required"])
        dct[rs["role"]] = signoffs_required

    return dct


def get_required_signoffs_for_product_channel(product, channel, product_rs_by_product, all_product_rs):
    """Get required signoffs for a (product, channel) pair.

    Channel supports globbing, so we must take that into account before deciding
    whether or not a signoff requirement is a match.
    """
    source = product_rs_by_product.get(product, []) if product else all_product_rs
    return [rs for rs in source if not channel or matchRegex(channel, rs["channel"])]
