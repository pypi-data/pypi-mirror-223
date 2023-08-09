#####
# title: test_snapshot_2d.py
#
# language: python3
# author: Elmar Bucher
# date: 2022-10-15
# license: BSD 3-Clause
#
# description:
#   pytest unit test library for the pcdl library pyMCDS class.
#   + https://docs.pytest.org/
#
#   note:
#   assert actual == expected, message
#   == value equality
#   is reference equality
#   pytest.approx for real values
#####


# load library
import os
import pathlib
import pcdl


# const
s_path_2d = str(pathlib.Path(pcdl.__file__).parent.resolve()/'data_timeseries_2d')
s_file_2d = 'output00000024.xml'
s_pathfile_2d = f'{s_path_2d}/{s_file_2d}'


# test data
if not os.path.exists(s_path_2d):
    pcdl.install_data()


# load physicell data with microenvironment
class TestPyMcdsMicroenvTrue2D(object):
    ''' test for pcdl.pyMCDS data loader, the complete data set. '''
    mcds = pcdl.pyMCDS(xmlfile=s_file_2d, output_path=s_path_2d, custom_type={}, microenv=True, graph=True, settingxml='PhysiCell_settings.xml', verbose=True)

    def test_pyMCDS(self, mcds=mcds):
        # load physicell data
        print(f"process: pcdl.pyMCDS(xmlfile={s_file_2d}, output_path={s_path_2d}, custom_type={{}}, microenv=True, graph=True, settingxml='PhysiCell_settings.xml', verbose=True) ...")
        assert str(type(mcds)) == "<class 'pcdl.pyMCDS.pyMCDS'>"

    ## metadata related functions
    def test_mcds_get_multicellds_version(self, mcds=mcds):
        s_mcdsversion = mcds.get_multicellds_version()
        assert s_mcdsversion == 'MultiCellDS_2'

    def test_mcds_get_physicell_version(self, mcds=mcds):
        s_pcversion = mcds.get_physicell_version()
        assert s_pcversion == 'PhysiCell_1.10.4'

    def test_mcds_get_timestamp(self, mcds=mcds):
        s_timestamp = mcds.get_timestamp()
        assert s_timestamp == '2022-10-19T01:12:20Z'

    def test_mcds_get_time(self, mcds=mcds):
        r_time = mcds.get_time()
        assert r_time == 1440.0

    def test_mcds_get_runtime(self, mcds=mcds):
        r_runtime = mcds.get_runtime()
        assert r_runtime == 35.033598

    ## mesh related functions
    def test_mcds_get_voxel_ijk_range(self, mcds=mcds):
        ltr_range = mcds.get_voxel_ijk_range()
        assert ltr_range == [(0, 10), (0, 10), (0, 0)]

    def test_mcds_get_mesh_mnp_range(self, mcds=mcds):
        ltr_range = mcds.get_mesh_mnp_range()
        assert ltr_range == [(-15, 285), (-10, 190), (0, 0)]

    def test_mcds_get_xyz_range(self, mcds=mcds):
        ltr_range = mcds.get_xyz_range()
        assert ltr_range == [(-30, 300), (-20, 200), (-5, 5)]

    def test_mcds_get_voxel_ijk_axis(self, mcds=mcds):
        lar_axis = mcds.get_voxel_ijk_axis()
        assert (str(type(lar_axis)) == "<class 'list'>") and \
               (len(lar_axis) == 3) and \
               (str(type(lar_axis[0])) == "<class 'numpy.ndarray'>") and \
               (str(lar_axis[0].dtype) == "int64") and \
               (lar_axis[0].shape == (11,)) and \
               (str(type(lar_axis[1])) == "<class 'numpy.ndarray'>") and \
               (str(lar_axis[1].dtype) == "int64") and \
               (lar_axis[1].shape == (11,)) and \
               (str(type(lar_axis[2])) == "<class 'numpy.ndarray'>") and \
               (str(lar_axis[2].dtype) == "int64") and \
               (lar_axis[2].shape == (1,))

    def test_mcds_get_mesh_mnp_axis(self, mcds=mcds):
        lar_axis = mcds.get_mesh_mnp_axis()
        assert (str(type(lar_axis)) == "<class 'list'>") and \
               (len(lar_axis) == 3) and \
               (str(type(lar_axis[0])) == "<class 'numpy.ndarray'>") and \
               (str(lar_axis[0].dtype) == "float64") and \
               (lar_axis[0].shape == (11,)) and \
               (str(type(lar_axis[1])) == "<class 'numpy.ndarray'>") and \
               (str(lar_axis[1].dtype) == "float64") and \
               (lar_axis[1].shape == (11,)) and \
               (str(type(lar_axis[2])) == "<class 'numpy.ndarray'>") and \
               (str(lar_axis[2].dtype) == "float64") and \
               (lar_axis[2].shape == (1,))

    def test_mcds_get_mesh_flat_false(self, mcds=mcds):
        aar_mesh = mcds.get_mesh(flat=False)
        assert (str(type(aar_mesh)) == "<class 'numpy.ndarray'>") and \
               (len(aar_mesh) == 3) and \
               (str(type(aar_mesh[0])) == "<class 'numpy.ndarray'>") and \
               (str(aar_mesh[0].dtype) == "float64") and \
               (aar_mesh[0].shape == (11, 11, 1)) and \
               (str(type(aar_mesh[1])) == "<class 'numpy.ndarray'>") and \
               (str(aar_mesh[1].dtype) == "float64") and \
               (aar_mesh[1].shape == (11, 11, 1)) and \
               (str(type(aar_mesh[2])) == "<class 'numpy.ndarray'>") and \
               (str(aar_mesh[2].dtype) == "float64") and \
               (aar_mesh[2].shape == (11, 11, 1))

    def test_mcds_get_mesh_flat_true(self, mcds=mcds):
        aar_mesh = mcds.get_mesh(flat=True)
        assert (str(type(aar_mesh)) == "<class 'numpy.ndarray'>") and \
               (len(aar_mesh) == 2) and \
               (str(type(aar_mesh[0])) == "<class 'numpy.ndarray'>") and \
               (str(aar_mesh[0].dtype) == "float64") and \
               (aar_mesh[0].shape == (11, 11)) and \
               (str(type(aar_mesh[1])) == "<class 'numpy.ndarray'>") and \
               (str(aar_mesh[1].dtype) == "float64") and \
               (aar_mesh[1].shape == (11, 11))

    def test_mcds_get_mesh_2d(self, mcds=mcds):
        aar_mesh_flat = mcds.get_mesh(flat=True)
        aar_mesh_2d = mcds.get_mesh_2D()
        assert (str(type(aar_mesh_2d)) == "<class 'numpy.ndarray'>") and \
               (len(aar_mesh_2d) == 2) and \
               (aar_mesh_2d[0] == aar_mesh_flat[0]).all() and \
               (aar_mesh_2d[1] == aar_mesh_flat[1]).all()

    def test_mcds_get_mesh_coordinate(self, mcds=mcds):
        # cube coordinates
        ar_m_cube, ar_n_cube, ar_p_cube = mcds.get_mesh(flat=False)
        er_m_cube = set(ar_m_cube.flatten())
        er_n_cube = set(ar_n_cube.flatten())
        er_p_cube = set(ar_p_cube.flatten())
        # linear coordinates
        aar_voxel = mcds.get_mesh_coordinate()
        assert (str(type(aar_voxel)) == "<class 'numpy.ndarray'>") and \
               (len(aar_voxel) == 3) and \
               (str(type(aar_voxel[0])) == "<class 'numpy.ndarray'>") and \
               (str(aar_voxel[0].dtype) == "float64") and \
               (set(aar_voxel[0]) == er_m_cube) and \
               (aar_voxel[0].shape == (121,)) and \
               (str(type(aar_voxel[1])) == "<class 'numpy.ndarray'>") and \
               (str(aar_voxel[1].dtype) == "float64") and \
               (set(aar_voxel[1]) == er_n_cube) and \
               (aar_voxel[1].shape == (121,)) and \
               (str(type(aar_voxel[2])) == "<class 'numpy.ndarray'>") and \
               (str(aar_voxel[2].dtype) == "float64") and \
               (set(aar_voxel[2]) == er_p_cube) and \
               (aar_voxel[2].shape == (121,))

    def test_mcds_get_voxel_volume(self, mcds=mcds):
        r_volume = mcds.get_voxel_volume()
        assert r_volume == 6000.0

    def test_mcds_get_mesh_spacing(self, mcds=mcds):
        lr_spacing = mcds.get_mesh_spacing()
        assert lr_spacing == [30.0, 20.0, 1]

    def test_mcds_get_voxel_spacing(self, mcds=mcds):
        lr_spacing = mcds.get_voxel_spacing()
        assert lr_spacing == [30.0, 20.0, 10.0]

    def test_mcds_is_in_mesh(self, mcds=mcds):
        assert mcds.is_in_mesh(x=42, y=42, z=3, halt=False) and \
               not mcds.is_in_mesh(x=-42, y=-42, z=-42, halt=False)

    def test_mcds_get_voxel_ijk(self, mcds=mcds):
        li_voxel_0 = mcds.get_voxel_ijk(x=0, y=0, z=0, is_in_mesh=True)
        li_voxel_1 = mcds.get_voxel_ijk(x=15, y=10, z=0, is_in_mesh=True)
        li_voxel_2 = mcds.get_voxel_ijk(x=30, y=20, z=0, is_in_mesh=True)
        li_voxel_3 = mcds.get_voxel_ijk(x=42, y=42, z=42, is_in_mesh=True)
        assert (li_voxel_0 == [0, 0, 0]) and \
               (li_voxel_1 == [1, 1, 0]) and \
               (li_voxel_2 == [2, 2, 0]) and \
               (li_voxel_3 is None)

    ## micro environment related functions
    def test_mcds_get_substrate_names(self, mcds=mcds):
        ls_substrate = mcds.get_substrate_names()
        assert ls_substrate == ['oxygen']

    def test_mcds_get_substrate_dict(self, mcds=mcds):
        ds_substrate = mcds.get_substrate_dict()
        assert (str(type(ds_substrate)) == "<class 'dict'>") and \
               (len(ds_substrate) == 1)

    def test_mcds_get_substrate_df(self, mcds=mcds):
        df_substrate = mcds.get_substrate_df()
        assert (str(type(df_substrate)) == "<class 'pandas.core.frame.DataFrame'>") and \
               (df_substrate.shape == (1, 2))

    def test_mcds_get_concentration(self, mcds=mcds):
        ar_conc = mcds.get_concentration(substrate='oxygen', z_slice=None)
        assert (str(type(ar_conc)) == "<class 'numpy.ndarray'>") and \
               (ar_conc.shape == (11, 11, 1))

    def test_mcds_get_concentration_zslice_meshcenter(self, mcds=mcds):
        ar_conc = mcds.get_concentration(substrate='oxygen', z_slice=0, halt=False)
        assert (str(type(ar_conc)) == "<class 'numpy.ndarray'>") and \
               (ar_conc.shape == (11, 11))

    def test_mcds_get_concentration_zslice_non_meshcenter(self, mcds=mcds):
        ar_conc = mcds.get_concentration(substrate='oxygen', z_slice=-3.333, halt=False)
        assert (str(type(ar_conc)) == "<class 'numpy.ndarray'>") and \
               (ar_conc.shape == (11, 11))

    def test_mcds_get_concentration_at(self, mcds=mcds):
        ar_conc = mcds.get_concentration_at(x=0, y=0, z=0)
        assert (str(type(ar_conc)) == "<class 'numpy.ndarray'>") and \
               (ar_conc.shape == (1,))

    def test_mcds_get_concentration_df(self, mcds=mcds):
        df_conc = mcds.get_concentration_df(z_slice=None, halt=False, states=0, drop=set(), keep=set())
        assert (str(type(df_conc)) == "<class 'pandas.core.frame.DataFrame'>") and \
               (df_conc.shape == (121, 9))

    def test_mcds_get_concentration_df_zslice(self, mcds=mcds):
        df_conc = mcds.get_concentration_df(z_slice=0, halt=False, states=1, drop=set(), keep=set())
        assert (str(type(df_conc)) == "<class 'pandas.core.frame.DataFrame'>") and \
               (df_conc.shape == (121, 9))

    def test_mcds_get_concentration_df_states(self, mcds=mcds):
        df_conc = mcds.get_concentration_df(z_slice=None, halt=False, states=2, drop=set(), keep={'oxygen'})
        assert (str(type(df_conc)) == "<class 'pandas.core.frame.DataFrame'>") and \
               (df_conc.shape == (121, 9))

    def test_mcds_get_contour(self, mcds=mcds):
        fig = mcds.get_contour(
            'oxygen',
            z_slice = -3.333,  # test if
            vmin = None,  # test if
            vmax = None,  # test if
            #alpha = 1,  # matplotlib
            fill = False,  # contour case
            #cmap = 'viridis',  matplotlib
            title = 'test_mcds_get_contour',  # test if
            #grid = False, # matplotlib
            xlim = None,  # test if
            ylim = None,  # test if
            xyequal = True, # test if
            figsize = None,  # test if
            ax = None  # generate fig ax case
        )
        assert(str(type(fig)) == "<class 'matplotlib.figure.Figure'>")

    def test_mcds_get_contourf(self, mcds=mcds):
        fig = mcds.get_contour(
            'oxygen',
            z_slice = 0,  # jum over if
            vmin = None,  # test if
            vmax = None,  # test if
            #alpha = 1,  # matplotlib
            fill = True,  # contourf case
            #cmap = 'viridis',  # matplotlib
            title = 'test_mcds_get_contourf',  # test if
            #grid = True,  # matplotlib
            xlim = None,  # test if
            ylim = None,  # test if
            xyequal = True, # test if
            figsize = None,  # test if
            ax = None  # generate fig ax case
        )
        assert(str(type(fig)) == "<class 'matplotlib.figure.Figure'>")

    ## cell related functions
    def test_mcds_get_cell_variables(self, mcds=mcds):
        ls_variable = mcds.get_cell_variables()
        assert (str(type(ls_variable)) == "<class 'list'>") and \
               (len(ls_variable) == 77) and \
               (ls_variable[0] == 'ID')

    def test_mcds_get_celltype_dict(self, mcds=mcds):
        ds_celltype = mcds.get_celltype_dict()
        assert (str(type(ds_celltype)) == "<class 'dict'>") and \
               (len(ds_celltype) == 1)

    def test_mcds_get_cell_df(self, mcds=mcds):
        df_cell = mcds.get_cell_df(states=0, drop=set(), keep=set())
        assert (str(type(df_cell)) == "<class 'pandas.core.frame.DataFrame'>") and \
               (df_cell.shape == (1099, 94))

    def test_mcds_get_cell_df_states(self, mcds=mcds):
        df_cell = mcds.get_cell_df(states=2, drop=set(), keep=set())
        assert (str(type(df_cell)) == "<class 'pandas.core.frame.DataFrame'>") and \
               (df_cell.shape == (1099, 39))

    def test_mcds_get_cell_df_keep(self, mcds=mcds):
        df_cell = mcds.get_cell_df(states=0, drop=set(), keep={'oxygen'})
        assert (str(type(df_cell)) == "<class 'pandas.core.frame.DataFrame'>") and \
               (df_cell.shape == (1099, 12))

    def test_mcds_get_cell_df_at(self, mcds=mcds):
        df_cell = mcds.get_cell_df_at(x=0, y=0, z=0, states=1, drop=set(), keep=set())
        assert (str(type(df_cell)) == "<class 'pandas.core.frame.DataFrame'>") and \
               (df_cell.shape == (5, 94))

    ## get_scatter command ##
    def test_mcds_get_scatter_cat(self, mcdsts=mcdsts):
        s_path = mcds.get_scatter(
            focus='cell_type',  # case categorical
            z_slice = -3.333,   # test if
            z_axis = None,  # test if categorical
            #cmap = 'viridis',  # matplotlib
            #grid = True,  # matplotlib
            xlim = None,  # test if
            ylim = None,  # test if
            xyequal = True,  # test if
            s = None,  # test if
            figsizepx = [641, 481],  # case non even pixel number
            ext = 'jpeg', # test if
            figbgcolor = None,  # test if
        )
        assert os.path.exists(s_path + 'cell_type_000000000.0.jpeg') and \
               os.path.exists(s_path + 'cell_type_000001440.0.jpeg')
        shutil.rmtree(s_path)

    def test_mcds_get_scatter_cat_cmap(self, mcdsts=mcdsts):
        s_path = mcds.get_scatter(
            focus='cell_type',  # case categorical
            z_slice = -3.333,   # test if
            z_axis = None,  # test if categorical
            cmap = {'cancer_cell': 'maroon'},  # matplotlib
            #grid = True,  # matplotlib
            xlim = None,  # test if
            ylim = None,  # test if
            xyequal = True,  # test if
            s = None,  # test if
            figsizepx = [641, 481],  # case non even pixel number
            ext = 'jpeg', # test if
            figbgcolor = None,  # test if
        )
        assert os.path.exists(s_path + 'cell_type_000000000.0.jpeg') and \
               os.path.exists(s_path + 'cell_type_000001440.0.jpeg')
        shutil.rmtree(s_path)

    def test_mcds_get_scatter_num(self, mcdsts=mcdsts):
        s_path = mcds.get_scatter(
            focus='pressure',  # case numeric
            z_slice = -3.333,   # test if
            z_axis = None,  # test if numeric
            #cmap = 'viridis',  # matplotlib
            #grid = True,  # matplotlib
            xlim = None,  # test if
            ylim = None,  # test if
            xyequal = True,  # test if
            s = None,  # test if
            figsizepx = None,  # case extract from initial.svg
            ext = 'jpeg', # test if
            figbgcolor = None,  # test if
        )
        assert os.path.exists(s_path + 'pressure_000000000.0.jpeg') and \
               os.path.exists(s_path + 'pressure_000001440.0.jpeg')
        shutil.rmtree(s_path)

    ## graph related functions
    def test_mcds_get_attached_graph_dict(self, mcds=mcds):
        dei_graph = mcds.data['discrete_cells']['graph']['attached_cells']
        assert (str(type(dei_graph)) == "<class 'dict'>") and \
               (len(dei_graph) == 1099) and \
               (len(dei_graph[1098]) == 0)

    def test_mcds_get_neighbor_graph_dict(self, mcds=mcds):
        dei_graph = mcds.data['discrete_cells']['graph']['neighbor_cells']
        assert (str(type(dei_graph)) == "<class 'dict'>") and \
               (len(dei_graph) == 1099) and \
               (len(dei_graph[1098]) == 7)

    ## unit related functions
    def test_mcds_get_unit_se(self, mcds=mcds):
        se_unit = mcds.get_unit_se()
        assert (str(type(se_unit)) == "<class 'pandas.core.series.Series'>") and \
               (se_unit.shape == (82,))

