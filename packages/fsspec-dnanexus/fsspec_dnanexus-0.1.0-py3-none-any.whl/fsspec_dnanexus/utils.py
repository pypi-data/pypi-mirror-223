from .core import DXFileSystemException, DXBufferedFileOnRay, DXBufferedFile

FILECLASS_DICT = {
    "DXBufferedFileOnRay": DXBufferedFileOnRay, 
    "DXBufferedFile": DXBufferedFile
}

def get_n_partitions(df) -> int:
    from modin.pandas import DataFrame
    try:
        assert type(df) == DataFrame, "`df` must be modin.pandas.DataFrame"
        return len(df._query_compiler._modin_frame._partitions)
    except AssertionError as ae:
        raise DXFileSystemException(ae)
    
def provision_dx_on_ray():
    from modin import set_execution, __version__
    from packaging import version

    if version.parse(__version__) < version.parse("0.20.0"):
        raise DXFileSystemException(f"The version of Modin is too low. You need at least 0.20.0 but you have {__version__}. \
            Because Modin>=0.20.0 allows us to modify the Factory and PandasOnRayIO.")

    from modin.config import StorageFormat
    from modin.core.execution.dispatching.factories import factories

    from .dxfactory import DXPandasOnRayFactory
    factories.DxpandasOnRayFactory = DXPandasOnRayFactory
    StorageFormat.add_option("Dxpandas")

    set_execution(storage_format="Dxpandas")

def init_ray_with_fsspec_dnanexus(n_partitions: int = None):
    import os
    import ray
    import dxpy
    import modin.config as cfg

    # init ray
    if ray.is_initialized():
        ray.shutdown()

    dx_job_id = os.environ.get('DX_JOB_ID')
    ray.init(address='auto',
            _temp_dir="_tmp/ray",
            _plasma_directory="_tmp/ray",
            _node_ip_address=dxpy.describe(dx_job_id)['host'] if dx_job_id else ray._private.services.get_node_ip_address(),
            runtime_env={'env_vars': {'__MODIN_AUTOIMPORT_PANDAS__': '1'}},
        )
    
    # set NPartitions
    if n_partitions is not None:
        cfg.NPartitions.put(n_partitions)

    provision_dx_on_ray()