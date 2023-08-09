####
# title: test_timeseries.py
#
# language: python3
# author: Elmar Bucher
# date: 2022-10-15
# license: BSD 3-Clause
#
# description:
#   pytest unit test library for the pcdl library pyMCDSts class.
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
import platform
import shutil


# const
s_path_2d = str(pathlib.Path(pcdl.__file__).parent.resolve()/'data_timeseries_2d')


# test data
if not os.path.exists(s_path_2d):
    pcdl.install_data()


# load physicell data time series
class TestPyMcdsTs(object):
    ''' test for pcdl.pyMCDSts data loader. '''
    mcdsts = pcdl.pyMCDSts(s_path_2d, verbose=False)

    ## get_xmlfile and read_mcds command ##
    def test_mcdsts_get_xmlfile_list(self, mcdsts=mcdsts):
        ls_xmlfile = mcdsts.get_xmlfile_list()
        assert len(ls_xmlfile) == 25

    def test_mcdsts_get_xmlfile_list_read_mcds(self, mcdsts=mcdsts):
        ls_xmlfile = mcdsts.get_xmlfile_list()
        ls_xmlfile = ls_xmlfile[-3:]
        l_mcds = mcdsts.read_mcds(ls_xmlfile)
        assert len(ls_xmlfile) == 3 and \
               len(l_mcds) == 3 and \
               len(mcdsts.l_mcds) == 3 and \
               mcdsts.l_mcds[2].get_time() == 1440

    def test_mcdsts_read_mcds(self, mcdsts=mcdsts):
        l_mcds = mcdsts.read_mcds()
        assert len(l_mcds) == 25 and \
               len(mcdsts.l_mcds) == 25 and \
               mcdsts.l_mcds[-1].get_time() == 1440

    def test_mcdsts_get_mcds_list(self, mcdsts=mcdsts):
        l_mcds = mcdsts.get_mcds_list()
        assert l_mcds == mcdsts.l_mcds

    ## data triage command ##
    def test_mcdsts_get_cell_df_states(self, mcdsts=mcdsts):
        dl_cell = mcdsts.get_cell_df_states(states=2, drop=set(), keep=set(), allvalues=False)
        assert len(dl_cell.keys()) == 28 and \
               len(dl_cell['oxygen']) == 2

    def test_mcdsts_get_cell_df_states_allvalues(self, mcdsts=mcdsts):
        dl_cell = mcdsts.get_cell_df_states(states=2, drop=set(), keep=set(), allvalues=True)
        assert len(dl_cell.keys()) == 28 and \
               len(dl_cell['oxygen']) > 2

    def test_mcdsts_get_conc_df_states(self, mcdsts=mcdsts):
        dl_conc = mcdsts.get_conc_df_states(states=2, drop=set(), keep=set(), allvalues=False)
        assert len(dl_conc.keys()) == 1 and \
               len(dl_conc['oxygen']) == 2

    def test_mcdsts_get_conc_df_states_allvalues(self, mcdsts=mcdsts):
        dl_conc = mcdsts.get_conc_df_states(states=2, drop=set(), keep=set(), allvalues=True)
        assert len(dl_conc.keys()) == 1 and \
               len(dl_conc['oxygen']) > 2

    ## magick command ##
    def test_mcdsts_handle_magick(self, mcdsts=mcdsts):
        s_magick = mcdsts._handle_magick()
        if not((os.system('magick --version') == 0) or ((platform.system() in {'Linux'}) and (os.system('convert --version') == 0))):
            s_magick = None
            print('Error @ pyMCDSts._handle_magick : image magick installation version >= 7.0 missing!')
        assert s_magick in {'', 'magick '}

    ## make_imgcell command ##
    def test_mcdsts_make_imgcell_cat(self, mcdsts=mcdsts):
        s_path = mcdsts.make_imgcell(
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

    def test_mcdsts_make_imgcell_cat_cmap(self, mcdsts=mcdsts):
        s_path = mcdsts.make_imgcell(
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

    def test_mcdsts_make_imgcell_num(self, mcdsts=mcdsts):
        s_path = mcdsts.make_imgcell(
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

    ## make_imgsubs command ##
    def test_mcdsts_make_imgsubs(self, mcdsts=mcdsts):
        s_path = mcdsts.make_imgsubs(
            focus = 'oxygen',
            z_slice = -3.333,  # test if
            extrema = None,  # test if
            #alpha = 1,  # matplotlib
            #fill = True,  # mcds.get_contour
            #cmap = 'viridis',  # matplotlib
            #grid = True,  # matplotlib
            xlim = None,  # test if
            ylim = None,  # test if
            xyequal = True,  # test if
            figsizepx = [641, 481],  # test non even pixel number
            ext = 'jpeg',
            figbgcolor = None,  # test if
        )
        assert os.path.exists(s_path + 'oxygen_000000000.0.jpeg') and \
               os.path.exists(s_path + 'oxygen_000001440.0.jpeg')
        shutil.rmtree(s_path)

    ## make_gif command ##
    def test_mcdsts_make_gif(self, mcdsts=mcdsts):
        s_path = mcdsts.make_imgcell()
        s_opathfile = mcdsts.make_gif(
            path = s_path,
            #interface = 'jpeg',
        )
        assert os.path.exists(s_opathfile) and \
            (s_opathfile == s_path+'cell_cell_type_z0_jpeg.gif')
        shutil.rmtree(s_path)

    ## make_movie command ##
    def test_mcdsts_make_movie(self, mcdsts=mcdsts):
        s_path = mcdsts.make_imgcell()
        s_opathfile = mcdsts.make_movie(
            path = s_path,
            #interface = 'jpeg',
            #framerate = 12,
        )
        assert os.path.exists(s_opathfile) and \
            (s_opathfile == s_path+'cell_cell_type_z0_jpeg12.mp4')
        shutil.rmtree(s_path)

