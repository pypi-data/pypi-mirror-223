# %%
import time
import numpy as np
import pandas as pd
from typing import Any, Union, Dict, List, Tuple
from PIL import Image, ImageDraw, ImageFont, ImageFilter


from sklearn.cluster import KMeans, MiniBatchKMeans

from ..utils import get_image, COLOR, PixelMask, Chrono, Timer

# %%
import logging
debug_logger = logging.getLogger('color_extract')
c_handler = logging.StreamHandler()
debug_logger.addHandler(c_handler)
debug_logger.setLevel(logging.WARNING)

# %%
class ColorKMeans:
    def __init__(self,
                colors:Union[np.ndarray, Image.Image, None]=None,
                colors_yiq:Union[np.ndarray, None]=None,
                n_clusters:Union[int, None]=2,
                cluster_centers:Union[np.ndarray, None]=None,
                edge_amounts:list=[0.05, 0.1],
                middle_amounts:list=[0.3],
                ):
        self.chrono = Chrono(f'ColorKMeans')
        self.chrono.watch('load')
        if colors_yiq is not None:
            assert colors is None
            self.colors_yiq = colors_yiq
        else:
            assert colors is not None
            self.shape = colors.shape[:-1]
            self.colors_yiq = COLOR.rgb2yiq(colors)
        
        self.shape = self.colors_yiq.shape[:-1]
        self.colors_yiq_flat = self.colors_yiq.reshape(-1, 3)
        
        assert n_clusters >= 2
        self.n_clusters = n_clusters
        
        # assert n_clusters is None or n_clusters >= 2
        # if cluster_centers is None:
        #     assert isinstance(n_clusters, int)
        #     assert n_clusters >= 2
        #     self.n_clusters = n_clusters
        #     uniques, counts = COLOR.count_unique_colors(self.colors_yiq_flat)
        #     cluster_centers = uniques[:n_clusters]
        #     if n_clusters > len(uniques):
        #         cluster_centers = np.pad(
        #             cluster_centers, [[0, n_clusters - len(uniques)], [0, 0]],
        #             mode='edge',
        #         )
        
        # self.n_clusters = len(cluster_centers)
        
        self.chrono.watch('fit')
        self.model = KMeans(
            n_clusters=self.n_clusters,
            n_init=1,
            init=cluster_centers,
            # n_init=2,
            max_iter=60,
        )
        # self.model = MiniBatchKMeans(
        #     n_clusters=self.n_clusters,
        #     n_init=1,
        #     init=cluster_centers,
        #     max_iter=20,
        # )
        cluster_indices = self.model.fit_predict(self.colors_yiq_flat)
        
        self.chrono.watch('post')
        self.cluster_map = cluster_indices.reshape(self.shape)
        
        self.cluster_onehot = self.cluster_map[:, :, None] == np.arange(self.n_clusters)
        
        self.cluster_centers_yiq = self.model.cluster_centers_
        self.cluster_centers = COLOR.yiq2rgb(self.cluster_centers_yiq)
        
        self.chrono.watch('score_prep')
        self.center_dists = np.linalg.norm(
            self.cluster_centers_yiq[None] - self.cluster_centers_yiq[:, None],
            axis=-1,
        )
        self.center_dist_max = self.center_dists.max()
        self.center_dists_nonzero = self.center_dists[
            np.logical_not(PixelMask.diagonal_mask(self.n_clusters))
        ].reshape(self.n_clusters, self.n_clusters-1)
        
        self.chrono.watch('error')
        self.cluster_errors = np.array([
            np.linalg.norm(
                self.colors_yiq[self.cluster_map == cluster_index] - self.cluster_centers_yiq[cluster_index][None],
                axis=-1
            ).mean()
            for cluster_index in range(self.n_clusters)
        ])
        self.cluster_errors_ratio = self.cluster_errors / self.center_dist_max
        
        self.chrono.watch('score')
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

# %%
class ColorExtractor:
    def __init__(self,
                image:Image.Image,
                n_clusters_max=4,
                n_clusters_min=4,
                with_foreground=True,
                **kwargs,
                ):
        '''
        Parameters:
            n_clusters_min / n_clusters_max (int): range of values for KMeans n_clusters
            with_foreground (bool): whether to extract foreground color
            kwargs:
                bg_error_ratio_max [0.05]
                unique_ratio_min [0.5]
        '''
        _id = np.random.choice(list('0123456789'), 10)
        self.chrono = Chrono(f'ColorExtractor_{_id}')
        
        self.chrono.watch('load')
        
        self.image = get_image(image).convert('RGB')
        self.size = self.image.size
        self.shape = np.array(self.image.size[::-1])
        
        self.chrono.watch('score')
        self.extracted_data = self.extract_colors_from_scores_and_dist(
            image=self.image,
            n_clusters_max=n_clusters_max,
            n_clusters_min=n_clusters_min,
            with_foreground=with_foreground,
            **kwargs,
        )
        self.chrono.watch('map')
        self.extract_map = self.extracted_data['extract_map']
        self.color_bg = tuple([int(v) for v in self.extracted_data['color_bg']])
        self.color_fg = tuple([int(v) for v in self.extracted_data['color_fg']])
        self.colors = (self.color_bg, self.color_fg)
        self.image_anno = None
        
        self.chrono.watch()
        
        debug_logger.debug(msg=f'ColorExtractor [{self.size[0]}x{self.size[1]}] > timers: ' + ' '.join([
            f"{'.'.join(k)}[{v.time_total:.3f}]"
            for k, v in self.chrono.timers.items()
        ]))
    
    def __repr__(self) -> str:
        return f'ColorExtractor[{self.shape}]({self.color_bg} | {self.color_fg})'
    
    def draw_anno(self,):
        _transparent_contrast = 32
        img_anno_np = np.zeros([*self.shape, 3], np.uint8) + (128 - _transparent_contrast)
        mask_checker = PixelMask.checkerboard([*self.shape], int(max(min(self.shape) // 20, 4)))
        img_anno_np[mask_checker] = [128 + _transparent_contrast] * 3
        # img_anno_np[np.logical_not(mask_checker)] = [128 - _transparent_contrast] * 3
        img_anno_np[self.extract_map == 0] = [*self.color_bg]
        img_anno_np[self.extract_map == 1] = [*self.color_fg]
        img_anno = Image.fromarray(img_anno_np, 'RGB')
        self.image_anno = img_anno
        return img_anno

    @classmethod
    def get_primary_color(cls, colors:np.ndarray, unique_ratio_min=0.5):
        '''
        Parameters:
            colors: (np.ndarray) [..., 3] RGB colors
        '''
        # time_perf_0 = time.perf_counter()
        
        _colors = COLOR.get_colors(colors, 3).reshape(-1, 3)
        # uniques, counts = COLOR.count_unique_colors(_colors)
        # ratios = counts / counts.sum()
        # if ratios[0] >= unique_ratio_min:
        #     time_perf_1 = time.perf_counter()
        #     return uniques[0]
        # colors_yiq = COLOR.rgb2yiq(_colors)
        # avg_color_yiq = colors_yiq.mean(0)
        # avg_color = COLOR.yiq2rgb(avg_color_yiq)
        
        # time_perf_1 = time.perf_counter()
        
        avg_color = _colors.mean(0).astype(np.uint8)
        return avg_color
    
    @classmethod
    def extract_colors_from_scores_and_dist(cls,
                image,
                n_clusters_max=5,
                n_clusters_min=2,
                bg_error_ratio_max=0.05,
                with_foreground=True,
                unique_ratio_min=0.5,
                **kwargs
                ):
        chrono = Chrono(f'ColorExtractor.extract_colors_from_scores_and_dist')
        
        chrono.watch('load')
        assert n_clusters_max >= n_clusters_min >= 2, f'n_clusters_max[{n_clusters_max}] >= n_clusters_min[{n_clusters_min}] >= 2'
        # data = []
        assert isinstance(image, Image.Image)
        assert image.mode == 'RGB'
        if isinstance(image, Image.Image):
            colors = COLOR.get_colors(np.array(image.convert('RGB')), 3)
        # else:
        #     assert isinstance(image, np.ndarray)
        #     colors = COLOR.get_colors(image, 3)
        
        chrono.watch('convert')
        # colors_yiq = COLOR.rgb2yiq(colors)
        # colors_yiq_flat = colors_yiq.reshape(-1, 3)
        shape = colors.shape[:-1]
        
        chrono.watch('count')
        # _round_scale = 20
        # colors_yiq_round = np.round(colors_yiq * _round_scale).astype(int)
        # uniques_yiq_round, counts = COLOR.count_unique_colors(colors_yiq_round)
        # uniques_yiq = uniques_yiq_round / _round_scale
        
        # TODO: experiment with ratios_cumsum for n_clusters selection ??
        # ratios = counts / counts.sum()
        # ratios_cumsum = np.cumsum(ratios)
        
        uniques_rgb = np.array([
            v[1]
            for v in sorted(image.getcolors(np.prod(image.size)))[-n_clusters_max:][::-1]
        ], np.uint8)
        chrono.watch('pre_cluster')
        d_out = {
            'n_clusters': 0,
            'bg_passed': True,
            'bg_error': 0.,
            'color_bg': (255, 255, 255),
            'color_fg': (0, 0, 0),
            'extract_map': np.zeros(shape, bool), 
        }
        
        n_uniques = len(uniques_rgb)
        if n_uniques == 0:
            return d_out
        if n_uniques == 1:
            d_out['color_bg'] = tuple([int(v) for v in n_uniques[0]])
            return d_out
        # n_clusters_max = min(n_clusters_max, n_uniques)
        # n_clusters_min = min(n_clusters_min, n_clusters_max)
        # if n_uniques < 2 or n_clusters_max < 2 or n_clusters_min < 2:
        #     return d_out
        
        assert len(uniques_rgb) >= 2, f'must have 2 unique colors at this point'
        n_clusters_max = min(n_clusters_max, n_uniques)
        n_clusters_min = min(n_clusters_min, n_clusters_max)
        
        chrono.watch('cluster')
        for n_clusters in range(n_clusters_min, n_clusters_max+1):
            chrono.watch('cluster', str(n_clusters))
            # _cluster_centers = uniques_yiq[:n_clusters]
            
            chrono.watch('cluster', str(n_clusters), 'CKM')
            ckm = ColorKMeans(
                # colors_yiq=colors_yiq,
                colors_yiq=colors,
                n_clusters=n_clusters,
                # cluster_centers=_cluster_centers,
                cluster_centers=uniques_rgb[:n_clusters],
                **kwargs,
            )
            extract_map = np.zeros(shape, int) - 1
            
            chrono.watch('cluster', str(n_clusters), 'bg')
            bg_scores = ckm.edge_scores + ckm.areas / 4
            bg_order = np.argsort(bg_scores)[::-1]
            bg_index = bg_order[0]
            bg_mask = ckm.cluster_map == bg_index
            
            if bg_mask.sum() > 0:
                chrono.watch('cluster', str(n_clusters), 'bg_primary')
                bg_color = cls.get_primary_color(colors[bg_mask], unique_ratio_min=unique_ratio_min)
                extract_map[bg_mask] = 0
                bg_error = ckm.cluster_errors_ratio[bg_index]
                bg_passed = bg_error <= bg_error_ratio_max
            else:
                bg_color = (255, 255, 255)
                bg_error = 100.
                bg_passed = False
            
            fg_color = (0, 0, 0)
            if with_foreground:
                chrono.watch('cluster', str(n_clusters), 'fg')
                fg_scores = ckm.middle_scores + ckm.areas / 10
                fg_order = np.argsort(fg_scores)[::-1]
                fg_index = [v for v in fg_order if v != bg_index][0]
                fg_mask = ckm.cluster_map == fg_index
                
                chrono.watch('cluster', str(n_clusters), 'fg_primary')
                if fg_mask.sum() > 0:
                    extract_map[fg_mask] = 1
                    fg_color = cls.get_primary_color(colors[fg_mask], unique_ratio_min=unique_ratio_min)
            
            d_out = {
                'n_clusters': n_clusters,
                'bg_passed': bg_passed,
                'bg_error': bg_error,
                'color_bg': tuple([int(v) for v in bg_color]),
                'color_fg': tuple([int(v) for v in fg_color]),
                'extract_map': extract_map, 
            }
            # data.append(d_out)
            del ckm
            
            chrono.watch('cluster', str(n_clusters))
            if bg_passed:
                break
        
        chrono.watch('cluster')
        chrono.watch()
        
        debug_logger.debug(msg=f'extract_colors... [{shape[1]}x{shape[0]}] > timers(ms): ' + ' '.join([
            f"{'.'.join(k)}[{v.time_total*1000:.0f}]"
            for k, v in chrono.timers.items()
        ]))
        
        return d_out


# %%
def extract_colors(image) -> Tuple[tuple]:
    img = get_image(image)
    color_extractor = ColorExtractor(img)
    return color_extractor.colors

# %%
if __name__ == '__main__':
    image = Image.open('path/to/the/image.png').convert('RGB')
    color_extractor = ColorExtractor(image)
    color_extractor.colors
    color_extractor.color_bg
    color_extractor.color_fg
