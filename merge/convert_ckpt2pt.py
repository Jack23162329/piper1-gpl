# convert checkpoints file into pure .pt file.
import sys, pathlib, torch
torch.serialization.add_safe_globals([pathlib.PosixPath]) # if trusting the source :) 
src = sys.argv[1]
dst = sys.argv[2] if len(sys.argv) > 2 else src.replace(".ckpt","-weights.pt")
obj = torch.load(src, map_location="cpu", weights_only=False)
state = obj.get("state_dict", obj)
torch.save(state, dst)
print("wrote:", dst)
