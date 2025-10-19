import sys, torch, pathlib
warm = sys.argv[1]                 # our ckpt（version_0）
weights = sys.argv[2]              # pretrained .pt（pure state_dict）
out = sys.argv[3] if len(sys.argv) > 3 else "merged.ckpt" # merged it into ckpt, so that we can fit out pytorch version.

# loading complete ckpt（includes optimizer etc.）
ckpt = torch.load(warm, map_location="cpu")

# loading pretrained w&b file（pure state_dict）
pre = torch.load(weights, map_location="cpu")
if "state_dict" in pre:    # for both .ckpt/.pt
    pre = pre["state_dict"]

# trying to conver ckpt' state_dict
missing, unexpected = [], []
sd = ckpt["state_dict"]
for k, v in pre.items():
    if k in sd and sd[k].shape == v.shape:
        sd[k] = v
    else:
        if k not in sd:
            unexpected.append(k)
        else:
            missing.append((k, sd[k].shape, v.shape))

print(f"Loaded {len(pre)} keys. Replaced {len(pre)-len(unexpected)-len(missing)} keys.")
if unexpected: print(f"Unexpected keys (ignored): {len(unexpected)}")
if missing:    print(f"Shape mismatch: {len(missing)} (ignored)")

torch.save(ckpt, out)
print("Wrote:", out)

# ===============================
# CLI prompt example
# ===============================
# python merge_ckpt.py [epoch=11-step=8856.ckpt](out first few checkpoint file) [epoch=6679-step=1554200.pt](pretrained w&b .pt file) [merged.ckpt](output file :inside runs/merged)
# ===============================
# output would be like
# ===============================
# Loaded 350 keys. Replaced 342 keys.
# Unexpected keys (ignored): 2
# Shape mismatch: 6 (ignored)
# Wrote: merged.ckpt

