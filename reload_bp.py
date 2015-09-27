import reload_bpschema

print "If error occures, check if backpack.tf is online."
bpkey = raw_input("Enter bp api key:")
reload_bpschema.reload( bpkey )