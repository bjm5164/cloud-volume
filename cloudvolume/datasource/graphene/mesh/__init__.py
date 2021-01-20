from .sharded import GrapheneShardedMeshSource
from .unsharded import GrapheneUnshardedMeshSource
from .metadata import GrapheneMeshMetadata

from ..metadata import GrapheneMetadata
from ....cacheservice import CacheService
from ....paths import strict_extract
from ....cloudvolume import SharedConfiguration

class GrapheneMeshSource(object):
  def __new__(cls, meta, cache, config, readonly=False):
    mesh_meta = GrapheneMeshMetadata(meta, cache)

    if mesh_meta.is_sharded():
      return GrapheneShardedMeshSource(mesh_meta, cache, config, readonly) 

    return GrapheneUnshardedMeshSource(mesh_meta, cache, config, readonly)

  @classmethod
  def from_cloudpath(cls, cloudpath, cache=False, progress=False, storage_class=None):
    config = SharedConfiguration(
      cdn_cache=False,
      compress=True,
      compress_level=None,
      storage_class=storage_class,
      green=False,
      mip=0,
      parallel=1,
      progress=progress,
    )

    cache = CacheService(
      cloudpath=(cache if type(cache) == str else cloudpath),
      enabled=bool(cache),
      config=config,
      compress=True,
    )

    cloudpath, mesh_dir = os.path.split(cloudpath)
    meta = GrapheneMetadata(cloudpath, cache, info={ 'mesh': mesh_dir })

    return GrapheneMeshSource(meta, cache, config)