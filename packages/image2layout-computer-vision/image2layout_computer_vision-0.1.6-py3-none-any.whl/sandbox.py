# %%
import os, time, string, json
import numpy as np
import pandas as pd
from PIL import Image
import image2layout_computer_vision as icv

# %%
fp = '/home/test/code/image2layout_computer_vision/data/inputs/image 559.png'
img = icv.get_image(fp)
img

# %%
CE = icv.ColorExtractor(img)
CE

# %%
CE.color_clusters_df

# %%






# %%
import os, time, string, json
import numpy as np
import pandas as pd
from PIL import Image
import plotly.express as px
import plotly.io as pio
pio.templates.default = 'plotly_dark'

from image2layout_computer_vision import get_image, COLOR, PixelMask
from image2layout_computer_vision.color_extract import (
    kmeans_cluster_colors,
)
from typing import Any, Union, Dict, List, Tuple
from sklearn.cluster import KMeans


# %%
class ColorExtractor:
    bg_score_weights = {
        'area': 1.0,
        'dist_median': 1.0,
        'dist_mean': 1.0,
    }
    
    def __init__(self, image:Image.Image):
        assert isinstance(image, Image.Image)
        self.image = image.convert('RGB')
        self.size = self.image.size
        self.process_colors()
    
    def process_colors(self,):
        self.color_clusters_df = self.analyze_colors_kmeans(self.image, n_clusters=2)
        self.mask_bg = np.array(self.color_clusters_df['mask'][0], bool)
        assert self.color_clusters_df.shape[0] in [1, 2], 'KMeans failed'
        
        if self.color_clusters_df.shape[0] == 1:
            self.colors = [
                tuple(self.color_clusters_df['color'][0])
                for _ in range(2)
            ]
        else:
            self.colors = [
                tuple(v)
                for v in self.color_clusters_df['color'][:2]
            ]
        
        assert len(self.colors) == 2, f'[ColorExtractor] error during analyze_colors_kmeans, did not return 2 colors?'
        self.color_bg, self.color_fg = self.colors
        return self.color_clusters_df
    
    def draw_anno(self):
        img_anno = Image.new('RGB', self.size, self.color_fg)
        img_bg_fill = Image.new('RGB', self.size, self.color_bg)
        img_anno.paste(
            img_bg_fill,
            (0,0),
            Image.fromarray((self.mask_bg.astype(float) * 255).astype(np.uint8), 'L'),
        )
        return img_anno
    
    @classmethod
    def analyze_colors_kmeans(cls, image:Image.Image, n_clusters:int=2) -> pd.DataFrame:
        assert isinstance(n_clusters, int)
        assert n_clusters >= 2
        colors = COLOR.get_colors(np.array(image), 3)
        colors_yiq = COLOR.rgb2yiq(colors)
        
        shape = np.array(colors_yiq.shape[:-1])
        
        cluster_mask, colors_center_yiq = kmeans_cluster_colors(colors_yiq, n_clusters)
        colors_center = COLOR.yiq2rgb(colors_center_yiq)
        
        assert cluster_mask.max() >= 0, f'KMeans failed to return any cluster??'
        
        dist_map = get_dist_map(shape)
        
        cluster_hist_data = []
        for i in range(cluster_mask.max() + 1):
            _mask = cluster_mask == i
            _dist_cluster = dist_map[_mask]
            _colors = colors[_mask]
            _colors_unique, _counts = COLOR.count_unique_colors(_colors)
            _ratio = _counts[0] / _counts.sum()
            
            _color = _colors_unique[0] if _ratio >= 1/2 else colors_center[i]
            _color_code = COLOR.rgb2hex(_color)
            
            _area = np.mean(_mask)
            _dist_median = np.quantile(_dist_cluster, 0.5)
            _dist_mean = np.mean(_dist_cluster)
            
            w = cls.bg_score_weights
            _bg_score = _area * w['area'] + _dist_median * w['dist_median'] + _dist_mean * w['dist_mean']
            
            cluster_hist_data.append({
                'mask': _mask,
                'area': _area,
                'color': _color,
                'color_code': _color_code,
                'dist_median': _dist_median,
                'dist_mean': _dist_mean,
                'bg_score': _bg_score,
            })
        
        color_clusters_df = pd.DataFrame(cluster_hist_data).sort_values('bg_score', ascending=False)
        
        return color_clusters_df

# %%
fp = '/home/test/code/image2layout_computer_vision/data/inputs/image 559.png'
img = get_image(fp).convert('RGB')
shape = img.size[::-1]
img

# %%
cluster_df = ColorExtractor.analyze_colors_kmeans(img, 2)
cluster_df

# %%
cluster_mask = np.zeros(shape, int)
for i, d in enumerate(cluster_df.to_dict('records')):
    cluster_mask[d['mask']] = i

cluster_mask

# %%
n_clusters = 2
amounts = [0.05, 0.1]
cluster_edge_scores_all = np.zeros((len(amounts), n_clusters), float)
for i, _amount in enumerate(amounts):
    edge_mask = PixelMask.edge_mask(shape=shape, amount=_amount)
    indices, counts = COLOR.count_uniques(cluster_mask[edge_mask])
    ratios = counts / counts.sum()
    
    cluster_edge_scores_all[i, indices] = ratios

cluster_edge_scores = cluster_edge_scores_all.mean(0)
cluster_edge_scores

# %%
cluster_edge_scores


# %%
cluster_df['edge_score'] = cluster_edge_scores
cluster_df


# %%
class ColorKMeans:
    def __init__(self,
                colors:Union[np.ndarray, Image.Image],
                n_clusters:int=2,
                edge_amounts:list=[0.05, 0.1, 0.15],
                middle_amounts:list=[0.2, 0.4],
                ):
        assert n_clusters >= 2
        self.n_clusters = n_clusters
        
        self.colors = COLOR.get_colors(np.array(colors), 3)
        self.colors_yiq = COLOR.rgb2yiq(self.colors)
        self.colors_yiq_flat = self.colors_yiq.reshape(-1, 3)
        
        self.shape = self.colors.shape[:-1]
        uniques, counts = COLOR.count_unique_colors(self.colors_yiq_flat)
        n_uniques = uniques.shape[0]
        assert n_uniques > 0, f'`data` is either empty or invalid'
        # if n_uniques == 1:
        #     return np.zeros(shape, int), uniques[0]
        assert n_clusters <= n_uniques
    
        self.model = KMeans(
            n_clusters=n_clusters,
            n_init='auto',
            init=uniques[:n_clusters],
        )
        cluster_indices = self.model.fit_predict(self.colors_yiq_flat)
        self.cluster_map = cluster_indices.reshape(self.shape)
        
        self.cluster_onehot = self.cluster_map[:, :, None] == np.arange(self.n_clusters)
        
        self.cluster_centers_yiq = self.model.cluster_centers_
        self.cluster_centers = COLOR.yiq2rgb(self.cluster_centers_yiq)
        
        self.center_dists = np.linalg.norm(
            self.cluster_centers_yiq[None] - self.cluster_centers_yiq[:, None],
            axis=-1,
        )
        self.center_dist_max = self.center_dists.max()
        self.center_dists_nonzero = self.center_dists[
            np.logical_not(PixelMask.diagonal_mask(self.n_clusters))
        ].reshape(self.n_clusters, self.n_clusters-1)
        
        self.cluster_errors = np.array([
            np.linalg.norm(
                self.colors_yiq[self.cluster_map == cluster_index] - self.cluster_centers_yiq[cluster_index][None],
                axis=-1
            ).mean()
            for cluster_index in range(self.n_clusters)
        ])
        self.cluster_errors_ratio = self.cluster_errors / self.center_dist_max
        
        self.edge_scores = self.compute_scores_from_dist(amount=edge_amounts, from_edge=True)
        self.middle_scores = self.compute_scores_from_dist(amount=middle_amounts, from_edge=False)
        self.areas = self.cluster_onehot.mean(0).mean(0)
    
    def __repr__(self) -> str:
        info = ' | '.join([
            f'{k}{v.round(3)}'
            for k, v in {
                'areas': self.areas,
                'errors_r': self.cluster_errors_ratio,
                'edge_scores': self.edge_scores,
                'middle_scores': self.middle_scores,
            }.items()
        ])
        return f'ColorKMeans[{self.n_clusters}]({info})'
    
    def compute_scores_from_dist(self, amount:float=0.1, from_edge:bool=True) -> np.ndarray:
        if isinstance(amount, (list, tuple, np.ndarray)):
            assert len(amount) >= 1
            edge_ratios = np.array([
                self.compute_scores_from_dist(amount=_amount, from_edge=from_edge)
                for _, _amount in enumerate(amount)
            ])
            edge_scores = edge_ratios.mean(0)
            return edge_scores
        
        _mask = PixelMask.edge_mask(shape=self.shape, amount=float(amount))
        if not from_edge:
            _mask = np.logical_not(_mask)
        _indices, _counts = COLOR.count_uniques(self.cluster_map[_mask])
        _scores = np.zeros(self.n_clusters, float)
        _scores[_indices] = _counts / _counts.sum()
        return _scores
    
ckm = ColorKMeans(img, 3)
ckm

# %%
bg_scores = ckm.edge_scores + ckm.areas / 4
bg_order = np.argsort(bg_scores)[::-1]
bg_index = bg_order[0]
bg_mask = ckm.cluster_map == bg_index
px.imshow(bg_mask)

# %%
# px.imshow(ckm.cluster_map)
ckm.cluster_map.shape

ckm.compute_edge_scores()

# %%
cluster_onehot = ckm.cluster_map[:, :, None] == np.arange(ckm.n_clusters)
cluster_onehot.shape

# %%
edge_ratios = np.zeros(ckm.n_clusters, float)
edge_mask = PixelMask.edge_mask(shape=ckm.shape, amount=.1)
_indices, _counts = COLOR.count_uniques(ckm.cluster_map[edge_mask])
edge_ratios[_indices] = _counts / _counts.sum()
edge_ratios


# %%
ckm.cluster_errors / ckm.center_dists_nonzero.min(-1)

# %%
center_dists_nearest = ckm.center_dists[ckm.center_dists > 0]
center_dists_nearest



# %%
ckm_3 = ColorKMeans(img, 3)
ckm_3.cluster_mask

px.imshow(ckm_3.cluster_mask)

# %%
ckm_4 = ColorKMeans(img, 4)
ckm_4.cluster_mask

px.imshow(ckm_4.cluster_mask)

# %%
import numpy as np
import cv2 as cv

# %%
contour_input = np.zeros([*shape, 3], np.uint8)

n = 3
colors = COLOR.hsv2rgb(np.array([[v, 1.0, 1.0] for v in np.linspace(0, 1, n+1)[:-1]]))
colors
for i in range(n):
    _mask = ckm_3.cluster_mask == i
    contour_input[_mask] = colors[i]

contour_input.shape

Image.fromarray(contour_input)

# %%
contour_input = np.zeros([*shape], np.uint8)
for i in range(n):
    _mask = ckm_3.cluster_mask == i
    contour_input[_mask] = 255 / (n - 1) * i

Image.fromarray(contour_input)

# %%
edges = cv.Canny(contour_input,100,200)
edges
Image.fromarray(edges)

# %%
contours, hierarchy = cv.findContours(
    # np.repeat(ckm_3.cluster_mask[:, :, None].astype(np.uint8), 3, axis=-1),
    ckm_3.cluster_mask.astype(np.uint8),
    # contour_input,
    # edges,
    cv.RETR_TREE,
    cv.CHAIN_APPROX_NONE,
)
contours

mask = np.zeros(shape, int)
for i, poss in enumerate(contours):
    for pos in poss.reshape(-1, 2):
        mask[pos[1], pos[0]] = i

mask
px.imshow(mask)

# %%
img_draw = np.array(img)
img_draw2 = cv.drawContours(img_draw, contours, 10, (0,255,0), 2)
# Image.fromarray(img_draw)
Image.fromarray(img_draw2)

# %%
hierarchy[0][2]

# %%
count, masks = cv.connectedComponents(ckm_3.cluster_mask.astype(np.uint8))
count, masks

masks.shape

# %%
px.imshow(masks)

# %%
px.imshow(ckm_3.cluster_mask.astype(np.uint8))

# %%