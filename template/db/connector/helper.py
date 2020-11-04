_ALLOW_UPDATE_OPS = {
    "$inc",
    "$min",
    "$set",
    "$setOnInsert",
    "$unset",
    "$addToSet",
    "$pop",
    "$pull",
    "$push",
    "$pullAll",
}


def hasUpdateOps(update_ops):
    if not isinstance(update_ops, dict):
        return False
    if any(k not in _ALLOW_UPDATE_OPS for k in update_ops):
        return False
    return True
