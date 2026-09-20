# stub pymatting (needs numba/llvmlite, blocked by app-control policy); rembg only uses it for alpha_matting=True which we don't use
import sys, types
for name in ['pymatting','pymatting.alpha','pymatting.alpha.estimate_alpha_cf','pymatting.foreground','pymatting.foreground.estimate_foreground_ml','pymatting.util','pymatting.util.util']:
    m = types.ModuleType(name); sys.modules[name] = m
sys.modules['pymatting.alpha.estimate_alpha_cf'].estimate_alpha_cf = lambda *a, **k: None
sys.modules['pymatting.foreground.estimate_foreground_ml'].estimate_foreground_ml = lambda *a, **k: None
sys.modules['pymatting.util.util'].stack_images = lambda *a, **k: None
