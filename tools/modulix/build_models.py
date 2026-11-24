"""Builds the four Modulix configuration models (assets/models/modulix-*.glb)
from the single-module CAD export in module-source.glb. Run: python3 tools/modulix/build_models.py
Needs: pip install trimesh pygltflib numpy"""
import os, tempfile
HERE=os.path.dirname(os.path.abspath(__file__)); OUT=os.path.join(HERE,'..','..','assets','models'); TMP=tempfile.mkdtemp()
import os, trimesh, numpy as np, json, copy, os, pygltflib as g
from trimesh.visual.material import PBRMaterial
from trimesh.transformations import rotation_matrix, translation_matrix
src=trimesh.load(os.path.join(HERE,'module-source.glb'))
mod=list(src.geometry.values())[0].copy(); mod.apply_scale(0.01)
b=mod.bounds; mod.apply_translation([-(b[0][0]+b[1][0])/2, -b[0][1], -(b[0][2]+b[1][2])/2])
W,H,D=mod.extents
fab=PBRMaterial(name='Fabric',baseColorFactor=[0.26,0.27,0.28,1.0],metallicFactor=0.0,roughnessFactor=0.95)
def rbox(sx,sy,sz,r=0.03):
    pts=[]
    for x in (-1,1):
        for y in (-1,1):
            for z in (-1,1):
                s=trimesh.creation.icosphere(subdivisions=2,radius=r); s.apply_translation([x*(sx/2-r),y*(sy/2-r),z*(sz/2-r)]); pts.append(s.vertices)
    m=trimesh.convex.convex_hull(np.vstack(pts)); m.visual=trimesh.visual.TextureVisuals(material=fab); return m
geoms={'module':mod,
 'seat':rbox(D-0.02,0.12,W-0.03),          # sofa seat cushion (length along x)
 'back':rbox(D-0.03,0.40,0.14),            # sofa back cushion
 'lounge':rbox(2*D-0.02,0.10,W-0.03),      # lounger mattress
 'lback':rbox(0.12,0.46,W-0.03),           # lounger back cushion against the backrest
 'store':rbox(W-0.07,0.115,D-0.05)}        # cushion lying inside a module
sc=trimesh.Scene()
for k,v in geoms.items(): sc.add_geometry(v,geom_name=k,node_name=k)
open(os.path.join(TMP,'all.glb'),'wb').write(trimesh.exchange.gltf.export_glb(sc,include_normals=True))
base=g.GLTF2().load(os.path.join(TMP,'all.glb'))
for mat in base.materials:
    if mat.name!='Fabric':
        p=mat.pbrMetallicRoughness; p.baseColorFactor=[0.55,0.565,0.58,1.0]; p.metallicFactor=1.0; p.roughnessFactor=0.38; mat.doubleSided=True; mat.extensions={}
    mat.pbrMetallicRoughness.baseColorTexture=None
meshidx={n.name:n.mesh for n in base.nodes if n.mesh is not None}
BLOB=base.binary_blob()
T=lambda x=0,y=0,z=0: translation_matrix([x,y,z])
Rz=rotation_matrix(np.pi/2,[0,0,1]); Ry=rotation_matrix(np.pi/2,[0,1,0])
Rzm=rotation_matrix(-np.pi/2,[0,0,1])
def arm(x): return T(x,0,0)@T(0,W/2,0)@(Rzm if x<0 else Rz)@T(0,-H/2,0)  # mirror so both frames face outward
def seatm(x): return T(x,0,0)@Ry
tilt=rotation_matrix(np.radians(-10),[1,0,0])
cfg={}
cfg['single']=[('module',T())]
p=[('module',seatm(-D/2)),('module',seatm(D/2)),('module',arm(-(D+H/2))),('module',arm(D+H/2))]
p+=[('module',T(x,0,-W/2-H/2)@Ry@T(0,W/2,0)@Rz@T(0,-H/2,0)) for x in (-D/2,D/2)]
for x in (-D/2,D/2):
    p+=[('seat',T(x,H+0.06,0)),('back',T(x,H+0.12+0.19,-W/2+0.1)@tilt)]
cfg['sofa']=p
p=[('module',seatm(0)),('module',seatm(D)),('module',arm(-(D/2+H/2)))]
p+=[('lounge',T(D/2,H+0.05,0)),('lback',T(-D/2+0.06,H+0.10+0.23,0))]
cfg['lounger']=p
p=[]
for i in range(4):
    y=i*(H+0.004); p+=[('module',T(0,y,0)),('store',T(0,y+0.0775,0)),('store',T(0,y+0.1955,0))]
cfg['stack']=p
used=lambda c:{m for m,_ in c}
for k,parts in cfg.items():
    m=copy.deepcopy(base)
    m.nodes=[g.Node(mesh=meshidx[n],matrix=[float(v) for v in M.T.flatten()]) for n,M in parts]
    m.scenes=[g.Scene(nodes=list(range(len(parts))))]; m.scene=0
    m.buffers[0].uri=None; m.set_binary_blob(BLOB)
    m.save_binary(os.path.join(OUT,f'modulix-{k}.glb')); print(k,len(parts),'parts')
