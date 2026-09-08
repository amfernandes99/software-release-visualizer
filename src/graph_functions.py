def set_release_relationships(releases):
    for release in releases:
        release.children = []

    for release in releases:
        if release.parent_id:
            for possible_parent in releases:
                if possible_parent.release_id == release.parent_id:
                    possible_parent.children.append(release)
                    break
