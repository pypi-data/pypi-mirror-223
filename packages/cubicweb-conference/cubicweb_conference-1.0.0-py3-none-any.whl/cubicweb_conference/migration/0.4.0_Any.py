# Sponsor migration

add_entity_type("SponsorShip", auto=True, commit=True)

rset = rql("Any S WHERE S is Sponsor")

sp_hash = {}
for sponsor in rset.entities():
    key = (sponsor.level, tuple(sponsor.supports_conf))
    sp_hash.setdefault(key, []).append(sponsor)

urql = session.unsafe_execute

for (level, confs), sponsors in sp_hash.items():
    sponsors_eid = ",".join(str(i.eid) for i in sp_hash[key])
    confs_eid = ",".join([str(i.eid) for i in confs])
    rset = urql(
        "INSERT SponsorShip X: X level %(level)s, X title %(title)s",
        {"level": level, "title": "automatic title"},
    )
    sponsorship = rset.get_entity(0, 0)
    urql(
        f"SET X sponsoring_conf Y WHERE X eid {sponsorship.eid}, Y eid IN {confs_eid})"
    )
    urql(f"SET X is_sponsor Y WHERE X eid IN ({sponsors_eid}), Y eid {sponsorship.eid}")

drop_attribute("Sponsor", "level", commit=True)
drop_relation_definition("Sponsor", "supports_conf", "Conference", commit=True)

commit()
