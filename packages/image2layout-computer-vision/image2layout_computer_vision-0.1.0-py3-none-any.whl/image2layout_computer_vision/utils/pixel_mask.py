import numpy as np

class PixelMask:
    @classmethod
    def coordinates(cls, shape=(10, 10)) -> np.ndarray:
        '''
        Return:
            coords: [H, W, 2] (y, x) coordinates map
        '''
        assert isinstance(shape, (list, tuple))
        assert len(shape) == 2
        coords = np.stack(
            np.meshgrid(*[np.arange(v) for v in shape], indexing="ij"),
            axis=-1,
        )
        return coords
    
    @classmethod
    def diagonal_mask(cls, shape=(10, 10)) -> np.ndarray:
        '''
        Return:
            mask: [H, W] (bool) mask of whether pixels are on the diagonal line
        '''
        if isinstance(shape, int):
            assert shape > 0
            return cls.diagonal_mask(shape=(shape, shape))
        coords = cls.coordinates(shape=shape)
        mask = coords[:, :, 0] == coords[:, :, 1]
        return mask
        
    @classmethod
    def edge_mask(cls, shape=(10, 10), amount:float=0.1) -> np.ndarray:
        '''
        Parameters:
            amount: (float) [0-1] the distance to the edge, 0 = none, 1 = entire image
        Return:
            mask: [H, W] (bool) mask of whether pixels are near the edges
        '''
        coords = cls.coordinates(shape=shape)
        mid_pos = (np.array(shape) - 1) / 2
        dist_map_yx = (coords - mid_pos) / mid_pos
        edge_dist = (1 - np.abs(dist_map_yx)).min(-1)
        mask = edge_dist <= amount
        return mask

    @classmethod
    def dist_map(cls, shape=(10, 10)) -> np.ndarray:
        '''
        Return:
            distmap: [H, W] (float) map of distance to the center
        '''
        coords = cls.coordinates(shape=shape)
        mid_pos = (np.array(shape) - 1) / 2
        dist_map_yx = (coords - mid_pos) / mid_pos
        dist_map = np.linalg.norm(dist_map_yx, axis=-1)
        dist_map /= np.clip(dist_map.max(), 0.000001, None)
        return dist_map
    
    @classmethod
    def checkerboard(cls, shape=(10, 10), cell_size:int=10) -> np.ndarray:
        '''
        Parameters:
            cell_size: (int) the size of the checkerboard cells
        Return:
            checker_mask: [H, W] (bool) checkerboard mask
        '''
        coords = PixelMask.coordinates(shape=shape).astype(float)
        coord_mod = np.floor(coords / cell_size).astype(int) % 2
        checker_mask = coord_mod[:, :, 0] == coord_mod[:, :, 1]
        return checker_mask
