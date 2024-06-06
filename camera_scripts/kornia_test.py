import kornia as K
import kornia.feature as KF
import kornia.geometry.transform as transform
import torch

device = K.utils.get_cuda_or_mps_device_if_available()
print(device)

fname1 = "kn_church-2.jpg"
fname2 = "tree.jpg"

lg_matcher = KF.LightGlueMatcher("disk").eval().to(device)


img1 = K.io.load_image(fname1, K.io.ImageLoadType.RGB32, device=device)[None, ...]
img2 = K.io.load_image(fname2, K.io.ImageLoadType.RGB32, device=device)[None, ...]
img2 = transform.resize(img2, (1000,667), interpolation="bilinear")

num_features = 2048
disk = KF.DISK.from_pretrained("depth").to(device)

hw1 = torch.tensor(img1.shape[2:], device=device)
hw2 = torch.tensor(img2.shape[2:], device=device)


with torch.inference_mode():
    inp = torch.cat([img1, img2], dim=0)
    features1, features2 = disk(inp, num_features, pad_if_not_divisible=True)
    kps1, descs1 = features1.keypoints, features1.descriptors
    kps2, descs2 = features2.keypoints, features2.descriptors
    lafs1 = KF.laf_from_center_scale_ori(kps1[None], torch.ones(1, len(kps1), 1, 1, device=device))
    lafs2 = KF.laf_from_center_scale_ori(kps2[None], torch.ones(1, len(kps2), 1, 1, device=device))
    dists, idxs = lg_matcher(descs1, descs2, lafs1, lafs2, hw1=hw1, hw2=hw2)





print(f"{idxs.shape[0]} tentative matches with DISK LightGlue")

