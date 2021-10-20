import pubchempy as pcp

c = pcp.Compound.from_cid(241)
print(c.molecular_formula)
print(c.molecular_weight)
print(c.isomeric_smiles)
print(c.xlogp)
print(type(c.xlogp))

